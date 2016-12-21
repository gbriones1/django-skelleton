import xml.etree.ElementTree as ET
tree = ET.parse('hero.xml')
root = tree.getroot()
l = [child.attrib for child in root]
heroes = []
highs = {}
lows = {}

for x in l:
    a = {'capacity': float(0)}
    for key, value in x.iteritems():
        if value.isdigit():
            value = int(value)
        if key.startswith('data-'):
            key = key[5:]
        a[key] = value
    heroes.append(a)

for key in heroes[0].keys():
    if str(heroes[0][key]).isdigit() and key != 'movement' and key != 'mp' and key != 'mprecovery' and key != 'mastery' and key != 'hitrate':
        high = max(heroes, key=lambda x:x[key])[key]
        low = min(heroes, key=lambda x:x[key])[key]
        highs[key] = high
        lows[key] = low
        val = high - low
        for h in heroes:
            h['capacity-'+key] = (float(h[key])-low)/val
            h['capacity'] += (float(h[key])-low)/val

for h in heroes:
    capacities = []
    for key in h.keys():
        if key.startswith('capacity-'):
            capacities.append({'key': key[9:], 'value': h[key[9:]], 'capacity': h[key]})
    h['maxed'] = [(x['key'], x['value']) for x in sorted(capacities, key=lambda x: x['capacity'], reverse=True)[:4]]

for key in heroes[0].keys():
    if key == 'capacity' or key == 'maxed':
        x = sorted(heroes, key=lambda x: x[key], reverse=True)
        print("\n"+key)
        for a in x:
            print(a['name'], a[key])

# import pdb; pdb.set_trace()
