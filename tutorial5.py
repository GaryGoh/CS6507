__author__ = 'GaryGoh'


def ParentToAdj(r):
    adj_list = {}
    for key, value in r.items():
        if value == None: continue
        if not value in adj_list.keys():
            adj_list[str(value)] = key
            continue
        adj_list[str(value)].append(key)
    return adj_list


r = {10: None, 1: 10, 5: 10, 9: 10, 20: 1, 7: 1, 4: 9}
t = {10: [1, 5, 9], 9: [4], 1: [7, 20]}
print ParentToAdj(r)