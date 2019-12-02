import builtins
import json
import socket

import psutil

BUILTIN_TYPES = list(dir(builtins))
HOSTNAME = socket.gethostname()


def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))


def report():
    rows = []
    for p in psutil.process_iter():
        p_info = {}
        try:
            d = p.as_dict()
        except Exception:
            continue
        for k, v in d.items():
            if type(v).__name__ in BUILTIN_TYPES:
                if isinstance(v, (dict, list, tuple)):
                    p_info[k] = len(v)
                else:
                    p_info[k] = v

            else:
                if not v:
                    p_info[k] = v
                else:
                    for attr in v._fields:
                        attr_val = getattr(v, attr)
                        if type(attr_val).__name__ in dir(__builtins__):
                            p_info[f'{k}.{attr}'] = attr_val
            p_info['hostname'] = HOSTNAME

        rows.append(p_info)

    return json.dumps(rows)
