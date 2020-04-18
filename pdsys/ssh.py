try:
    from remoto import connection
except ImportError:
    raise ImportError('remoto package needs to be installed for remote host \
    monitoring')

from pdsys import utils

from . import LOG_LEVEL


def connect_ssh(hosts):
    reports = []
    for host in hosts:
        connect = connection.get('ssh')
        conn = connect(host)
        conn.logger.setLevel(LOG_LEVEL)

        conn.remote_import_system = 'json'

        remote = conn.import_module(utils)
        report = remote.report()
        reports.append(report)
        conn.exit()

    return reports
