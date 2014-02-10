import random

lane_num = 2
lane = [[], []]

max_car_num = 100 
road_len = 100

h = 6
p_b = 0.94
p_0 = 0
p_d = 0.1
v_max = 20
gap = 7

p_car = 1
p_crash = 0

time_period = 100


class Car:
    car_cnt = 0
    def __init__(self, v = 1, lane = 1):
        self.c_id = Car.car_cnt
        self.v = 10
        self.lane = lane
        self.pos = random.randint(0, road_len)
        self.b = 0
    def __lt__(self, other):
        return self.pos < other.pos

def mmod(a, b):
    return (a - b + road_len) % road_len
def rand(v, b, t_h, t_s):
    if b == 1 and t_h < t_s:
        return p_b
    if v == 0 and not(b == 1 and t_h < t_s):
        return p_0
    return p_d


def main():

    lane_cnt = [0] * lane_num
    car_num = 0

    car = [0] * max_car_num
    for i in range(max_car_num):
        car[i] = Car()

    flow = [0] * lane_num

    for i in range(2):
        for j in range(road_len):
            lane[i].append('.')
    v_now = 0
    v_succ = [0] * lane_num
    for i in range(time_period):
        for j in list(reversed(range(car_num))):
            k = j + 1
            while (k < car_num and car[k].lane != car[j].lane):
                k += 1
            if k >= car_num:
                k = 0
                while k < car_num and car[k].lane != car[j].lane:
                    k += 1
            kk = k + 1
            while (kk < car_num and car[kk].lane != car[j].lane):
                kk += 1
            if kk >= car_num:
                kk = 0
                while kk < car_num and car[kk].lane != car[j].lane:
                    kk += 1
            #0 Determine p
            t_s = min(car[j].v, h)
            d = mmod(car[k].pos, car[j].pos)
            if k >= car_num - 1:
                d = 2 ** 31
            if int(car[j].v) > 0 and d != 2 ** 31:
                t_h = d / car[j].v
            else:
                t_h = t_s
            p = rand(car[j].v, car[k].b, t_h, t_s)
            car[j].b = 0
            if j > 0:
                v_succ[car[j - 1].lane] = v_now
            v_now = car[j].v

            #1 accelerate
            if k >= car_num or (car[k].b == 0 and car[j].b == 0) or t_h >= t_s:
                car[j].v = min(car[j].v + 1, v_max)

            #2 braking
            if kk < car_num:
                v_anti = min(mmod(car[kk].pos, car[k].pos), car[k].v)
            else:
                v_anti = car[k].v
            d_eff = d - 1 + max(v_anti - gap, 0)
            car[j].v = max(min(d_eff, car[j].v), 0)
            if car[j].v < v_now:
                car[j].b = 1

            #3 random brake
            if random.random() < p:
                car[j].v = max(car[j].v - 1, 0)
                if p == p_b:
                    car[j].b = 1

            #traffic accident
            #if random.random() < p_crash:
                #car[j].v /= 3

            #lane changing
            k = j + 1
            l = j - 1
            while (k < car_num and car[k].lane == car[j].lane):
                k += 1
            if k >= car_num:
                k = 0
                while (k < car_num and car[k].lane == car[j].lane):
                    k += 1
            kk = k + 1
            while (kk < car_num and car[kk].lane == car[j].lane):
                kk += 1
            if kk >= car_num:
                kk = 0
                while (kk < car_num and car[kk].lane == car[j].lane):
                    kk += 1
            if k < car_num:
                v_anti = car[k].v
                if kk < car_num:
                    v_anti = min(mmod(car[kk].pos, car[k].pos), car[k].v)
                d_p = mmod(car[k].pos, car[j].pos) + max(car[k].v - gap, 0)
            else:
                d_p = 2 ** 31
            while (l > 0 and car[l].lane == car[j].lane):
                l -= 1
            if l < 0:
                l = car_num - 1
                while (l > 0 and car[l].lane == car[j].lane):
                    l -= 1
            dst = 1 - car[j].lane
            #if (car[j].b == 0 and v_now > d):
            if dst == 1 or v_now > d:
                if (d_p >= car[j].v and
                        (j == 0 or l < 0 or (mmod(car[j].pos, car[l].pos)) >= v_succ[dst])):
                    lane_cnt[dst] += 1
                    lane_cnt[1-dst] -= 1
                    #print lane_cnt, car_num
                    car[j].lane = dst
                    car[j].v = v_now

            #4 car motion
            car[j].pos = (car[j].pos + car[j].v) % road_len

        #adding new car
        if random.random() <= p_car and car_num < max_car_num - 1:
            car[car_num] = Car()
            lane_cnt[car[car_num].lane] += 1
            car_num += 1

        car[:car_num] = sorted(car[:car_num])
        for i in reversed(range(car_num)):
            if car[i].pos > road_len:
                flow[car[i].lane] += 1
                del car[i]
                car_num -= 1

        '''
        line = '.' * road_len
        for j in range(car_num):
            if car[j].lane == 0:
                #line = line[:car[j].pos] + str((car[j].v + 1) / 2) + line[(car[j].pos + 1):]
                line = line[:car[j].pos] + str((car[j].v)) + line[(car[j].pos + 1):]
            print "car %d: id=%d pos=%d v=%d" % (j, car[j].c_id, car[j].pos, car[j].v)
        print line
        line = '.' * road_len
        for j in range(car_num):
            if car[j].lane == 1:
                #line = line[:car[j].pos] + str((car[j].v + 1) / 2) + line[(car[j].pos + 1):]
                line = line[:car[j].pos] + str((car[j].v)) + line[(car[j].pos + 1):]
        print line
        print
        #'''
    return lane_cnt,car_num

if __name__ == "__main__":
    #print main()
    #'''
    print('p_car left  right cnt')
    for i in range(10):
        p_car = float(i + 1) / 10
        flow = [0] * lane_num
        rep = 30
        for j in range(rep):
            ret,car_num = main()
            flow[0] += ret[0]
            flow[1] += ret[1]
        flow = [i / rep for i in flow]
        print('%2.2f %5d %5d %5d' % (p_car, flow[0], flow[1], car_num))
    #'''
