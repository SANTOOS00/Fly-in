import re



ss = '{[s] simo'

patter = r'^([^\s-]+)(.*)'

match = re.match(patter, ss)
print(match.groups())
