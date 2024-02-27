# Change directory to specified directory before loading apps.
chdir = 'app'
# The number of worker processes for handling requests.
workers = 2
# The number of worker threads for handling requests.
threads = 2
# The socket to bind.
bind = ['0.0.0.0:8000']
# How verbose the Gunicorn error logs should be
loglevel = 'debug'
# default is the send error log to stdout
#errorlog = '-'
#accesslog = '-'
# Whether to send flask output to the error log
capture_output = True
# hot reload
reload = True
