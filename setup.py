#!/usr/bin/env python

import os
import sys
import re
from glob import glob
from distutils.core import setup

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
if 'linux' == sys.platform:
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
        data_files.append((os.path.join('share','icons','hicolor','512x512','apps'),['data/icons/icon.png']))
    data_files.append((os.path.join('.','share','gitso'),['data/icons/icon.ico']))
    data_files.append((os.path.join('.','share','gitso'),['data/icons/icon.png']))
    data_files.append((os.path.join('.','share','doc','gitso'),['COPYING']))

    for lang_name in [f for f in os.listdir('locale')]:
        mofile = os.path.join('locale', lang_name,'LC_MESSAGES','gitso.mo')
        # translations must be always in /usr/share because Gtk.builder only search there. If someone knows how to fix this...
        if platform == 'windows':
            target = os.path.join('.', lang_name, 'LC_MESSAGES') # share/locale/fr/LC_MESSAGES/
        else:
            target = os.path.join('/usr','share', 'locale', lang_name, 'LC_MESSAGES') # share/locale/fr/LC_MESSAGES/
        data_files.append((target, [mofile]))

    return data_files


def compile_translations():

        for pofile in [f for f in os.listdir('po') if f.endswith('.po')]:
            pofile = os.path.join('po', pofile)

            lang = os.path.basename(pofile)[:-3] # len('.po') == 3
            modir = os.path.join('locale', lang, 'LC_MESSAGES') # e.g. locale/fr/LC_MESSAGES/
            mofile = os.path.join(modir, 'gitso.mo') # e.g. locale/fr/LC_MESSAGES/devede_ng.mo

            # create an architecture for these locales
            if not os.path.isdir(modir):
                os.makedirs(modir)

            if not os.path.isfile(mofile) or (has_dep and dep_util.newer(pofile, mofile)):
                # msgfmt.make(pofile, mofile)
                os.system("msgfmt \"" + pofile + "\" -o \"" + mofile + "\"")

compile_translations()

#here = os.path.abspath(os.path.dirname(__file__))

params_setup = {}

params_setup['name'] = 'gitso'
params_setup['version'] = '0.7'
params_setup['description']='Gitso is to support others'
params_setup['long_description']="A program to simplify using reverse VNC"
params_setup['license']='GPLv3'
params_setup['packages']=['Gitso']
params_setup['package_dir'] = {"Gitso" : "src/Gitso"}
params_setup['data_files'] = get_data_files()
params_setup['scripts']=['src/gitso.py']

if platform == 'windows':
    params_setup['windows'] = [{"script":"Gitso.py", "icon_resources":[(1,"icon.ico")]}]

setup(**params_setup)
