#!/usr/bin/python

import os
import sys

def find_executable(executable, paths):
    for path in paths.split(os.pathsep):
        fullpath = os.path.join(path, executable)
        if os.access(fullpath, os.X_OK):
            return fullpath
    print '%s: Command not found.' % executable
    sys.exit(1)

def run_wrapped_executable(executable, options):
    current_path = os.path.dirname(sys.argv[0])
    paths = os.environ['PATH'].split(os.pathsep)
    if current_path not in paths:
        current_path = os.getcwd()
    try:
        paths.remove(current_path)
    except:
        pass # must not be there to begin with ..

    path_env = os.pathsep.join(paths)
    cmd = find_executable(executable, path_env)
    # need to use popen ..
    os.execv(cmd, options)

path = os.environ['PATH']
path = "/tmp/curldir:" + path
os.environ['PATH'] = path

run_wrapped_executable('scramv1', sys.argv)
