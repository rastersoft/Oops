#! /usr/bin/env python3

"""
Oops - Oops is to support others

Oops is a utility to facilitate the connection of VNC

Based on Gitso, from Aaron Gerber and Derek Buranen, @copyright: 2008 - 2010

Oops is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Oops is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Oops.  If not, see <http://www.gnu.org/licenses/>.
"""

import os, sys, signal, os.path, re
import subprocess
import time
from gettext import gettext as _

class Processes:
	def __init__(self, paths):
		self.returnPID = None
		self.paths = paths
		self.process = None


	def getSupport(self, host):
		if sys.platform == 'darwin':
			self.process = subprocess.Popen([os.path.join(self.paths['resources'],'OSXvnc/OSXvnc-server'), '-connectHost', host])

		elif re.match('(?:open|free|net)bsd|linux',sys.platform):
			# We should include future versions with options for speed.
			#self.returnPID = os.spawnlp(os.P_NOWAIT, 'x11vnc', 'x11vnc','-nopw','-ncache','20','-solid','black','-connect','%s' % host)
			
			self.process = subprocess.Popen(['x11vnc','-nopw','-ncache','20','-connect_or_exit', host])
			
			# Added for OpenBSD compatibility
		elif sys.platform == 'win32':
			self.process = subprocess.Popen(['WinVNC.exe'])
			print(_("Launched WinVNC.exe, waiting to run -connect command..."))
			time.sleep(2)
			if self.paths['mode'] == 'dev':
				subprocess.Popen(['%sWinVNC.exe' % self.paths['resources'], '-connect', '%s' % host])
			else:
				subprocess.Popen(['WinVNC.exe', '-connect', '%s' % host])
		else:
			print(_('Platform not detected'))
		self.returnPID = self.process.pid
		return self.returnPID


	def giveSupport(self):
		if sys.platform == 'darwin':
			vncviewer = '%scotvnc.app/Contents/MacOS/cotvnc' % self.paths['resources']
			self.process = subprocess.Popen([vncviewer, '--listen'])
		elif re.match('(?:open|free|net)bsd|linux',sys.platform):
			
			# These are the options for low-res connections.
			# In the future, I'd like to support cross-platform low-res options.
			# What aboot a checkbox in the gui
			if self.paths['low-colors'] == False:
				self.process = subprocess.Popen(['vncviewer', '-listen'])
			else:
				self.process = subprocess.Popen(['vncviewer', '-bgr233', '-listen'])
		elif sys.platform == 'win32':
			if self.paths['mode'] == 'dev':
				self.process = subprocess.Popen(['%svncviewer.exe' % self.paths['resources'], '-listen'])
			else:
				self.process = subprocess.Popen(['vncviewer.exe', '-listen'])
		else:
			print(_('Platform not detected'))
		self.returnPID = self.process.pid
		return self.returnPID

	def isrunning(self):
		
		if self.process.poll() == None:
			return True
		else:
			return False


	def KillPID(self):
		"""	Kill VNC instance, called by the Stop Button or Application ends. """
		if self.returnPID is not None:
			print(_("Processes.KillPID(%s)") % str(self.returnPID))
			if sys.platform == 'win32':
				import win32api
				PROCESS_TERMINATE = 1
				handle = win32api.OpenProcess(PROCESS_TERMINATE, False, self.returnPID)
				win32api.TerminateProcess(handle, -1)
				win32api.CloseHandle(handle)
			elif re.match('(?:open|free|net)bsd|linux',sys.platform):
				# New processes are created when you made connections. So if you kill self.returnPID,
				# you're just killing the dispatch process, not the one actually doing business...
				os.spawnlp(os.P_NOWAIT, 'pkill', 'pkill', '-f', 'vncviewer')
				os.spawnlp(os.P_NOWAIT, 'pkill', 'pkill', '-f', 'x11vnc')
			else:
				os.kill(self.returnPID, signal.SIGKILL)
			try:
				os.waitpid(self.returnPID, 0)
			except:
				pass
			self.returnPID = None
		return
