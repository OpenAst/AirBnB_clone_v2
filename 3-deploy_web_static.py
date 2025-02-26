#!/usr/bin/python3
from fabric.api import run, local, put, env
import datetime
import os


def do_pack():
    now = datetime.datetime.now()
    date = (str(now.year) + str(now.month) + str(now.day) + str(now.hour) +
            str(now.minute) + str(now.second))
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz ./web_static".format(date))
        return "./versions/web_static_{}.tgz".format(date)
    except:
        return None


env.hosts = ['35.190.188.208', '35.227.47.184']


def do_deploy(archive_path):
    if os.path.exists(archive_path) is False:
        return False
    try:
        upload = put(archive_path, "/tmp/")
        name = archive_path[11:-4]
        rmt_path = "/data/web_static/releases/" + name
        run("mkdir {}".format(rmt_path))
        run("tar -xvzf /tmp/{}.tgz --directory {}/".format(name, rmt_path))
        run("rm /tmp/{}.tgz".format(name))
        run("rm /data/web_static/current")
        run("ln -nsf /data/web_static/releases/{} /data/web_static/current"
            .format(name))
        run("mv {}/web_static/* {}".format(rmt_path, rmt_path))
        run("rm -d {}/web_static/".format(rmt_path))
        return True
    except:
        return False


def deploy():
    path = do_pack()
    print("este es el path: ", path)
    if path is None:
        return False
    return do_deploy(path)
