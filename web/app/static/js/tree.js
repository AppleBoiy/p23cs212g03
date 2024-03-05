const rectangleData = {};
const courseData = {};
const courseList = [];
const edgesList = [];

const debug = true;

const main = () => {
    const spreadsheetUrl = "https://docs.google.com/spreadsheets/d/1t8dvUUdvOxdiKQv5nagGaHyiw3P-C2o0Qg6C_1Tlq58/edit?usp=sharing";

    spreadsheetToJson(spreadsheetUrl)
        .then(async rawData => {
            await generateTreeView(rawData);

            for (const subject of rawData) {
                const abbreviation = subject.abbr;
                rectangleData[abbreviation] = {};
                courseData[abbreviation] = subject;
            }

            const nodeDivs = document.getElementsByClassName("node");
            Array.from(nodeDivs).forEach(div => {
                const [rect, text] = div.childNodes;
                const rectData = rectangleData[div.id];

                Object.assign(rectData, {
                    rectangleDiv: rect,
                    textDiv: text,
                    nodeDiv: div,
                    originalFill: rect.style.fill,
                    originalStroke: rect.style.stroke,
                    highlightFill: "#eb8f34",
                    highlightStroke: "#000"
                });
            });

            for (const [abbreviation, rectData] of Object.entries(rectangleData)) {
                const {nodeDiv} = rectData;
                attachEventHandlers(abbreviation, nodeDiv);
            }


        })
        .catch(error => console.log(error));
};

/**
 * Fetches a spreadsheet from the provided URL and converts it to JSON format.
 * Each row in the spreadsheet becomes an object in the resulting array.
 * The headers of the spreadsheet become the keys of the objects.
 *
 * @param {string} url - The URL of the spreadsheet to fetch and convert.
 * @returns {Promise<Array<Object>|null>} - A Promise that resolves to an array of objects representing the spreadsheet data in JSON format.
 *                                          Returns null if an error occurs during the fetch or conversion process.
 */
async function spreadsheetToJson(url) {
    const response = await fetch(url);
    const data = await response.arrayBuffer();

    const workbook = XLSX.read(data, {type: "array"});
    const [workSheet] = workbook.SheetNames;
    const worksheet = workbook.Sheets[workSheet];

    const range = XLSX.utils.decode_range(worksheet["!ref"]);
    range["s"]["r"] = 1;
    range["s"]["c"] = 1;

    const rawJsonData = XLSX.utils.sheet_to_json(worksheet, {header: 1, range});
    const infoCount = rawJsonData[0].length;

    const jsonData = rawJsonData.filter(data => {
        return data.length === infoCount && !data.includes(undefined);
    });

    const [headers, ...rows] = jsonData;

    const result = rows.map(row =>
        headers.reduce((obj, headerCell, index) => {
            obj[headerCell] = row[index];
            return obj;
        }, {})
    );

    const parseValue = (value) => {
        return value.toString() === "-" ? [] : value.toString().split(", ");
    };

    result.forEach(element => {
        element.parent = parseValue(element.parent);
        element.children = parseValue(element.children);
    });

    return result;
}

/**
 * Generates a tree view of prerequisite tree from a JSON-like object.
 * @param {Object} rawData - Dictionary of course details.
 */
async function generateTreeView(rawData) {

    if (debug) {
        console.log(rawData);
    }

    const graphlib = dagreD3.graphlib;
    const render = dagreD3.render();

    const svg = d3.select("svg");
    const svgGroup = svg.append("g");

    const mainTree = new graphlib.Graph();
    mainTree.setGraph({ranksep: 100});
    mainTree.setDefaultEdgeLabel({});

    for (const subject of rawData) {
        mainTree.setNode(subject.code, {
            label: subject.abbr,
            width: 50,
            height: 30,
            id: subject.abbr,
            class: `y${subject.year}`
        });

        subject.children.forEach(child => {
            mainTree.setEdge(subject.code, child, {
                class: `${subject.code}-${child}`
            });
        });

        courseList.push(subject.abbr);
    }


    mainTree.nodes().forEach(v => {
        const node = mainTree.node(v);
        Object.assign(node, {rx: 10, ry: 10});
    });


    render(d3.select("svg g"), mainTree);

    svg.attr("width", mainTree.graph().width + 120);
    svg.attr("height", mainTree.graph().height + 120);

    svgGroup.attr("transform", `translate(${60}, ${60})`);

    for (const edge of document.querySelectorAll(".edgePath")) {
        const [, relation] = edge.classList;
        const [parent, child] = relation.split("-").map(e => convertCourseId(e));

        edgesList.push({
            parent,
            child,
            rect: edge
        });
    }
}

/**
 * Traverses a node hierarchy based on an abbreviation.
 * Returns an array of parent nodes and their ancestors.
 *
 * @param {string} abbreviation - The abbreviation of the node to traverse.
 * @returns {Array} - An array containing the parent nodes and their ancestors.
 */
function getNodeAncestors(abbreviation) {
    const parents = courseData[abbreviation]?.parent.map(e => convertCourseId(e));

    if (!parents) return [];

    const ancestors = parents.map(e => getNodeAncestors(e));
    const flattenedAncestors = ancestors.flat();

    return [...parents, ...flattenedAncestors];
}

/**
 * Highlights or reverts the highlight of a rectangle element.
 *
 * @param {string} abbreviation - The abbreviation associated with the rectangle to be highlighted or reverted.
 * @param mode
 */
function highlightRectangle(abbreviation, mode = "") {
    const rectData = rectangleData[abbreviation];
    const {highlightFill, highlightStroke, originalFill, originalStroke} = rectData;
    const rectangle = rectData.rectangleDiv;

    switch (mode) {
        case "enter":
            rectangle.style.fill = highlightFill;
            rectangle.style.stroke = highlightStroke;
            break;

        case "leave":
            rectangle.style.fill = originalFill;
            rectangle.style.stroke = originalStroke;
            rectangle.style.opacity = "1";
            break;

        default:
            rectangle.style.opacity = "0.1";

    }
}

/**
 * Converts an ID or abbreviation to its corresponding.
 *
 * @param {string} identifier - The ID or Abbreviation to be converted.
 * @returns {string} The corresponding abbreviation or ID.
 */
function convertCourseId(identifier) {
    const courseMapping = {
        "204": "CS",
        "206": "Math",
        "208": "Stat",

        "CS":"204",
        "Math":"206",
        "Stat":"208"
    };

    return `${courseMapping[identifier.slice(0, 3)]}${identifier.slice(3)}`
}

/**
 * Attaches event handlers to a given node element based on the provided abbreviation.
 *
 * @param {string} abbreviation - The abbreviation of the node.
 * @param {HTMLElement} nodeEl - The node element to attach the event handlers to.
 * @returns {void} - This function does not return a value.
 */
function attachEventHandlers(abbreviation, nodeEl) {
    const data = courseData[abbreviation];

    const popupEl = document.getElementById("popup");
    const closeEl = document.getElementById("close");

    const childCodes = data.children.map(convertCourseId);
    const nodes = [abbreviation, ...childCodes, ...getNodeAncestors(abbreviation)];
    const unrelatedNodes = courseList.filter(course => !nodes.includes(course));

    const fadedEdges = [];

    const handleMouseEnter = () => {
        nodes.forEach(node => highlightRectangle(node, "enter"));
        unrelatedNodes.forEach(node => highlightRectangle(node, "fade"));

        edgesList.forEach(({ parent, child, rect }) => {
            if (!nodes.includes(parent) || !nodes.includes(child)) {
                rect.style.opacity = "0.1";
                fadedEdges.push(rect);
            }
        });
    };

    const handleMouseLeave = () => {
        nodes.forEach(node => highlightRectangle(node, "leave"));
        unrelatedNodes.forEach(node => highlightRectangle(node, "leave"));
        fadedEdges.forEach(edge => (edge.style.opacity = "1"));
    };

    const handleMouseClick = (event) => {
        event.preventDefault();
        popupEl.style.display = "flex";
        const [nameEl, contentEl] = popupEl.children[0].children;

        nameEl.innerHTML = data["full name (ENG)"];
        let courseContent = "";
        for (const [key, value] of Object.entries(courseData[abbreviation])) {
            courseContent += key + " : " + value + "<br/>"
        }
        contentEl.innerHTML = courseContent;

        nodeEl.removeEventListener("mouseleave", handleMouseLeave);
        handleMouseEnter();
    };


    closeEl.addEventListener("click", (event) => {
        event.preventDefault();
        if (popupEl.style.display !== "none") {
            popupEl.style.display = "none";
        } else {
            nodeEl.addEventListener("mouseleave", handleMouseLeave);
            handleMouseLeave();
        }
    });

    // Add custom styles to the node element
    nodeEl.style.cursor = "pointer";
    nodeEl.style.transition = "background-color 3s ease";

    nodeEl.addEventListener("mouseenter", handleMouseEnter);
    nodeEl.addEventListener("mouseleave", handleMouseLeave);
    nodeEl.addEventListener("click", handleMouseClick);
}



main()