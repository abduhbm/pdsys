import json
import multiprocessing as mp
import os
from datetime import datetime

import pandas as pd

from .__version__ import __version__  # noqa: F401
from pdsys import utils

LOG_LEVEL = 'ERROR'


def report(hosts=None, np='MAX'):
    if not hosts:
        r = utils.report()
        df = pd.read_json(r)
        df.insert(0, 'timestamp', datetime.now().replace(microsecond=0))
        df.set_index('timestamp', inplace=True)

        return df

    if isinstance(hosts, list):
        pass

    elif isinstance(hosts, str):
        hosts = hosts.splitlines()
        if len(hosts) == 1 and os.path.isfile(hosts[0]):
            with open(hosts[0], 'r') as f:
                hosts = [h.strip() for h in f.readlines()]

    elif hasattr(hosts, 'read'):
        hosts = [h.strip() for h in hosts.readlines()]

    else:
        raise ValueError('hosts must be str, path object or file-like object')

    from pdsys.ssh import connect_ssh

    if np == 'MAX':
        cpu_count = mp.cpu_count()
    else:
        cpu_count = int(np)

    if len(hosts) < cpu_count:
        cpu_count = len(hosts)

    chunks = utils.chunker_list(hosts, cpu_count)
    pool = mp.Pool(cpu_count)
    procs = pool.map(connect_ssh, chunks)
    pool.terminate()
    pool.close()

    results = []
    for p in procs:
        for r in p:
            results += json.loads(r)

    df = pd.DataFrame(results)
    df.insert(0, 'timestamp', datetime.now().replace(microsecond=0))
    df.set_index('timestamp', inplace=True)

    return df
