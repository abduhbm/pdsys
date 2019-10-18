import json
import multiprocessing as mp
from pdsys import utils
from .__version__ import __version__


def report(hosts=None, np='MAX'):
    import pandas as pd

    if not hosts:
        r = utils.report()
        return pd.read_json(r)

    if not isinstance(hosts, list):
        raise ValueError('hosts type must be list')

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

    return pd.DataFrame(results)
