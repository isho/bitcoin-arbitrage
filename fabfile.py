
from fabric.api import run, env

env.hosts = ['isho.tv']

def hello():
    print("Hello world!")


def ls():
    run("pwd")
    run("ls")