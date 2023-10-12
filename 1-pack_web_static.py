#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo.
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Create a compressed archive from the web_static folder.
    """
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_{}.tgz".format(timestamp)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_name))
        if os.path.exists(archive_name):
            return archive_name
        else:
            return None
    except Exception:
        return None
