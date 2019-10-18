import pdsys

df = pdsys.report()
print(df)
print(df[df['cpu_percent'] > 0][['name', 'pid', 'memory_percent']])
