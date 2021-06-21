from lidar import LiDAR

lidar = LiDAR.Rplidar()
lidar.connect()
lidar.startMotor()

block = 8
step = 360 // block
ret = {}
for i in range(block):
    ret[step * (i+1) - step] = 0

points = list(ret.keys())

vectors = lidar.getVectors()
index = 0
for v in vectors:
    pass

print(ret)

lidar.stopMotor()