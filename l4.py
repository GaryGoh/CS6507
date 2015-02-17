__author__ = 'GaryGoh'

t0 = None


def insert(t, v):
    if t == None:
        return {'d': v, 'l': None, 'r': None}
    elif v < t['d']:
        return {'d': t['d'], 'l': insert(t['l'], v), 'r': t['r']}
    else:
        return {'d': t['d'], 'l': t['l'], 'r': insert(t['r'], v)}


# def bin_sort_tree(t):
# if t.values[-] == None:

def preorder(t):
    if t==None:
        return []
    else:
        return preorder(t['l']) + [t['d']] + preorder(t['r'])


t1 = insert(t0, 10)
print t1.values()

t2 = insert(t1, 5)
print t2.values()

t3 = insert(t2, 15)
print t3

t = {'r': {'r': None, 'd': 15, 'l': None}, 'd': 10, 'l': {'r': None, 'd': 5, 'l': None}}
print preorder(t)

