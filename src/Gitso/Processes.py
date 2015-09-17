#! /usr/bin/env python

"""
Gisto - Gitso is to support others

Gitso is a utility to facilitate the connection of VNC

@author: Aaron Gerber ('gerberad') <gerberad@gmail.com>
@author: Derek Buranen ('burner') <derek@buranen.info>
@copyright: 2008 - 2010

Gitso is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Gitso is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Gitso.  If not, see <http://www.gnu.org/licenses/>.
"""

import wx
import os, sys, signal, os.path, re
import subprocess
import time
from gettext import gettext as _

class Processes:
	def __init__(self, paths):
		self.returnPID = 0
		self.paths = paths


	def getSupport(self, host):
		if sys.platform == 'darwin':
			self.returnPID = subprocess.Popen([os.path.join(self.paths['resources'],'OSXvnc/OSXvnc-server'), '-connectHost', host]).pid

		elif re.match('(?:open|free|net)bsd|linux',sys.platform):
			# We should include future versions with options for speed.
			#self.returnPID = os.spawnlp(os.P_NOWAIT, 'x11vnc', 'x11vnc','-nopw','-ncache','20','-solid','black','-connect','%s' % host)
			
			self.returnPID = subprocess.Popen(['x11vnc','-nopw','-ncache','20','-connect_or_exit', host]).pid
			
			# Added for OpenBSD compatibility
		elif sys.platform == 'win32':
			self.returnPID = subprocess.Popen(['WinVNC.exe']).pid
			print _("Launched WinVNC.exe, waiting to run -connect command...")
			time.sleep(2)
			if self.paths['mode'] == 'dev':
				subprocess.Popen(['%sWinVNC.exe' % self.paths['resources'], '-connect', '%s' % host])
			else:
				subprocess.Popen(['WinVNC.exe', '-connect', '%s' % host])
		else:
			print _('Platform not detected')
		return self.returnPID


	def giveSupport(self):
		if sys.platform == 'darwin':
			vncviewer = '%scotvnc.app/Contents/MacOS/cotvnc' % self.paths['resources']
			self.returnPID = subprocess.Popen([vncviewer, '--listen']).pid
		elif re.match('(?:open|free|net)bsd|linux',sys.platform):
			
			# These are the options for low-res connections.
			# In the future, I'd like to support cross-platform low-res options.
			# What aboot a checkbox in the gui
			if self.paths['low-colors'] == False:
				self.returnPID = subprocess.Popen(['vncviewer', '-listen']).pid
			else:
				self.returnPID = subprocess.Popen(['vncviewer', '-bgr233', '-listen']).pid
		elif sys.platform == 'win32':
			if self.paths['mode'] == 'dev':
				self.returnPID = subprocess.Popen(['%svncviewer.exe' % self.paths['resources'], '-listen']).pid
			else:
				self.returnPID = subprocess.Popen(['vncviewer.exe', '-listen']).pid
		else:
			print _('Platform not detected')
		return self.returnPID


	def KillPID(self):
		"""
		Kill VNC instance, called by the Stop Button or Application ends.
		
		@author: Derek Buranen
		@author: Aaron Gerber
		"""
		if self.returnPID != 0:
			print _("Processes.KillPID(%s)") % str(self.returnPID)
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
			self.returnPID = 0
		return

