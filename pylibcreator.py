#!/usr/bin/env python
"""
A script that helps initiate a new python library. 

Dependencies: 
$ pip install requests

Usage: pylibcreator.py --path /path/to/foo_lib --token <github_personal_token>

Does the following tasks for you:
1) Initializes a new private git repository for foo_lib on github and clones that to /path/to/foo_lib
2) Sets up package and tests directories 
3) Sets up a setup.py file with initial contents
"""
#Standard Lib
import sys
import os
import getopt
import urllib2
import json

#External Dependencies
import requests 

class LibCreator(object):
    """
    Class that maintains state about the library path and git user to help creating a python library and exposes a LibCreateor_self.run() method 
    to execute the process of creating a new library. 
    """
    def __init__(self, libpath, ghtoken):
        self._libpath = os.path.expanduser(libpath)
        self._ghtoken = ghtoken

    def _libname(self):
        """
        Returns the library name
        """
        return os.path.basename(self._libpath)

    def _libdir(self):
        """
        Returns the directory on the filesystem that contains the library
        """
        return os.path.dirname(self._libpath)

    def _setup_with_git(self):
        if os.path.exists(self._libpath):
            raise StandardError("Directory already exists at {0}".format(self._libpath))
        
        old_cwd = os.getcwd() #Save current directory to get back to that later. 
        os.chdir(self._libdir())
        try:
            github_create_url = "https://api.github.com/user/repos"
            data = json.dumps({'name':self._libname(),
                               'description':'A python library',
                               'private':True,
                               'has_wiki':True,
                               'auto_init':True,
                               'gitignore_template':'Python',})
            response = requests.post(github_create_url, data, auth=(self._ghtoken, 'x-oauth-basic'))
            if response.status_code != 201:
                raise StandardError("Unexpected response when trying to create repository\nResponse: {0}\n\n{1} \n".format(response.status_code, response.json()))
            response_body = response.json()
            repo_url = response_body['ssh_url']
            if repo_url == None or len(repo_url) == 0:
                raise StandardError("Could not get the repository url from github create repo response: %s".format(response_body))
            os.system("git clone {0}".format(repo_url))
	finally:
	    os.chdir(old_cwd)

    def _setup_dir_structure(self):
	old_cwd = os.getcwd()
        print "Setting up setup.py file and package and tests directories in {0} ... ".format(self._libpath)
        os.chdir(self._libpath)
        os.mkdir(self._libname())
        os.mkdir("tests")
        os.system("touch {0}/__init__.py".format(self._libname()))
        os.system("touch tests/__init__.py")
        os.system("touch setup.py")
        setup_string = """\
from distutils.core import setup 

setup(
    name='{0}',
    version='0.0.1',
    packages=['{0}', ],
    license='MIT License',
    description='',
    long_description='',
) """.format(self._libname())

        setup_file_path = os.path.join(self._libpath, 'setup.py')
        if not os.path.exists(setup_file_path):
            raise StandardError("Trying to write to setup.py but it doesn't exist at path {0}".format(setup_file_path))

        print "Now writing to setup.py: {0}".format(setup_string)
        print "Initializing setup.py contents for {0} ... ".format(setup_file_path)
        with open(setup_file_path, 'w') as f:
            f.write(setup_string)

    def run(self):
        """
        Actually executes process of creating library. 
        """
        try:
            self._setup_with_git()
            self._setup_dir_structure()
            os.chdir(self._libpath)
        except StandardError, e:
            print "Error setting up library: {0}".format(e)
            sys.exit(1)
        


def main():
    path = ''
    token = ''
    usage_string = 'pylibcreate.py -p <path_for_library> -t <github_token>'
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:t:", ["help", "path=", "token="])
    except getopt.GetoptError:
        print usage_string
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print usage_string
        elif opt in ('-p', '--path'):
            path = arg
        elif opt in ('-t', '--token'):
            token = arg
        else:
            print "Invalid option: " + opt
            print "Usage: " + usage_string
            sys.exit(2)

    if len(path.strip()) == 0 or len(token.strip()) == 0:
        print "Invalid arguments. Must provide non-empty path and user. \nUsage: " + usage_string
        sys.exit(2)

    lc = LibCreator(path, token)
    lc.run()

if __name__ == '__main__':
    main()
        
