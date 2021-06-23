import multiprocessing as mp
import time
import os

start_time = time.time()

def count(n):
    proc = os.getpid()      # pid 프로세스마다의 고유번호
    for i in range(n):
        print("PIDL %d, -- %d" %(proc, i))


nums = [2500, 2500, 2500, 2500]
pool = mp.Pool(processes=4)
pool.map(count, nums)       # 함수와 인자를 연결시켜줌 (함수 4번 실행 - 인자 4개 전달)

pool.close()                # setting이 끝나고 run시킴
pool.join()


print("time : %f"%(time.time() - start_time))