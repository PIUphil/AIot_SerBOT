import multiprocessing as mp

# x = None

def boo(d):
    # global x
    # x = 10
    d.append(1)

def foo(d):
    # global x
    # print(x)
    # x = 100
    d.append(2)

# manager = mp.Manager()
# d = manager.list()
d = mp.Manager().list()

# p1 = mp.Process(target=boo)
# p2 = mp.Process(target=foo)
p1 = mp.Process(target=boo, args=(d,))
p2 = mp.Process(target=foo, args=(d,))

p1.start()
p2.start()

p1.join()
p2.join()

print(d)