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

import os
import sys
import re
from glob import glob
from distutils.core import setup
try:
    from distutils import dep_util
except:
    pass

OPTIONS = {}

if sys.platform == 'darwin':
    platform = 'mac'
elif re.match('(?:open|free|net)bsd|linux',sys.platform):
    platform = 'unix'
elif sys.platform.startswith('win'):
    platform = 'windows'
else:
    platform = 'unknown'

has_dep = False

if re.match('linux',sys.platform):
    try:
        from distutils import dep_util
        has_dep = True
    except:
        pass


if platform=='windows':
    import py2exe
    OPTIONS = {'argv_emulation': True}


def get_data_files():

    global platform
    global has_dep

    data_files = []

    if platform == 'unix':
        data_files.append((os.path.join('.','share','icons','hicolor','512x512','apps'),['data/icons/oops.png']))
        data_files.append((os.path.join('.','share','applications'),['data/oops.desktop']))
    if platform == "windows":
        data_files.append((os.path.join('.'),['data/icons/oops.ico']))
        data_files.append((os.path.join('.'),['data/icons/oops.png']))
    else:
        data_files.append((os.path.join('.','share','oops'),['data/icons/oops.ico']))
        data_files.append((os.path.join('.','share','oops'),['data/icons/oops.png']))
    data_files.append((os.path.join('.','share','doc','oops'),['COPYING']))

    try:
        for lang_name in [f for f in os.listdir('locale')]:
            mofile = os.path.join('locale', lang_name,'LC_MESSAGES','oops.mo')
            # translations must be always in /usr/share because Gtk.builder only search there. If someone knows how to fix this...
            if platform == 'windows':
                target = os.path.join('.','locale', lang_name, 'LC_MESSAGES') # share/locale/fr/LC_MESSAGES/
            else:
                target = os.path.join('.','share', 'locale', lang_name, 'LC_MESSAGES') # share/locale/fr/LC_MESSAGES/
            data_files.append((target, [mofile]))
    except:
        pass
    return data_files


def compile_translations():

    try:
        if (0 == os.system("msgfmt -h > /dev/null")) and os.path.exists('po'):
            os.system("rm -rf locale")
            for pofile in [f for f in os.listdir('po') if f.endswith('.po')]:
                pofile = os.path.join('po', pofile)
    
                lang = os.path.basename(pofile)[:-3] # len('.po') == 3
                modir = os.path.join('locale', lang, 'LC_MESSAGES') # e.g. locale/fr/LC_MESSAGES/
                mofile = os.path.join(modir, 'oops.mo') # e.g. locale/fr/LC_MESSAGES/devede_ng.mo
    
                # create an architecture for these locales
                if not os.path.isdir(modir):
                    os.makedirs(modir)
    
                if not os.path.isfile(mofile) or (has_dep and dep_util.newer(pofile, mofile)):
                    # msgfmt.make(pofile, mofile)
                    os.system("msgfmt \"" + pofile + "\" -o \"" + mofile + "\"")
    except:
        pass

compile_translations()

#here = os.path.abspath(os.path.dirname(__file__))

params_setup = {}

params_setup['name'] = 'oops'
params_setup['version'] = '0.7'
params_setup['description']='Oops is to support others'
params_setup['long_description']="A program to simplify using reverse VNC"
params_setup['license']='GPLv3'
params_setup['data_files'] = get_data_files()
params_setup['packages']=['Oops']
params_setup['package_dir'] = {"Oops" : "src/Oops"}


if platform == 'windows':
    params_setup['windows'] = [{"script":"src/oops.py", "icon_resources":[(1,"data/icons/oops.ico")]}]
else:
    params_setup['scripts']=['src/oops.py']

setup(**params_setup)
