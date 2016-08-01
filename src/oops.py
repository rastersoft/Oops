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

import sys
import platform

import tkinter
import os
import gettext
import locale
import pkg_resources

import Oops.ConnectionWindow
import Oops.ArgsParser

if sys.platform.startswith('win'):
	if os.getenv('LANG') is None:
		lang, enc = locale.getdefaultlocale()
		os.environ['LANG'] = lang


if __name__ == "__main__":

	args = Oops.ArgsParser.ArgsParser()
	locale.setlocale(locale.LC_ALL, '')
	if sys.platform.startswith('win'):
		gettext.bindtextdomain('oops', os.path.join('.','locale'))
	else:
		gettext.bindtextdomain('oops', args.paths['locales'])
	gettext.textdomain('oops')

	w = Oops.ConnectionWindow.ConnectionWindow(args.GetPaths())
	w.run()
