import random
 
lane_num = 2
lane = [[], []]
 
max_car_num = 1000
road_len = 1000
 
h = 6
p_b = 0.94
p_0 = 0.5
p_d = 0.1
v_max = 20
gap = 7
 
p_car = 0.6
p_crash= 0
 
time_period = 300
 
class Car:
    def __init__(self, v = 0, lane = 1):
        self.v = random.randint(1, v_max)
        self.lane = lane
        self.pos = 0
        self.b = 0
    def __lt__(self, other):
        return self.pos < other.pos
 
car = [0] * max_car_num
for i in range(max_car_num):
    car[i] = Car()
 
def rand(v, b, t_h, t_s):
    if b == 1 and t_h < t_s:
        return p_b
    if v == 0 and not(b == 1 and t_h < t_s):
        return p_0
    return p_d
 
 
if __name__ == "__main__":
    car_num = 0
    for i in range(2):
        for j in range(road_len):
            lane[i].append('.')
    v_now = 0
    v_succ = [0] * lane_num
    for i in range(time_period):
        for j in range(car_num):
            k = j + 1
            while (k < car_num and car[k].lane != car[j].lane):
                k += 1
            #0 Determine p
            t_s = min(car[j].v, h)
            d = car[k].pos - car[j].pos
            if j == car_num - 1:
                d = 2 ** 31
            if car[j].v > 0 and d != 2 ** 31:
                t_h = float(d) / car[j].v
            else:
                t_h = t_s
            p = rand(car[j].v, car[k].b, t_h, t_s)
            car[j].b = 0
            if j > 0:
                v_succ[car[j - 1].lane] = v_now
            v_now = car[j].v
 
            #1 accelerate
            if (car[k].b == 0 and car[j].b == 0) or t_h >= t_s:
                car[j].v = min(car[j].v + 1, v_max)
 
            #2 braking
            #simplicated
            d_eff = d -1 + max(car[k].v - gap, 0)
            car[j].v = max(min(d_eff, car[j].v), 0)
            if car[j].v < v_now:
                car[j].b = 1
 
            #3 random brake
            if random.random() < p:
                car[j].v = max(car[j].v - 1, 0)
                if p == p_b:
                    car[j].b = 1
 
            #traffic accident
            if random.random() < p_crash:
                car[j].v /= 3
 
            #lane changing
            k = j + 1
            l = j - 1
            while (k < car_num and car[k].lane == car[j].lane):
                k += 1
            if k < car_num:
                d_p = car[k].pos - car[j].pos + max(car[k].v - gap, 0)
            else:
                d_p = 2 ** 31
            while (l > 0 and car[l].lane == car[j].lane):
                l -= 1
            dst = 1 - car[j].lane
            #if (car[j].b == 0 and v_now > d):
            if v_now > d:
                if (d_p >= car[j].v and
                        (j == 0 or l < 0 or (car[j].pos - car[l].pos) >= v_succ[dst])):
                    car[j].lane = dst
                    car[j].v = v_now
 
            #4 car motion
            car[j].pos += car[j].v
 
        #adding new car
        if random.random() < p_car:
            car[car_num] = Car()
            car_num += 1
        car[:car_num] = sorted(car[:car_num])
        for i in reversed(range(car_num)):
            if car[i].pos > road_len:
                del car[i]
                car_num -= 1
 
        line = '.' * road_len
        cnt1 = 0
        cnt2 = 0
        for j in range(car_num):
            if car[j].lane == 0:
                line = line[:car[j].pos] + str(car[j].v) + line[(car[j].pos + 1):]
                cnt1 += 1
            #print "car %d: pos=%d v=%d" % (j, car[j].pos, car[j].v)
        print(line)
        line = '.' * road_len
        for j in range(car_num):
            if car[j].lane == 1:
                line = line[:car[j].pos] + str(car[j].v) + line[(car[j].pos + 1):]
                cnt2 += 1
        print(line)
        print('')
        print('(%d, %d)' % (cnt1,cnt2))
