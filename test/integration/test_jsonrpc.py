import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from sanityd import SanityDaemon
from sanity_config import SanityConfig


def test_sanityd():
    config_text = SanityConfig.slurp_config_file(config.sanity_conf)
    network = 'mainnet'
    is_testnet = False

    # MODMOD
    genesis_hash = u'00000a609bb4527e1e35162d7a08b3a47df9ae1a479fcd0adf87675936896b60'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'0000096b17ca35b6884cd9269dbacc60b9ab5aa15995b5b8678e6b8a58ba85ca'

    creds = SanityConfig.get_rpc_creds(config_text, network)
    sanityd = SanityDaemon(**creds)
    assert sanityd.rpc_command is not None

    assert hasattr(sanityd, 'rpc_connection')

    # Sanity testnet block 0 hash == 0000069571db7fb6ef1177650bcaff0494380301f09a671eab1d76d3070139c3
    # test commands without arguments
    info = sanityd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert sanityd.rpc_command('getblockhash', 0) == genesis_hash
