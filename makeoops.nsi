; makeoops.nsi
; ----------------
; Package Oops for Windows using NSIS
;
; Oops - Oops is to support others
;
; Copyright 2016 Raster Software Vigo
;
; Oops is a utility to facilitate the connection of VNC
;
; Based on Gitso, from Aaron Gerber and Derek Buranen, @copyright: 2008 - 2010
;
; Oops is free software: you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation, either version 3 of the License, or
; (at your option) any later version.
;
; Oops is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.
;
; You should have received a copy of the GNU General Public License
; along with Oops.  If not, see <http://www.gnu.org/licenses/>.


!define VERSION "0.1.0"
Name "Oops ${VERSION}"
Icon "./data/icons/oops.ico"
UninstallIcon "./data/icons/oops.ico"
OutFile "oops-install.exe"

; The default installation directory
InstallDir $PROGRAMFILES\Oops
; Registry key to check for directory (so if you install again, it will overwrite the old one automatically)
InstallDirRegKey HKLM "Software\Oops" "Install_Dir"

;--------------------------------
; Version Information
  VIProductVersion ${VERSION}.0
  VIAddVersionKey "ProductName" "Oops"
  VIAddVersionKey "Comments" "Oops is to support others"
  VIAddVersionKey "CompanyName" "https://github.com/rastersoft/Oops"
  VIAddVersionKey "LegalCopyright" "GPL 3"
  VIAddVersionKey "FileDescription" "Oops"
  VIAddVersionKey "FileVersion" "${VERSION}"
;--------------------------------

;--------------------------------
; Pages
Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles
;--------------------------------

Section "Oops"
  SectionIn RO
  SetOutPath $INSTDIR
	  ; Write the installation path into the registry
	  ; Write the uninstall keys for Windows
	  WriteRegStr HKLM SOFTWARE\Oops "Install_Dir" "$INSTDIR"
	  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Oops" "DisplayName" "Oops"
	  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Oops" "UninstallString" '"$INSTDIR\uninstall.exe"'
	  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Oops" "NoModify" 1
	  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Oops" "NoRepair" 1
	  WriteUninstaller "uninstall.exe"
;  File ".\hosts.txt"
  File ".\data\icons\oops.ico"
  File ".\data\icons\oops.png"
  File ".\COPYING"
  File ".\dist\oops.exe"
  File ".\dist\oops.ico"
  File ".\dist\library.zip"
  CreateDirectory "$INSTDIR\locale\es\LC_MESSAGES"
  File "/oname=locale\es\LC_MESSAGES\oops.mo" ".\dist\locale\es\LC_MESSAGES\oops.mo"
  File ".\dist\python34.dll"
  File ".\dist\pywintypes34.dll"
  File ".\dist\bz2.pyd"
  File ".\dist\win32api.pyd"
  File ".\dist\_ssl.pyd"
  File ".\dist\_socket.pyd"
  File ".\dist\select.pyd"
  File ".\dist\unicodedata.pyd"
  File ".\arch\win32\tightVNC_LICENCE.txt"
  File ".\arch\win32\tightVNC_COPYING.txt"
  File ".\arch\win32\tightVNC_README.txt"
  File ".\arch\win32\VNCHooks_COPYING.txt"
  File ".\arch\win32\msvcr71_README.txt"
 ;start menu items
  CreateDirectory "$SMPROGRAMS\Oops"
  CreateShortCut "$SMPROGRAMS\Oops\Oops.lnk" "$INSTDIR\oops.exe" "" "$INSTDIR\oops.ico" 0
  File ".\arch\win32\vncviewer.exe"
  File ".\arch\win32\WinVNC.exe"
  File ".\arch\win32\VNCHooks.dll"

 ;Registry tweaks to TightVNC's server
  WriteRegDWORD HKCU "Software\ORL\WinVNC3" "RemoveWallpaper" 1
  WriteRegDWORD HKCU "Software\ORL\WinVNC3" "EnableFileTransfers" 1
 ;set default password to something so WinVNC.exe doesn't complain about having no password
  WriteRegBin HKCU "SOFTWARE\ORL\WinVNC3" "Password" "238f16962aeb734e"
  WriteRegBin HKCU "SOFTWARE\ORL\WinVNC3" "PasswordViewOnly" "238f16962aeb734e"
 ;Try to set it for all users, but I'm not positive this works
  WriteRegDWORD HKLM "Software\ORL\WinVNC3" "RemoveWallpaper" 1
  WriteRegDWORD HKLM "Software\ORL\WinVNC3" "EnableFileTransfers" 1
  WriteRegBin HKLM "SOFTWARE\ORL\WinVNC3" "Password" "238f16962aeb734e"
  WriteRegBin HKLM "SOFTWARE\ORL\WinVNC3" "PasswordViewOnly" "b0f0ac1997133bc9"
SectionEnd


; Uninstall
;------------------------------------------------------
Section "Uninstall"
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Oops"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Oops"
  ; Remove files and uninstaller
  Delete $INSTDIR\vncviewer.exe
  Delete $INSTDIR\VNCHooks.dll
  Delete $INSTDIR\WinVNC.exe
  ; Remove shortcuts and folder
  RMDir /r "$SMPROGRAMS\Oops"
  RMDir /r $INSTDIR
SectionEnd
