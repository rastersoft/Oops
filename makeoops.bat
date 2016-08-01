:: Oops - Oops is to support others
::
:: Copyright 2016 Raster Software Vigo
::
:: Oops is a utility to facilitate the connection of VNC
::
:: Based on Gitso, from Aaron Gerber and Derek Buranen, @copyright: 2008 - 2010
::
:: Oops is free software: you can redistribute it and/or modify
:: it under the terms of the GNU General Public License as published by
:: the Free Software Foundation, either version 3 of the License, or
:: (at your option) any later version.
::
:: Oops is distributed in the hope that it will be useful,
:: but WITHOUT ANY WARRANTY; without even the implied warranty of
:: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
:: GNU General Public License for more details.
::
:: You should have received a copy of the GNU General Public License
:: along with Oops.  If not, see <http://www.gnu.org/licenses/>.

"C:\Python34\python" setup.py py2exe

"C:\Program Files (x86)\NSIS\makensis.exe" /X"SetCompressor /FINAL /SOLID lzma " makeoops.nsi
:: rd build /s /q
