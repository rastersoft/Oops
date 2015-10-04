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
import os, sys, signal, os.path, time, thread, re
import Gitso.AboutWindow
import Gitso.Processes

from gettext import gettext as _


if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
	import NATPMP


class GitsoTaskBarIcon(wx.TaskBarIcon):
	def __init__(self, icon, frame):
		wx.TaskBarIcon.__init__(self)
		self.SetIcon(icon, "Gitso")
		self.frame = frame
		
	def CreatePopupMenu(self):
		self.menu = wx.Menu()
		self.menu.Append(20, _("Restore Gitso"))
		self.menu.Append(21, _("Quit Gitso"))
		wx.EVT_MENU(self.menu, 20, self.frame.RestoreWindow)
		wx.EVT_MENU(self.menu, 21, self.frame.OnCloseWindow)
		return self.menu

class ConnectionWindow(wx.Frame):
	"""
	Main Window for Gitso
	
	@author: Derek Buranen
	@author: Aaron Gerber
	"""
	def __init__(self, parent, id, title, paths):
		"""
		Setup Application Window
		
		@author: Derek Buranen
		@author: Aaron Gerber
		@author: Markus Roth
		"""
		self.ToggleValue = 0
		self.paths = paths
		self.process = Gitso.Processes.Processes(paths)
		
		# Disable until 0.7 release
		self.enablePMP = False

		#if re.match('(?:open|free|net)bsd|linux',sys.platform):
		wsize = (350,260)
		xval1 = 155
		xval2 = 250
# 		else:
# 			wsize = (350,175)
# 			xval1 = 180
# 			xval2 = 265

		wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=wsize, style=wx.DEFAULT_FRAME_STYLE & ~(wx.FRAME_SHAPED | wx.RESIZE_BORDER | wx.RESIZE_BOX | wx.MAXIMIZE_BOX))
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		self.Bind(wx.EVT_ICONIZE, self.OnIconizeWindow)
		
		icon = wx.Icon(os.path.join(self.paths['main'], 'gitso.ico'), wx.BITMAP_TYPE_ICO)
		if sys.platform == 'win32':
			self.SetBackgroundColour(wx.Colour(236,233,216))

		self.SetIcon(icon)
		self.TrayIcon = GitsoTaskBarIcon(icon, self)
		wx.EVT_TASKBAR_LEFT_UP(self.TrayIcon, self.RestoreWindow)
		
		#Buttons
		self.connectButton = wx.Button(self, 10, _("Start"), wx.Point(xval1, 144))
		self.connectButton.SetDefault()
		wx.EVT_BUTTON(self, 10, self.ConnectSupport)
		self.stopButton = wx.Button(self, wx.ID_STOP, "", wx.Point(xval2, 144))
		self.stopButton.Enable(False)
		wx.EVT_BUTTON(self, wx.ID_STOP, self.KillPID)
		
		# Radio Boxes
		self.rb1 = wx.RadioButton(self, -1, _('Get Help'), (10, 15), style=wx.RB_GROUP)
		self.rb2 = wx.RadioButton(self, -1, _('Give Support'), (10, 80))
		self.rb1.SetValue(True)
		
		self.Bind(wx.EVT_RADIOBUTTON, self.RadioToggle, id=self.rb1.GetId())
		self.Bind(wx.EVT_RADIOBUTTON, self.RadioToggle, id=self.rb2.GetId())
		
		# checkbox for natpmp
		if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
			if self.enablePMP:
				self.cb1 = wx.CheckBox(self, -1, _('Use NAT-PMP'), (130, 48))
				self.cb1.Enable(False)

		# Checkbox for low color
		self.cb2 = wx.CheckBox(self, -1, _('Use low colors'), (40, 104))
		self.cb2.Set3StateValue(False)
		self.cb2.SetValue(self.paths['low-colors']) # Use value of --low-colors from command line
		self.cb2.Enable(False)
		
		# the combobox Control
		self.sampleList = self.paths['list']
		
		self.sampleList = self.getHosts(self.sampleList, os.path.join(self.paths['main'], 'hosts.txt'))
		self.sampleList = self.getHosts(self.sampleList, self.paths['preferences'])
		self.displayHostBox(self.sampleList, _("Enter/Select Support Address"))
		self.delete_entry = False
		
		# Menu      
		menuBar = wx.MenuBar()
		fileMenu = wx.Menu()
		
		editMenu = wx.Menu()
		editMenu.Append(11, _("&Cut\tCtrl+X"), _("Cut IP Address"))
		editMenu.Append(12, _("&Copy\tCtrl+C"), _("Copy IP Address"))
		editMenu.Append(wx.ID_PASTE, _("&Paste\tCtrl+V"), _("Paste IP Address"))
		wx.EVT_MENU(self, 11, self.SetClipboard)
		wx.EVT_MENU(self, 12, self.SetClipboard)
		wx.EVT_MENU(self, wx.ID_PASTE, self.GetClipboard)
		
		fileMenu.Append(13, _("&Clear History"), _("Clear History"))
		if sys.platform == 'darwin':
			fileMenu.Append(wx.ID_ABOUT, _("&About"), _("About Gitso"))
			wx.EVT_MENU(self, wx.ID_ABOUT, self.ShowAbout)
		else:       
			fileMenu.Append(wx.ID_EXIT, _("&Quit\tCtrl+Q"), _("Quit Gitso"))
			wx.EVT_MENU(self, wx.ID_EXIT, self.OnCloseWindow)
		
		helpMenu = wx.Menu()
		helpMenu.Append(wx.ID_ABOUT, _("&About"), _("About Gitso"))
		wx.EVT_MENU(self, wx.ID_ABOUT, self.ShowAbout)
		
		wx.EVT_MENU(self, 13, self.clearHistory)
		
		menuBar.Append(fileMenu, _("&File"))
		menuBar.Append(editMenu, _("&Edit"))
		
		if re.match('(?:open|free|net)bsd|linux',sys.platform) or sys.platform == 'win32':
			menuBar.Append(helpMenu, _("&Help"))
		
		self.SetMenuBar(menuBar)
		
		self.statusBar = self.CreateStatusBar()
		self.statusBar.SetStatusWidths([350])
		self.setMessage(_("Idle"), False)
		
		self.SetDefaultItem(self.hostField)
		#self.hostField.SetFocus()
		
		self.SetThemeEnabled(True)
		self.Centre()
		self.Show(True)
		
		if self.paths['listen']:
			self.Iconize(True)
			self.rb2.Value = True
			self.RadioToggle(None)
			self.ConnectSupport(None)
		elif self.paths['connect'] != "":
			self.rb1.Value = True
			self.RadioToggle(None)
			self.hostField.Value = self.paths['connect']
			self.ConnectSupport(None)


	def RadioToggle(self, event):
		"""
		Toggles Radio Buttons
		
		@author: Derek Buranen
		@author: Aaron Gerber
		@author: Markus Roth
		"""
		if self.rb1.GetValue():
			self.ToggleValue = 0
			self.hostField.Enable(True)
			self.cb2.Enable(False)
			if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
				if self.enablePMP:
					self.cb1.Enable(False)
		else:
			self.ToggleValue = 1
			self.hostField.Enable(False)
			self.cb2.Enable(True)
			if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
				if self.enablePMP:
					self.cb1.Enable(True)


	def ConnectSupport(self, event):
		"""
		Call VNC in a thread.
		
		@author: Derek Buranen
		@author: Aaron Gerber
		"""
		if self.rb1.GetValue(): # Get Help
			if self.validHost(self.hostField.GetValue().strip()) and self.hostField.GetValue() != _("Enter/Select Support Address"):
				self.setMessage(_("Connecting..."), True)
				
				host = self.hostField.GetValue().strip()
				
				self.sampleList = []
				self.sampleList = self.getHosts(self.sampleList, os.path.join(self.paths['main'], 'hosts.txt'))
				self.sampleList = self.getHosts(self.sampleList, self.paths['preferences'])
				
				if self.sampleList.count(host) == 0:
					self.saveHost(self.paths['preferences'], host)
					self.sampleList.append(host)
					self.hostField.Destroy()
					self.displayHostBox(self.sampleList, host)
				self.createThread(host)
			else:
				self.setMessage(_("Invalid Support Address"), False)
		else: # Give Suppport
			self.setMessage(_("Starting Server..."), True)
			self.createThread()


	def ShowAbout(self,e):
		"""
		Display About Dialog
		
		@author: Derek Buranen
		@author: Aaron Gerber
		"""
		about = Gitso.AboutWindow.AboutWindow(self, wx.ID_ABOUT, _("About Gitso"), self.paths)
	
	
	def clearHistory(self, event):
		handle = open(self.paths['preferences'], 'w')
		handle.write("")
		handle.close()
		
		text = self.hostField.GetValue()
		self.hostField.Destroy()

		self.sampleList = []
		self.sampleList = self.getHosts(self.sampleList, os.path.join(self.paths['main'], 'hosts.txt'))
		self.sampleList = self.getHosts(self.sampleList, self.paths['preferences'])

		self.displayHostBox(self.sampleList, text)
	
	
	def GetClipboard(self, menu, data=None):
		"""
		Paste clipboard text in Support Entry Field
		
		@author: Derek Buranen
		@author: Aaron Gerber
		"""
		do = wx.TextDataObject()
		wx.TheClipboard.Open()
		clip = wx.TheClipboard.GetData(do)
		wx.TheClipboard.Close()
		
		if clip:
			self.hostField.SetValue(do.GetText())
	
	
	def SetClipboard(self, menu, data=None):
		"""
		Set the value of the clipboard
		
		@author: Derek Buranen
		@author: Aaron Gerber
		"""
		self.clipdata = wx.TextDataObject()
		self.clipdata.SetText(self.hostField.GetValue())
		wx.TheClipboard.Open()
		wx.TheClipboard.SetData(self.clipdata)
		wx.TheClipboard.Close()
		if menu.GetId() == 11:
			self.hostField.SetValue("")
	
	
	def KillPID(self, showMessage=True):
		"""
		Kill VNC instance, called by the Stop Button or Application ends.
		
		@author: Derek Buranen
		@author: Aaron Gerber
		"""

		self.process.KillPID()
			# If you don't wait 0.5+ seconds, the interface won't reload and it'll freeze.
			# Possibly on older systems you should wait longer, it works fine on mine...
		if showMessage :
			self.setMessage(_("Idle"), False)
		return


	def OnCloseWindow(self, evt):

		self.KillPID()
		self.Destroy()
		sys.exit(0)
	
	def OnIconizeWindow(self, evt):
		self.Hide()
	
	def RestoreWindow(self, evt):
		if self.IsIconized():
			self.Iconize(False)
			if not self.IsShown():
				self.Show(True)
				self.Raise()
	
	def validHost(self, host):
		if host != "" and host.find(";") == -1 and host.find("/") == -1 and host.find("'") == -1 and host.find("`") == -1 and len(host) > 6:
			return True
		else:
			return False
	
	
	def getHosts(self, arr, file):
		list = arr
		if os.path.exists(file):
			handle = open(file, 'r')
			fileList = handle.read()
			parsedlist = fileList.split(",")
			for i in range(0, len(parsedlist)):
				if self.validHost(parsedlist[i].strip()):
					list.append(parsedlist[i].strip())
			handle.close()
		return list
	
	
	def saveHost(self, file, host):
		if os.path.exists(file):
			handle = open(file, 'a')
			handle.write(", %s" % host)
			handle.close()


	def delete_text_on_focus(self,evt):
		if self.hostField.HasFocus():
			if self.delete_entry == False:
				self.hostField.SetValue("")
				self.delete_entry = True


	def displayHostBox(self, list, text):

		self.hostField = wx.ComboBox(self, 30, "", wx.Point(40, 40), wx.Size(300, -1), list, wx.CB_DROPDOWN)
		self.hostField.SetValue(text)
		self.hostField.Bind(wx.EVT_SET_FOCUS,self.delete_text_on_focus)

	def setMessage(self, message, status):

		self.statusBar.SetStatusText(message, 0)

		if status:
			self.connectButton.Enable(False)
			self.stopButton.Enable(True)
		else:
			self.connectButton.Enable(True)
			self.stopButton.Enable(False)

		
		if self.ToggleValue == 0:
			self.rb1.SetValue(True)
		else:
			self.rb2.SetValue(True)
		

	def check_wm(self,event):

		if self.process.returnPID == 0:
			self.timer.Stop()
			self.timer = None
			return
		try:
			os.waitpid(-1, os.WNOHANG)
			retval = False
		except:
			retval = True

		if not wx.Process.Exists(self.process.returnPID):
			self.process.KillPID()
			self.setMessage(_("Idle"), False)
			self.timer.Stop()
			self.timer = None


	def NATPMP(self, action):
		"""
		Call NAT-PMP on router to get port 5500 forwarded.

		@author: Dennis Koot
		"""
		if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
			if self.enablePMP:
				if action == 'request':
					lifetime = 3600
					print "Request port 5500 (NAT-PMP)."
				else:
					lifetime = 0
					print "Give up port 5500 (NAT-PMP)."

				pubpriv_port = int(5500)
				protocol = NATPMP.NATPMP_PROTOCOL_TCP

				try:
					gateway = NATPMP.get_gateway_addr()
					print NATPMP.map_port(protocol, pubpriv_port, pubpriv_port, lifetime, gateway_ip=gateway)
				except:
					print "Warning: Unable to automap port."



	def createThread(self, host=""):

		self.paths['low-colors'] = self.cb2.GetValue() # Set low-colors to value of checkbox

		self.KillPID(False)
		if host != "":
			# Get Help
			self.process.getSupport(host)
			self.setMessage(_("Connected."), True)
		else:
			# Give Support
			if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
				if self.enablePMP:
					self.cb1.Enable(False)
					if self.cb1.GetValue() == True:
						self.NATPMP('request')

			self.process.giveSupport()
			self.setMessage(_("Server running."), True)

		print _("GitsoThread.run(pid: %s) running...") % str(self.process.returnPID)
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.check_wm, self.timer)
		self.timer.Start(500,False)
