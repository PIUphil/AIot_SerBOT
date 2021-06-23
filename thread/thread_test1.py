import multiprocessing as mp
import time

print(mp.cpu_count())       # 현재 사용가능한 코어 개수     # 6

def worker1():
    time.sleep(2)
    print("run SubProcess1")

def worker2():
    time.sleep(1)
    print("run SubProcess2")

p1 = mp.Process(target=worker1)       # sub process 함수 - thread처럼 보이도록 함
#p1.start()                           # 복제됨. 병렬 실행(스케쥴링해라 - 운영체제에게 명령)
#time.sleep(2)
#print("The end, MainProcess")
p2 = mp.Process(target=worker2)
p1.start()
p2.start()                    
#p.join()                            # 자식이 종료될 때까지 blocking함
print("The end, MainProcess")