#!/usr/bin/python

import sys
import os

# To be able to import modules in the project root directory, that directory
# has to be added to the module search path (since e.g. Apache won't find the
# modules otherwise).
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from controller import c3bottles, load_config
load_config()

application = c3bottles

# vim: set expandtab ts=4 sw=4:
