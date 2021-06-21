from pop import LiDAR, Pilot

SPEED = 50
direction = 0

lidar = LiDAR.Rplidar()
bot = Pilot.SerBot()

lidar.connect()
lidar.startMotor()

bot.setSpeed(SPEED)

while True:
    collision = True

    while collision:
        collision = False
        vectors = lidar.getVectors()
        
        for v in vectors:
            degree = v[0]    # 각도
            distance = v[1]  # 거리

            left_hand = (direction-60)%360   # 360을 넘어서지 않도록
            right_hand = (direction+60)%360

            disc = None
            if left_hand > right_hand:      # 진행방향쪽 거리만 이용하기위해
                disc = degree >= left_hand or degree <= right_hand
            else:
                disc = degree >= left_hand and degree <= right_hand

            if disc:
                if distance <= 750:
                    collision = True
                    bot.stop()
                    break
        
        if collision:
            direction += 30
            direction %= 360
    
    bot.move(direction, 50)
