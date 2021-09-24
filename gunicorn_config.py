import os

# https://docs.gunicorn.org/en/stable/settings.html

proc_name = 'fyle-interview-be'
port_number = int(os.environ.get('GUNICORN_PORT', 7755))
bind = '0.0.0.0:{0}'.format(port_number)

backlog      = int(os.environ.get('GUNICORN_BACKLOG', 50))
workers      = int(os.environ.get('GUNICORN_NUMBER_WORKERS', 1))
threads      = int(os.environ.get('GUNICORN_NUMBER_WORKER_THREADS', 1))
worker_connections = int(os.environ.get('GUNICORN_NUMBER_WORKER_CONNECTIONS', 20))
timeout      = int(os.environ.get('GUNICORN_WORKER_TIMEOUT', 60))
keepalive    = int(os.environ.get('GUNICORN_KEEPALIVE', 2))

loglevel     = os.environ.get('GUNICORN_LOG_LEVEL', 'info')
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'sync')
max_requests = int(os.environ.get('GUNICORN_MAX_REQUESTS', 0))
max_requests_jitter = int(os.environ.get('GUNICORN_MAX_REQUESTS_JITTER', 20))
graceful_timeout = int(os.environ.get('GUNICORN_WORKER_GRACEFUL_TIMEOUT', 5))

reload = True

limit_request_line = 0

spew = False

daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

errorlog = '-'
accesslog = '-'
access_log_format = '%({X-Real-IP}i)s - - - %(t)s.%(T)s "%(r)s" "%(f)s" "%(a)s" %({X-Request-Id}i)s %(L)s %(b)s %(s)s'
# todo - JC: pass org_user_id tpa_id proxy_id and replace the three dashes in above format


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker):
    pass


def pre_exec(server):
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    server.log.info("Server is ready. Spawning workers")


def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

    # get traceback info
    import threading
    import sys
    import traceback
    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    code = []
    for thread_id, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(thread_id, ""),
                                            thread_id))
        for filename, line_no, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                                                        line_no, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))


def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")


def child_exit(server, worker):
    server.log.info("server: child_exit is called")
    worker.log.info("worker: child_exit is called")


def worker_exit(server, worker):
    server.log.info("server: worker_exit is called")
    worker.log.info("worker: worker_exit is called")


def nworkers_changed(server, new_value, old_value):
    server.log.info("server: nworkers_changed is called with new_value: %s old_value: %s", new_value, old_value)


def on_exit(server):
    server.log.info("server: on_exit is called")