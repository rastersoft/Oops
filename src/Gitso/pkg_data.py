'''
Created on 14 de sept. de 2015

@author: raster
'''

import pkg_resources

def get_version():
    
    version = str(pkg_resources.require("gitso")[0].version)
    return version