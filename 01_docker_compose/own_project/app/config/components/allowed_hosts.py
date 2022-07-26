import os


def load_allowed_hosts():
    env = os.environ.get('ALLOWED_HOSTS', '')
    return env.split(',')


ALLOWED_HOSTS = load_allowed_hosts()
