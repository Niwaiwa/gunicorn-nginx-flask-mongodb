# Gunicorn config variables
loglevel = "info"
errorlog = "-"  # stderr
accesslog = "-"  # stdout
worker_tmp_dir = "/dev/shm"
graceful_timeout = 30
timeout = 120
keepalive = 5
# threads = 3
workers = 2
max_requests = 2000

# gevent
worker_class = "gevent"
worker_connections = 1000
