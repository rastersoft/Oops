import glob
from distutils.core import setup
import py2exe
DATA_FILES = []
OPTIONS = {'argv_emulation': True}

setup(
  version = "0.1.0",
  description = "RemoteH is to support Others",
  name="RemoteH",
  
  windows=[{"script":"remoteh.py", "icon_resources":[(1,"remoteh.ico")]}],
  data_files=[(".", ["remoteh.ico"])],
  py_modules = ['AboutWindow', 'ConnectionWindow', 'ArgsParser', 'pkg_data', 'Processes', 'NATPMP'],
)
