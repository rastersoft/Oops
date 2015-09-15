#Gitso

Gitso is a frontend to reverse VNC connections. It is meant to be a simple two-step process that connects one person to another's screen.

Original Project is kept at: https://code.google.com/p/gitso/

Few changes made by AustP:

+ Minimization now minimizes to the task tray
+ When using the command line switch --listen, Gitso starts minimized

Changes made by Rastersoft:

+ Internationalization and localization support
+ Fixed the interface in Linux (some elements where put outside the window)

##Building Gitso
####Windows
In the src folder you will find instructions on how to build Gitso on Windows along with installation files.
**You may have to change some paths in *makegitso.bat*** depending on your installation.

####Mac
These instructions have been taken from https://code.google.com/p/gitso/wiki/BuildOSX

1. Install Developer Tools (Xcode) from the OS X System CD
2. Install py2app
3. From the command line type:
4. curl -O http://peak.telecommunity.com/dist/ez_setup.py
5. sudo python ez_setup.py -U setuptools
6. sudo easy_install -U py2app
7. Update hosts.txt to have preset options for the client. Hosts are comma separated and optional.
8. Run: ./makegitso.sh

####Linux
These instructions have been taken from https://code.google.com/p/gitso/wiki/BuildLinux

**Non Ubuntu, Fedora, and OpenSUSE Users**
 
Gitso requires the following files so make sure to install them:

+ x11vnc
+ vncviewer
+ wxPython

**Fedora Users**

1. yum install subversion
2. yum install rpmdevtools

**Debian/Ubuntu packages**

Install *python-stdeb* to allow pysetup to create DEB packages, and run *makegitso_debian.sh*.

##Disclaimer
Gitso is NOT my project, but other's. I'm creating a fork, but still don't have a name for it.
