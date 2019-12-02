# pdsys

Pandas-powered package for systems monitoring

### To Inatall
```shell script
pip install pdsys
```

### Basic usage

```python
import pdsys
```

To get a system utilization report (as dataframe) on local:

```python
df = pdsys.report()
```

pdsys returns by default all process attributes information from ***psutil*** process iterator:

```python
df.columns.tolist()
>>> ['cmdline',
 'connections',
 'cpu_affinity',
 'cpu_num',
 'cpu_percent',
 'cpu_times.children_system',
 'cpu_times.children_user',
 'cpu_times.system',
 'cpu_times.user',
 'create_time',
 'cwd',
 'environ',
 'exe',
 'gids.effective',
 'gids.real',
 'gids.saved',
 'hostname',
 'io_counters',
 'io_counters.read_bytes',
 'io_counters.read_chars',
 'io_counters.read_count',
 'io_counters.write_bytes',
 'io_counters.write_chars',
 'io_counters.write_count',
 'ionice.value',
 'memory_full_info',
 'memory_full_info.data',
 'memory_full_info.dirty',
 'memory_full_info.lib',
 'memory_full_info.pss',
 'memory_full_info.rss',
 'memory_full_info.shared',
 'memory_full_info.swap',
 'memory_full_info.text',
 'memory_full_info.uss',
 'memory_full_info.vms',
 'memory_info.data',
 'memory_info.dirty',
 'memory_info.lib',
 'memory_info.rss',
 'memory_info.shared',
 'memory_info.text',
 'memory_info.vms',
 'memory_maps',
 'memory_percent',
 'name',
 'nice',
 'num_ctx_switches.involuntary',
 'num_ctx_switches.voluntary',
 'num_fds',
 'num_threads',
 'open_files',
 'pid',
 'ppid',
 'status',
 'terminal',
 'threads',
 'uids.effective',
 'uids.real',
 'uids.saved',
 'username']
```

You can query the output dataframe to get more insights about the system:
```python
# getting top 5 processes sorted by memory utilization
df.sort_values(by='memory_percent',
               ascending=False)[['name', 'memory_percent']].head(5)
```

|     | name             |   memory_percent |
|----:|:-----------------|-----------------:|
| 104 | systemd-journald |         20.865   |
|  76 | gunicorn         |          4.06886 |
|  75 | gunicorn         |          4.05697 |
|  77 | gunicorn         |          4.01536 |
|  74 | gunicorn         |          1.92189 |


Also, pdsys can run reports from remote systems by providing list of hosts:
```python
df = pdsys.report(hosts=['user@host1', 'user@host2'])
df[df.memory_percent > 0.9].groupby(['hostname',
                                     'name']).agg({'memory_percent': 'sum',
                                                   'pid': 'count',
                                                   'num_threads': 'sum',
                                                   'memory_info.rss': lambda x: sum(x) / 1e6})
```
|    | hostname   | name                            |   memory_percent |   pid |   num_threads |   memory_info.rss |
|---:|:-----------|:--------------------------------|-----------------:|------:|--------------:|------------------:|
|  0 | host1      | Google Chrome                   |          2.13456 |     1 |            31 |          183.357  |
|  1 | host1      | Google Chrome Helper (GPU)      |          1.31197 |     1 |             9 |          112.697  |
|  2 | host1      | Google Chrome Helper (Renderer) |          9.3699  |     8 |           107 |          804.868  |
|  3 | host1      | Python                          |          1.0848  |     1 |            12 |           93.184  |
|  4 | host1      | Terminal                        |          1.7745  |     1 |             6 |          152.429  |
|  5 | host1      | pycharm                         |          9.88402 |     1 |            66 |          849.031  |
|  6 | host2      | do-agent                        |          1.19791 |     1 |             6 |           12.3822 |
|  7 | host2      | gunicorn                        |         14.0631  |     4 |             4 |          145.363  |
|  8 | host2      | postgres                        |          1.54504 |     1 |             1 |           15.9703 |
|  9 | host2      | python3                         |          3.47208 |     3 |             4 |           35.8892 |
| 10 | host2      | systemd-journald                |         21.0484  |     1 |             1 |          217.567  |
