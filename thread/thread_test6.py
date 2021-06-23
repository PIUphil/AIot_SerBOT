import multiprocessing as mp

#x = None

def boo(d):
    d.value = 10

def foo(d):
    d.value = 3.14

d = None

def show():
    print(d.value)

def main():
    global d
    d = mp.Manager().Value('d', None)
    p1 = mp.Process(target=boo, args = (d,))
    p2 = mp.Process(target=foo, args = (d,))

    p1.start()
    p2.start()

    p1.join()   
    p2.join()

    show()

if __name__ =='__main__':
    main()