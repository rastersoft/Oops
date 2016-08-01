::
:: Gisto - Gitso is to support others
:: 
:: Copyright 2008, Aaron Gerber and Derek Buranen
:: Copyright 2015, Raster Software Vigo
:: 
:: Gitso is free software: you can redistribute it and/or modify
:: it under the terms of the GNU General Public License as published by
:: the Free Software Foundation, either version 3 of the License, or
:: (at your option) any later version.
:: 
:: Gitso is distributed in the hope that it will be useful,
:: but WITHOUT ANY WARRANTY; without even the implied warranty of
:: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
:: GNU General Public License for more details.
:: 
:: You should have received a copy of the GNU General Public License
:: along with Gitso.  If not, see <http://www.gnu.org/licenses/>.
:: 

"C:\Python27\python" setup.py py2exe

::COPY "C:\Python27\Lib\site-packages\wx-3.0-msw\wx\msvcp71.dll" dist\msvcp71.dll

"C:\Program Files (x86)\NSIS\makensis.exe" /X"SetCompressor /FINAL /SOLID lzma " makegitso.nsi
:: rd build /s /q
