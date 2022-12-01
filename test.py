l1 = [1,0,3]
l2 = [0,2,0]
l3 = [0,4,5]

biglist = (l1 + l2 + l3)

def unique(biglist):
    list_set = set(biglist)
    unique_list = (list(list_set))
    for x in unique_list:
        print x

unique(biglist)