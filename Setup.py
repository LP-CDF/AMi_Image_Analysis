#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 10:50:12 2020

@author: ludovic
"""

__date__ = "04-08-2022"

import os
import os.path
from pathlib import Path
from subprocess import Popen, PIPE
import sys
from threading import Thread
import urllib.parse
import urllib.request
import venv

#Minimal python version compatible with https://bootstrap.pypa.io/get-pip.py
this_python = sys.version_info[:2]
min_version = (3, 7)    #Need to be checked in file
                        #https://bootstrap.pypa.io/get-pip.py
                        #if error "python: No module named pip"

class ExtendedEnvBuilder(venv.EnvBuilder):
    """
    This builder installs pip so that you can pip install other packages
    into the created virtual environment.
    
    :param nodist: If true, setuptools and pip are not installed into the
                   created virtual environment.
    :param nopip: If true, pip is not installed into the created
                  virtual environment.
    :param progress: If pip is installed, the progress of the
                     installation can be monitored by passing a progress
                     callable. If specified, it is called with two
                     arguments: a string indicating some progress, and a
                     context indicating where the string is coming from.
                     The context argument can have one of three values:
                     'main', indicating that it is called from virtualize()
                     itself, and 'stdout' and 'stderr', which are obtained
                     by reading lines from the output streams of a subprocess
                     which is used to install the app.

                     If a callable is not specified, default progress
                     information is output to sys.stderr.
    """

    def __init__(self, *args, **kwargs):
        self.nodist = kwargs.pop('nodist', False)
        self.nopip = kwargs.pop('nopip', False)
        self.progress = kwargs.pop('progress', None)
        self.verbose = kwargs.pop('verbose', False)
        self.noprojectID = kwargs.pop('noprojectID', False)
        self.layoutFR=kwargs.pop('layoutFR', False)
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        """
        Set up any packages which need to be pre-installed into the
        virtual environment being created.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        os.environ['VIRTUAL_ENV'] = context.env_dir

        #setuptools not required to install pip
        if not self.nopip:
            self.install_pip(context)

        self.install_dep(context)

    def reader(self, stream, context):
        """
        Read lines from a subprocess' output stream and either pass to a progress
        callable (if specified) or write progress information to sys.stderr.
        """
        progress = self.progress
        while True:
            s = stream.readline()
            if not s:
                break
            if progress is not None:
                progress(s, context)
            else:
                if not self.verbose:
                    sys.stderr.write('.')
                else:
                    sys.stderr.write(s.decode('utf-8'))
                sys.stderr.flush()
        stream.close()

    def install_script(self, context, name, fn, binpath, distpath):
        progress = self.progress
        if self.verbose:
            term = '\n'
        else:
            term = ''
        if progress is not None:
            progress('Installing %s ...%s' % (name, term), 'main')
        else:
            sys.stderr.write('Installing %s ...%s' % (name, term))
            sys.stderr.flush()
        # Install in the virtual environment
        args = [context.env_exe, fn]
        p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=binpath)
        t1 = Thread(target=self.reader, args=(p.stdout, 'stdout'))
        t1.start()
        t2 = Thread(target=self.reader, args=(p.stderr, 'stderr'))
        t2.start()
        p.wait()
        t1.join()
        t2.join()
        if progress is not None:
            progress('done.', 'main')
        else:
            sys.stderr.write('done.\n')
        # Clean up - no longer needed
        os.unlink(distpath)

    @staticmethod
    def url_pip():
        global this_python,min_version
        ''' return location of downloaded file'''
        if this_python < min_version:
            url = 'https://bootstrap.pypa.io/pip/{}.{}/get-pip.py'.format(*this_python)
        else:
            url = 'https://bootstrap.pypa.io/get-pip.py'
        return url
    
    def download_pip(self,context,url, path):
        ''''Download script into the virtual environment's binaries folder'''
        urllib.request.urlretrieve(url, path)

    @staticmethod
    def get_pip_compat(path):
        '''read pip script and return a tuple of min_version'''
        with open(path) as f:
            _lines=f.readlines()
        for i in _lines:
            if "min_version" in i:
                comp = i.split('=')[1]
                comp = tuple(int(ele) for ele in comp.replace('(', '').replace(')', '').split(', '))
                break
        print(f"Python min_version= {comp} for compatibility in {path}" )
        return comp

    @staticmethod
    def check_getpip_compat(compatibility):
        global this_python
        if this_python < compatibility:
            print(f'''Python {this_python} too old for this version
                  of get-pip.py
                  min_version = {str(compatibility)}
                  ''')
        else:
            print("Everything seems in order, continuing installation...")
        return bool(this_python < compatibility)

    def install_pip(self, context):
        global this_python,min_version
        """
        Install pip in the virtual environment.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
            
        url=self.url_pip()
        _, _, path, _, _, _ = urllib.parse.urlparse(url)
        fn = os.path.split(path)[-1]
        binpath = context.bin_path
        distpath = os.path.join(binpath, fn)
        
        self.download_pip(context,url, distpath)
        compat=self.get_pip_compat(distpath)
        if self.check_getpip_compat(compat) is True:
            os.unlink(distpath)
            min_version=compat
            print("Trying to update the installation script...")
            url=self.url_pip()
            _, _, path, _, _, _ = urllib.parse.urlparse(url)
            fn = os.path.split(path)[-1]
            binpath = context.bin_path
            distpath = os.path.join(binpath, fn)            
            self.download_pip(context,url, distpath)
            compat=self.get_pip_compat(distpath)
            self.check_getpip_compat(compat)
            self.install_script(context, 'pip', fn, binpath, distpath)
        else:
            self.install_script(context, 'pip', fn, binpath, distpath)
            
    def install_dep(self, context):
        try:
            import subprocess
        except:
            print("subprocess not found exiting")
            sys.exit()
        try:
            import platform
        except:
            print("platform not found exiting")
            sys.exit()

        _list = {'linux': "requirements.txt",
                 'darwin': "requirements_OSX.txt",
                 'win32': "requirements.txt",
                 'armv7l': "requirements_Raspbian.txt"}

        filepath = os.path.abspath(os.path.dirname(sys.argv[0]))
        # print('FILEPATH : ', filepath)
        if sys.platform == 'linux' and platform.machine() == "armv7l":
            deppath = Path(filepath).joinpath(_list['armv7l'])
        else:
            deppath = Path(filepath).joinpath(_list[sys.platform])
        print('WILL INSTALL packages from : ', deppath)
        with open(deppath, 'r') as f:
            lines = f.read().splitlines()
        # print("LINES", lines)

        binpath = Path(context.bin_path).joinpath("python")
        print("PYTHONPATH: ", binpath)
        for dep in lines:
            subprocess.call([binpath, '-m', 'pip', 'install',
                             "--prefix", context.env_dir, dep])

        #Finishing setup
        if sys.platform == 'linux' or sys.platform == 'darwin':
            print("\nUPDATING INTIALISATION SCRIPT bin/AMI_Image_Analysis.sh\n")
            Setup_bin_VENV = Path(filepath).joinpath("Setup_local.py")
            if self.noprojectID is True and self.layoutFR is False:
                subprocess.run([binpath, Setup_bin_VENV, "--no-ProjectID"])
            elif self.noprojectID is False and self.layoutFR is True:
                subprocess.run([binpath, Setup_bin_VENV, "--FR"])
            elif self.noprojectID is True and self.layoutFR is True:
                subprocess.run([binpath, Setup_bin_VENV,
                                "--no-ProjectID",
                                "--FR"])    
            else:
                subprocess.run([binpath, Setup_bin_VENV])


def main(args=None):
    script_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    print(f"Setup.py path is {script_path}")
    temp = Path(script_path).parent

    #Setup ENV_DIR if no destination given.
    ENV_DIR = temp.joinpath(
        "python", "venvs", "AMI_IMAGE_ANALYSIS_TENSORFLOW1")
    root = ENV_DIR.parent

    compatible = True
    if sys.version_info < (3, 6):
        compatible = False
    elif not hasattr(sys, 'base_prefix'):
        compatible = False
    if not compatible:
        raise ValueError('This script is only for use with '
                         'Python 3.6 or later')
    else:
        import argparse

        parser = argparse.ArgumentParser(prog=__name__,
                                         description='Creates virtual Python '
                                                     'environments in one or '
                                                     'more target '
                                                     'directories.')
        parser.add_argument('dirs', metavar='ENV_DIR', nargs='?',
                            help='A directory in which to create the'
                            'virtual environment.')
        parser.add_argument('--no-setuptools', default=False,
                            action='store_true', dest='nodist',
                            help="Don't install setuptools or pip in the "
                                 "virtual environment.")
        parser.add_argument('--no-pip', default=False,
                            action='store_true', dest='nopip',
                            help="Don't install pip in the virtual "
                                 "environment.")
        parser.add_argument('--system-site-packages', default=False,
                            action='store_true', dest='system_site',
                            help='Give the virtual environment access to the '
                                 'system site-packages dir.')
        if os.name == 'nt':
            use_symlinks = False
        else:
            use_symlinks = True
        parser.add_argument('--symlinks', default=use_symlinks,
                            action='store_true', dest='symlinks',
                            help='Try to use symlinks rather than copies, '
                                 'when symlinks are not the default for '
                                 'the platform.')
        parser.add_argument('--clear', default=False, action='store_true',
                            dest='clear', help='Delete the contents of the '
                                               'virtual environment '
                                               'directory if it already '
                                               'exists, before virtual '
                                               'environment creation.')
        parser.add_argument('--upgrade', default=False, action='store_true',
                            dest='upgrade', help='Upgrade the virtual '
                                                 'environment directory to '
                                                 'use this version of '
                                                 'Python, assuming Python '
                                                 'has been upgraded '
                                                 'in-place.')
        parser.add_argument('--verbose', default=False, action='store_true',
                            dest='verbose', help='Display the output '
                            'from the scripts which '
                            'install pip.')
        parser.add_argument('--no-ProjectID', default=False,
                            action='store_true', dest='noprojectID',
                            help="Don't use ProjectID in tree")
        parser.add_argument('--FR', default=False,
                            action='store_true', dest='layoutFR',
                            help="set keyboard to AZERTY") 

        options = parser.parse_args(args)

        if options.upgrade and options.clear:
            raise ValueError(
                'you cannot supply --upgrade and --clear together.')
        builder = ExtendedEnvBuilder(system_site_packages=options.system_site,
                                     clear=options.clear,
                                     symlinks=options.symlinks,
                                     upgrade=options.upgrade,
                                     nodist=options.nodist,
                                     nopip=options.nopip,
                                     verbose=options.verbose,
                                     noprojectID=options.noprojectID,
                                     layoutFR=options.layoutFR)

        if options.dirs is None:
            options.dirs = str(ENV_DIR)
            if not root.parent.exists():
                root.parent.mkdir()
            if not root.exists():
                root.mkdir()
            if not ENV_DIR.exists():
                ENV_DIR.mkdir()

        print(f"Will install venv in {options.dirs}")
        builder.create(options.dirs)


if __name__ == '__main__':
    RC = 1
    if sys.version >= '3.8':
        print(f'''
#########################################################################################################   
           
              WARNING:
              Python version {sys.version} is more recent than the recommended version.
              You may encounter setup issues.
              If you don't want to use Tensorflow, this should be fine.
              
#########################################################################################################            
              ''')
        #Ask to STOP installation if python >= 3.8 (need <= 3.7.x for MARCO TF model)
        val1=input("Do you want to proceed ? (Y(es) or N(o)) :")
        if val1.lower() not in ['y', 'yes']:
            print("Aborting \n")
            sys.exit(RC)        
    try:
        main()
        RC = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(RC)
