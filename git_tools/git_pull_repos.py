#!/bin/bash

from optparse import OptionParser, OptionError

import subprocess
import sys


class RequiredOptionError(OptionError):
   def __init__(self, option_id):
      OptionError.__init__(self, 'could not be omitted, try --help for details', option_id)


def check_required(opts, *argv):
   for k in argv:
      if not getattr(opts, k):
         raise RequiredOptionError(k)


class Options(OptionParser):

   def __init__(self):
      usage = "usage: %prog -h host -p proj -f repo_names_file \n scripts clones repositories listed in file"
      OptionParser.__init__(self, usage=usage)

      self.add_option('-s', '--host', dest='host', help="host of repository ")
      self.add_option('-f', '--file', dest='repo_names', help="files with list of repository names")
      self.add_option('-p', '--proj', dest='proj', help="task suffix")
      self.add_option('-c', '--command', dest='command', help="git command to execute, clone by default", default="pull")

   def parse(self, argv):
      (opts, args) = OptionParser.parse_args(self, argv[1:])
     
      check_required(opts, 'host')
      check_required(opts, 'repo_names')
      check_required(opts, 'proj')

      self.__dict__.update(opts.__dict__)


def main(argv):

   opts = Options()
   opts.parse(argv)

   repo_names = []
   repo_names = open(opts.repo_names, "r").read().splitlines()

   #print("repo_names=", repo_names)

   return_code = 0

   for repo in repo_names:
       fullreponame = f"{opts.host}:{repo}-{opts.proj}"
       #print(fullreponame)
       params = ["git", opts.command, fullreponame]
       process = subprocess.Popen(params, stdout=subprocess.PIPE)
       res = process.communicate()
       if process.returncode != 0:
           print("ERROR occured during running ", params)
           break

   return 0

if __name__ == '__main__':
   sys.exit(main(sys.argv) )
