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

import pkg_resources
import sys

def get_version():
    
    version = str(pkg_resources.require("remoteh")[0].version)
    return version
