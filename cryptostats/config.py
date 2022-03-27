"""
Config object, read in from config.json
"""

import json
import os

base_dir = os.path.dirname(os.path.realpath(__file__))
CONFIG = {}
CONFIG['base_dir'] = base_dir
CONFIG['infura_url'] = os.environ.get('INFURA_URL')