import random
import numpy

lane_num = 2
lane = [[], []]

max_car_num = 10000
road_len =  1000

h = 6
p_b = 0.94
p_0 = 0.5
p_d = 0.1
v_max = [6, 10]
gap = 7

p_car = 1
p_crash = 0

time_period = 200


class Car:
    car_cnt = 0
    def __init__(self, v = 1, lane = 1):
        self.size = 1
        if random.random() < 0.1:
            self.size = 0
        self.c_id = Car.car_cnt
        Car.car_cnt += 1
        #print(Car.car_cnt, max_car_num)
        #self.v = 0
        self.v = random.randint(0, v_max[self.size])
        self.lane = random.randint(0, 1)
        #self.pos = random.randint(0, road_len)
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
    Car.car_cnt = 0

    lane_cnt = [0] * lane_num
    car_num = 0
    flow = [0.0] * lane_num

    lane_change_cnt = 0

    car = [0] * max_car_num
    '''
    for i in range(max_car_num):
        car[i] = Car()
    '''
    for i in range(2):
        for j in range(road_len):
            lane[i].append('.')
    v_now = 0
    #adding new cars
    cur = 0
    vis = [[0]*road_len, [0]*road_len]
    for i in range(max_car_num):
        car[car_num] = Car()
        car[car_num].pos = int(cur / lane_num)
        cur += float(road_len) * lane_num / max_car_num
        car[car_num].lane = random.randint(0,1)
        if vis[car[car_num].lane][car[car_num].pos] == 0:
            vis[car[car_num].lane][car[car_num].pos] = 1
        else:
            car[car_num].lane = 1 - car[car_num].lane
            vis[car[car_num].lane][car[car_num].pos] = 1
        #print (car[car_num].pos, car[car_num].lane)
        #print car[car_num].pos, car[car_num].lane
        # random lane
        #car[car_num].lane = random.randint(0,1)
        lane_cnt[car[car_num].lane] += 1
        car_num += 1
    #print car_num,lane_cnt
    sum_v = 0
    sum_vs = [0] * lane_num
    speed_1 = []
    [speed_1.append([]) for i in range(max_car_num)]
    for i in range(time_period):
        v_succ = [2 ** 31] * lane_num

        if time_period-1 == i:
            for j in range(car_num):
                sum_v += car[j].v
                sum_vs[car[j].lane] += car[j].v
        for j in list(reversed(range(car_num))):
        #for j in (range(car_num)):
            if (time_period-1)*0.618 >= i:
                #print (max_car_num, car[j].c_id)
                speed_1[car[j].c_id].append(car[j].v)
            
            v_succ_cur = v_succ
            k = j + 1
            while k < car_num and car[k].lane != car[j].lane:
                k += 1
            if k >= car_num:
                k = 0
                while k < car_num and car[k].lane != car[j].lane:
                    k += 1
            kk = k + 1
            while kk < car_num and car[kk].lane != car[j].lane:
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
            b_now = car[j].b
            car[j].b = 0
            if j > 0:
                v_succ[car[j - 1].lane] = v_now
            else:
                v_succ[0] = [2**31] * lane_num
            v_now = car[j].v

            #1 accelerate
            if k >= car_num or (b_now == 0 and car[j].b == 0) or t_h >= t_s:
                car[j].v = min(car[j].v + 1, v_max[car[j].size])

            #2 braking
            if kk < car_num:
                v_anti = min(mmod(car[kk].pos, car[k].pos), car[k].v)
            else:
                v_anti = car[k].v
            d_eff = d - 1 + max(v_anti - gap, 0)
            car[j].v = max(min(d_eff, car[j].v), 0)
            #car[j].v = max(min(d_eff, v_now), 0)
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
                d_p = mmod(car[k].pos, car[j].pos)
                d_p_eff = mmod(car[k].pos, car[j].pos) + max(car[k].v - gap, 0)
            else:
                d_p = 2 ** 31
                d_p_eff = 2 ** 31
            while (l > 0 and car[l].lane == car[j].lane):
                l -= 1
            if l < 0:
                l = car_num - 1
                while (l > 0 and car[l].lane == car[j].lane):
                    l -= 1
            dst = 1 - car[j].lane
            #if ((dst == 1 and v_now <= 7) or v_now > d) and b_now == 0: # velocity based rule
            #if (car[j].b == 0 and (\
                #v_now > d or\
                #(dst == 1 and v_max[car[j].size] <= 7))): # slow car right rule
            #if (car[j].b == 0 and (\
                #v_now > d or\
                #dst == 1\
                #)):
            '''
            if v_now > 0:
                t_p_h = float(d_p) / v_now
            else:
                t_p_h = 4
            if (dst == 0 and b_now == 0 and v_now > d) or\
               (dst == 1 and b_now == 0 and t_p_h > 3.0 and (t_h > 6.0 or v_now > d)): # right priority rule in paper

            if v_now > 0:
                t_p_h = float(d_p) / v_now
            else:
                t_p_h = 4
            if (dst == 0 and b_now == 0 and v_now > d) or\
               (dst == 1 and v_now <= 7 and b_now == 0 and t_p_h > 3.0 and (t_h > 6.0 or v_now > d)): # velocity-based with paper
            '''
            if b_now == 0 and v_now > d: # symmetric rule
              if (d_p_eff >= v_now and
                        (j == 0 or l < 0 or (mmod(car[j].pos, car[l].pos)) >=
                            v_succ_cur[dst])):
                    lane_cnt[dst] += 1
                    lane_cnt[1-dst] -= 1
                    car[j].lane = dst
                    car[j].v = v_now
                    lane_change_cnt += 1


            #4 car motion
            car[j].pos = (car[j].pos + car[j].v) % road_len


        if i > int(time_period * 0.618):
                # calculate flow
                for m in range(road_len/10):
                    pinp = m * 10
                    for k in range(car_num):
                        if car[k].pos <= pinp and car[k].pos + car[k].v >= pinp and car[k].v > 0:
                            flow[car[k].lane] += 1
                flow = [float(i)*10/road_len for i in flow]

        car[:car_num] = sorted(car[:car_num])
        for i in reversed(range(car_num)):
            if car[i].pos > road_len:
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
    avg_vs = [float(sum_vs[i])/lane_cnt[i] if lane_cnt[i] != 0 else 0 for i in range(lane_num)]
    return lane_cnt, car_num, float(sum_v)/car_num, flow,\
            lane_change_cnt,avg_vs, speed_1

if __name__ == "__main__":
    #print main()
    #'''
    #print('rolen car_l car_r car_n avg_v flow_l flow_r  flow   lanchge    v_l    v_r')
    print("car_num   mean    std" )
    for i in range(0,20):
        #p_car = float(i + 1) / 10
        max_car_num = (i+1)*100
        lane_cnt = [0] * lane_num
        flow_sum = [0] * lane_num
        rep = 1
        avg_vs = []
        lane_change_sum = 0
        avg_v_lrs = [[],[]]
        speed_1 = [[]*max_car_num]
        for j in range(rep):
            ret, car_num, avg_v_instance, flow, lane_change_cnt, avg_v_lr,\
                    speed_1 = main()

            lane_cnt[0] += ret[0]
            lane_cnt[1] += ret[1]
            flow_sum[0] += flow[0]
            flow_sum[1] += flow[1]
            lane_change_sum += lane_change_cnt
            avg_vs.append(avg_v_instance)
            [avg_v_lrs[i].append(avg_v_lr[i]) for i in
                    range(lane_num)]

        lane_cnt = [i / rep for i in lane_cnt]
        avg_v = sum(avg_vs)/float(len(avg_vs))
        avg_v_lr = [sum(i)/float(len(i)) for i in avg_v_lrs]
        flow_l = flow_sum[0]/rep
        flow_r = flow_sum[1]/rep + 0.00001
        '''
        print('%4d %5d %5d %5d %6.2f %6.2f %6.2f %5.2f %8d %7.2f %7.2f' 
                % (road_len,lane_cnt[0], lane_cnt[1],
                    car_num, avg_v, flow_l,
                    flow_r,
                    flow_l+flow_r,
                    lane_change_sum / rep,\
                            avg_v_lr[0],\
                            avg_v_lr[1]
                    ))
        '''
        speed_stat = numpy.array(speed_1)
        speed_mean = (numpy.mean(speed_stat, axis = 1)).tolist()
        speed_std = (numpy.std(speed_stat, axis = 1).tolist())
        for i in range(len(speed_mean)):
            print('%7d %6.2f %6.2f' % (max_car_num, speed_mean[i],
                    speed_std[i]))

        #for lis in speed_1:
            #print(' '.join(map(str,lis)))
            
        #print("="*10, " "*5, "%.2f" % (avg_v*car_num/road_len))
        #print(", ".join(map(lambda x:"%.2f" % x,avg_vs[:5])))
        #print("="*10)

    #'''
