import random

lane_num = 2
lane = [[], []]

max_car_num = 10000
road_len = 10000

h = 6
p_b = 0.94
p_0 = 0.5
p_d = 0.1
v_max = 30
gap = 7

p_car = 7.3
p_crash = 0

time_period = 3600

class Car:
    car_cnt = 0
    def __init__(self, v = 1, lane = 1):
        self.c_id = Car.car_cnt
        Car.car_cnt += 1
        self.v = random.randint(1, v_max)
        self.lane = lane
        self.pos = 0
        self.b = 0
    def __lt__(self, other):
        return self.pos < other.pos

def rand(v, b, t_h, t_s):
    if b == 1 and t_h < t_s:
        return p_b
    if v == 0 and not(b == 1 and t_h < t_s):
        return p_0
    return p_d


def main():
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
    sum_v = 0
    for i in range(time_period):
        for j in range(car_num):
            k = j + 1
            while (k < car_num and car[k].lane != car[j].lane):
                k += 1
            kk = k + 1
            while (kk < car_num and car[kk].lane != car[k].lane):
                kk += 1
            #0 Determine p
            t_s = min(car[j].v, h)
            d = car[k].pos - car[j].pos
            if k >= car_num - 1:
                d = 2 ** 31
            if car[j].v > 0 and d != 2 ** 31:
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
                v_anti = min(car[kk].pos - car[k].pos, car[k].v)
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
            kk = k + 1
            while (kk < car_num and car[kk].lane == car[j].lane):
                kk += 1
            if k < car_num:
                v_anti = car[k].v
                if kk < car_num:
                    v_anti = min(car[kk].pos - car[k].pos, car[k].v)
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
            car[j].pos = car[j].pos + car[j].v
            
            if i == time_period-1:
                sum_v += car[j].v

        #adding new car
        if random.random() < p_car:
            car[car_num] = Car()
            car_num += 1

        car[:car_num] = sorted(car[:car_num])
        for i in reversed(range(car_num)):
            if car[i].pos > road_len:
                flow[car[i].lane] += 1
                del car[i]
                car_num -= 1

        line = '.' * road_len
        '''
        for j in range(car_num):
            if car[j].lane == 0:
                #line = line[:car[j].pos] + str((car[j].v + 1) / 2) + line[(car[j].pos + 1):]
                line = line[:car[j].pos] + str((car[j].v)) + line[(car[j].pos + 1):]
            #print "car %d: id=%d pos=%d v=%d" % (j, car[j].c_id, car[j].pos, car[j].v)
        print line
        line = '.' * road_len
        for j in range(car_num):
            if car[j].lane == 1:
                #line = line[:car[j].pos] + str((car[j].v + 1) / 2) + line[(car[j].pos + 1):]
                line = line[:car[j].pos] + str((car[j].v)) + line[(car[j].pos + 1):]
        print line
        print
        '''
    return float(sum_v)/ car_num

if __name__ == "__main__":
    print ('(veh/km, avg_v)')
    for i in range(10):
        p_car = float(i + 1) / 10
        #p_car = 0.8
        flow = 0
        rep = 20
        for j in range(rep):
            #print 'iter ' + str(i)
            ret = main()
            flow += ret
        flow /= rep
        print ('(%.0f, %.2f)' % (p_car*100, flow))
