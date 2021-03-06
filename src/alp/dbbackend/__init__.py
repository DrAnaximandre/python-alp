from __future__ import absolute_import
from __future__ import print_function

import json
import os


_alp_base_dir = os.path.expanduser('~')
if not os.access(_alp_base_dir, os.W_OK):  # pragma: no cover
    _alp_base_dir = '/tmp'


_alp_dir = os.path.join(_alp_base_dir, '.alp')
if not os.path.exists(_alp_dir):  # pragma: no cover
    os.makedirs(_alp_dir)

_db_engine = 'mongodb'
_host_adress = 'mongo_m'
_host_port = 27017
_db_name = 'modelization'
_models_collection = 'models'
_generators_collection = 'generators'

if os.getenv("TEST_MODE") == "ON":  # pragma: no cover
    _host_adress = '127.0.0.1'

# note: we have to be able to accept other structures

_config_path = os.path.expanduser(os.path.join(_alp_dir, 'alpdb.json'))
if os.path.exists(_config_path):  # pragma: no cover
    _config = json.load(open(_config_path))
    _db_engine = _config.get('db_engine', 'mongodb')
    assert _db_engine in {'mongodb'}
    _host_adress = _config.get('host_adress', 'mongo_m')
    _host_port = _config.get('host_port', 27017)
    _db_name = _config.get('db_name', 'modelization')
    _models_collection = _config.get('_models_collection', 'models')
    _generators_collection = _config.get('_generators_collection', 'models')

# save config file
_config = {'db_engine': _db_engine,
           'host_adress': _host_adress,
           'host_port': _host_port,
           'db_name': _db_name,
           'models_collection': _models_collection,
           'generators_collection': _generators_collection}

with open(_config_path, 'w') as f:
    f.write(json.dumps(_config, indent=4))

# import backend
if _db_engine == 'mongodb':
    from ..dbbackend.mongo_backend import *  # NOQA
else:
    raise Exception('Unknown backend: ' + str(_db_engine))
