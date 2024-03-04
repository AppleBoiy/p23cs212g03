from flask import jsonify, render_template, request, url_for, flash, redirect
import json
from sqlalchemy.sql import text
from app import app, db
from app.models.blog import BlogEntry


@app.route("/hw10", methods=("GET", "POST"))
def hw10():
    if request.method == "POST":
        app.logger.debug("POST request received")
        result = request.form.to_dict()
        #         app.logger.debug(str(result))
        name = result.get("name", "")
        message = result.get("message", "")
        email = result.get("email", "")

        validated = True
        validated_dict = dict()
        valid_keys = ["name", "message", "email"]

        for key in valid_keys:
            #             app.logger.debug(f"Validating {key}")

            if key not in valid_keys:
                continue

            value = result.get(key)

            if not value or value == "undefined":
                #                 app.logger.debug(f"Validation failed for {key}")
                validated = False
                break
            else:
                # Remove "undefined" value and store the actual value (if any)
                validated_dict[key] = value.strip() if value else ""

        if validated:
            app.logger.debug("validated dict: {validated_dict}")
            entry = BlogEntry(**validated_dict)
            #             app.logger.debug(str(entry))
            db.session.add(entry)
            db.session.commit()

        return redirect(url_for("hw10"))

    # type of data: <class 'flask.wrappers.Response'>
    data = hw10_data()
    data = json.loads(data.get_data(as_text=True))
    #
    #     app.logger.debug("GET request received")
    #     app.logger.debug(f"data: {data}")

    return render_template("hw10_microblog.html", data=data)


def hw10_data():
    data = BlogEntry.query.all()
    data = [d.to_dict() for d in data]
    return jsonify(data)


@app.route("/hw10/edit/<int:post_id>", methods=("GET", "POST"))
def edit_post(post_id):
    if request.method == "POST":
        result = BlogEntry.query.filter_by(id=post_id).first()
        app.logger.debug("post: " + str(result.to_dict()))
        message = result.to_dict().get("message", "")
        if message:
            post = BlogEntry.query.filter_by(id=post_id).first()
            post.update(message=message)
            db.session.commit()
        return redirect(url_for("hw10"))
    # type of data: <class 'flask.wrappers.Response'>
    posts = BlogEntry.query.filter_by(id=post_id).all()
    #         app.logger.debug(f"posts: {posts[0].to_dict()}")
    if posts:

        return jsonify(posts[0].to_dict())
    return jsonify({"error": "Post not found"})
