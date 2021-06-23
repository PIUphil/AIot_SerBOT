import threading as th

x = None

def boo():
    global x
    x = 10

def foo():
    print(x)

p1 = th.Thread(target=boo)
p2 = th.Thread(target=foo)

p1.start()
p2.start()

p1.join()
p2.join()