#! /usr/bin/env python3

"""
RemoteH - RemoteH is to support others

Copyright 2016 Raster Software Vigo

RemoteH is a utility to facilitate the connection of VNC

Based on Gitso, from Aaron Gerber and Derek Buranen, @copyright: 2008 - 2010

RemoteH is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RemoteH is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with RemoteH.  If not, see <http://www.gnu.org/licenses/>.
"""

import tkinter
import os, sys, signal, os.path, time, re
import RemoteH.AboutWindow
import RemoteH.Processes

from gettext import gettext as _


if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
	import RemoteH.NATPMP


class ConnectionWindow(object):
	"""	Main Window for RemoteH """
	def __init__(self, paths):
		"""	Setup Application Window """

		self.paths = paths
		self.process = RemoteH.Processes.Processes(paths)
		
		# Disable until 0.7 release
		self.enablePMP = False

		self.app = tkinter.Tk()
		self.app.minsize(width = 320, height = 100)
		self.app.wm_title("RemoteH")
		self.app.iconphoto(True, tkinter.PhotoImage(file=os.path.join(paths['main'],'remoteh.png')))
		
		self.opcion = tkinter.IntVar()
		self.lowcolor = tkinter.IntVar()
		self.address = tkinter.StringVar()
		self.status = tkinter.StringVar()

		self.menu = tkinter.Menu(self.app)
		filemenu = tkinter.Menu(self.menu, tearoff = 0)
		filemenu.add_command(label=_("Exit"), command = self.app.quit)
		self.menu.add_cascade(label=_("File"), menu = filemenu)
		
		editmenu = tkinter.Menu(self.menu, tearoff = 0)
		editmenu.add_command(label=_("Cut"))
		editmenu.add_command(label=_("Copy"))
		editmenu.add_command(label=_("Paste"))
		self.menu.add_cascade(label=_("Edit"), menu = editmenu)
		
		aboutmenu = tkinter.Menu(self.menu, tearoff = 0)
		aboutmenu.add_command(label=_("About"), command = self.about)
		self.menu.add_cascade(label=_("Help"), menu = aboutmenu)
		
		self.app.config(menu=self.menu)

		# Radio Boxes
		self.rb_gethelp = tkinter.Radiobutton(self.app, text = _('Get Help'), value = 0, variable = self.opcion, anchor = tkinter.W, command = self.optionChanged)
		self.rb_givesupport = tkinter.Radiobutton(self.app, text = _('Give Support'), value = 1, variable = self.opcion, anchor = tkinter.W, command = self.optionChanged)
		self.opcion.set(0)

		self.cb_lowcolors = tkinter.Checkbutton(self.app,text = _('Use low colors'), variable = self.lowcolor, onvalue = 1, offvalue = 0, anchor = tkinter.W)

		self.displayHostBox = tkinter.Entry(self.app, textvariable = self.address)
		self.displayHostBox.bind('<Return>', self.ConnectSupport)
		#self.sampleList,
		self.address.set(_("Enter/Select Support Address"))
		self.delete_entry = True
		self.displayHostBox.bind("<FocusIn>",self.delete_entry_cb)

		self.rb_gethelp.pack(side = tkinter.TOP, fill = tkinter.X)
		self.displayHostBox.pack(side = tkinter.TOP, fill = tkinter.X, padx = (20,0))
		self.rb_givesupport.pack(side = tkinter.TOP, fill = tkinter.X)
		self.cb_lowcolors.pack(side = tkinter.TOP, fill = tkinter.X, padx = (20,0))

		container1 = tkinter.Frame(self.app, relief = tkinter.RAISED, borderwidth = 2)
		container1.pack(side = tkinter.BOTTOM, fill = tkinter.X)
		self.statusbar = tkinter.Label(container1, textvariable = self.status, justify = tkinter.LEFT)
		self.statusbar.pack(side = tkinter.LEFT, fill = tkinter.X)

		contenedor = tkinter.Frame(self.app)
		contenedor.pack(side = tkinter.BOTTOM, fill = tkinter.X)

		#Buttons
		self.connectButton = tkinter.Button(contenedor, text = _("Start"), command = self.ConnectSupport)
		self.stopButton = tkinter.Button(contenedor, text = _("Stop"), command = self.KillPID)

		self.stopButton.pack( side = tkinter.RIGHT, fill = tkinter.X)
		self.connectButton.pack( side = tkinter.RIGHT, fill = tkinter.X)

		self.setMessage(_("Idle"), False)

	def about(self):
		
		t = RemoteH.AboutWindow.AboutWindow(self.paths)

	def run(self):

		self.app.mainloop()
		self.app = None
		self.KillPID()
		sys.exit(0)


	def optionChanged(self, disable_all = False):
		
		if disable_all:
			self.displayHostBox["state"] = tkinter.DISABLED
			self.cb_lowcolors["state"] = tkinter.DISABLED
		elif self.opcion.get() == 0:
		    self.displayHostBox["state"] = tkinter.NORMAL
		    self.cb_lowcolors["state"] = tkinter.DISABLED
		else:
		    self.displayHostBox["state"] = tkinter.DISABLED
		    self.cb_lowcolors["state"] = tkinter.NORMAL


	def delete_entry_cb(self,w):
		
		if self.delete_entry:
		    self.address.set("")
		    self.delete_entry = False


	def ConnectSupport(self, event = None):
		"""
		Call VNC in a thread.
		
		@author: Derek Buranen
		@author: Aaron Gerber
		"""
		if self.opcion.get() == 0: # Get Help
			if self.validHost(self.address.get().strip()) and self.address.get() != _("Enter/Select Support Address"):
				self.setMessage(_("Connecting..."), True)
				
				host = self.address.get().strip()
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
		about = RemoteH.AboutWindow.AboutWindow(self, wx.ID_ABOUT, _("About RemoteH"), self.paths)


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
	
	
	def setMessage(self, message, status):

		if self.app is None:
			return

		self.status.set(message)

		if status:
			self.connectButton["state"] = tkinter.DISABLED
			self.stopButton["state"] = tkinter.NORMAL
			self.optionChanged(True)
		else:
			self.connectButton["state"] = tkinter.NORMAL
			self.stopButton["state"] = tkinter.DISABLED
			self.optionChanged(False)


	def check_wm(self):

		if (not self.process.isrunning()) or (self.process.returnPID is None):
			self.process.KillPID()
			self.setMessage(_("Idle"), False)
			return

		self.app.after(500, self.check_wm)


	def NATPMP(self, action):
		"""
		Call NAT-PMP on router to get port 5500 forwarded.

		@author: Dennis Koot
		"""
		if sys.platform == 'darwin' or re.match('(?:open|free|net)bsd|linux',sys.platform):
			if self.enablePMP:
				if action == 'request':
					lifetime = 3600
					print("Request port 5500 (NAT-PMP).")
				else:
					lifetime = 0
					print("Give up port 5500 (NAT-PMP).")

				pubpriv_port = int(5500)
				protocol = NATPMP.NATPMP_PROTOCOL_TCP

				try:
					gateway = NATPMP.get_gateway_addr()
					print(NATPMP.map_port(protocol, pubpriv_port, pubpriv_port, lifetime, gateway_ip=gateway))
				except:
					print("Warning: Unable to automap port.")



	def createThread(self, host=""):

		self.paths['low-colors'] = self.lowcolor.get() # Set low-colors to value of checkbox

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

		print(_("RemoteHThread.run(pid: %s) running...") % str(self.process.returnPID))
		self.app.after(500, self.check_wm)
