import multiprocessing as mp
import time
import os

start_time = time.time()

def count(n):
    proc = os.getpid()      # pid 프로세스마다의 고유번호
    for i in range(n):
        print("PIDL %d, -- %d" %(proc, i))


pt = []                     # process_table
for _ in range(4):
    p = pt.append(mp.Process(target=count, args=(2500,)))
    pt[-1].start()    

for p in pt:
    p.join()

# p1 = mp.Process(target=count, args=(2500,))     # 인자로 줄땐 튜플로 줘야함..(한개라도)
# p2 = mp.Process(target=count, args=(2500,))
# p3 = mp.Process(target=count, args=(2500,))
# p4 = mp.Process(target=count, args=(2500,))

# p1.start()
# p2.start()
# p3.start()
# p4.start()

# # 어느쪽이 먼저 끝날지 모르니까,, 다 끝난후에 결과 프린트 하기위해 join 해줌
# p1.join()
# p2.join()
# p3.join()
# p4.join()

#count(10000)
print("time : %f"%(time.time() - start_time))

# 멀티쓰레드 - 병목을 줄여서 제 속도를 낼 수 있도록 해줌 (속도가 빨라진게 아님)