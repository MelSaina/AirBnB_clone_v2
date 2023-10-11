#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import env, put, run, local
from os.path import exists
import os
from datetime import datetime

env.hosts = ['52.86.203.247','100.25.212.105']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
    if not exists(archive_path):
        return False
    try:
        filename = os.path.basename(archive_path)
        basename = os.path.splitext(filename)[0]
        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}".format(basename))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(filename, basename))
        run("rm /tmp/{}".format(filename))
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}".format(basename, basename))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{} /data/web_static/current".format(basename))
        return True
    except Exception as e:
        return False
