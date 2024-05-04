#!/usr/bin/python3
"""
Deletes out-of-date archives from local and remote servers.
Usage:
    fab -f 100-clean_web_static.py do_clean:number=2
    -i ssh-key -u ubuntu > /dev/null 2>&1
"""

import os
from fabric.api import *

env.hosts = ['54.236.17.144', '54.160.73.160']


def do_clean(number=1):
    """Delete out-of-date archives."""
    number = 1 if int(number) == 0 else int(number)

    # Local cleanup
    local_archives = sorted(os.listdir("versions"))
    [local_archives.pop() for _ in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(archive)) for archive in local_archives]

    # Remote cleanup
    with cd("/data/web_static/releases"):
        remote_archives = run("ls -tr").split()
        remote_archives = [archive for archive in remote_archives
                           if "web_static_" in archive]
        [remote_archives.pop() for _ in range(number_to_keep)]
        [run("rm -rf ./{}".format(archive)) for archive in remote_archives]
