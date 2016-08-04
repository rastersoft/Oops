#RemoteH

RemoteH is a frontend for reverse VNC connections. It is meant to be a simple two-step process that connects one person to another's screen.

It is based on Gitso. The original project is kept at: https://code.google.com/p/gitso/

The main changes are:

+ Internationalization and localization support
+ Changed the interface from wxWidgets to TkInter, which also fixed the interface in Linux (some elements where put outside the window)
+ Now deletes the text in the address entry when the user clicks on it

##Building RemoteH
####Windows
In the src folder you will find instructions on how to build RemoteH on Windows along with installation files.
**You may have to change some paths in *makeremoteh.bat*** depending on your installation.

####Mac
These instructions have been taken from https://code.google.com/p/gitso/wiki/BuildOSX

1. Install Developer Tools (Xcode) from the OS X System CD
2. Install py2app
3. From the command line type:
4. curl -O http://peak.telecommunity.com/dist/ez_setup.py
5. sudo python ez_setup.py -U setuptools
6. sudo easy_install -U py2app
7. Update hosts.txt to have preset options for the client. Hosts are comma separated and optional.
8. Run: ./makeremoteh.sh

####Linux
These instructions have been taken from https://code.google.com/p/gitso/wiki/BuildLinux

**Non Ubuntu, Fedora, and OpenSUSE Users**
 
RemoteH requires the following files so make sure to install them:

+ x11vnc
+ vncviewer

**Fedora Users**

1. yum install subversion
2. yum install rpmdevtools

**Debian/Ubuntu packages**

Install *python-stdeb* to allow pysetup to create DEB packages, and run *makeremoteh_debian.sh*.
