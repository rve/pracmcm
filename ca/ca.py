from random import random
import sys

pb = 0.94
p0 = 0.5
pd = 0.1
ts = 7
vmax = 20
gap_safe = 7 #todo
lenmax = 1000000000
road_len = 100
lens = 10
time = 10

def column(mat, i):
    ans = list()
    for k in range(time):
        for l in range(lens):
            if k == i:
                ans.append(mat[l][k])
    return ans

def rand(vn, bn1, th, ts):
    p = 0
    if bn1 == 1 and th < ts:
        p = pb
    elif vn == 0:
        p = p0
    else:
        p = pd
    
    return p

def main():
    v = {}
    x = {}
    b = {}
    d = {}
    t = {}
    deff = {}
    a = 1

    for i in range(lens+2):
        v[i] = {}
        x[i] = {}
        b[i] = {}
        d[i] = gap_safe
        t[i] = ts
        deff[i] = gap_safe
        t[i] = ts
        for j in range(time+2):
            v[i][j] = 0
            x[i][j] = 0
            b[i][j] = 0
            if j == 0:
                v[i][j] = random() * vmax # test
                x[i][j] = a
                a += int(gap_safe*(1+random()))
                #sys.stdout.write('(%d,%d)' % (x[i][j],v[i][j]))
        #sys.stdout.write('\n')
    v[lens][0] = lenmax


    # print
    for k in range(road_len):
        line_x = column(x, 0)
        line_v = column(v, 0)
        if k in line_x:
            ind = line_x.index(k)
            sys.stdout.write('(%d)' % (line_x[ind]))
            sys.stdout.write('%d' % (line_v[ind]))
        else: sys.stdout.write('.')
    sys.stdout.write('\n')
    sys.stdout.write('debug end\n')


    for i in range(time):
        for j in range(lens):
            #(0) determine p
            p = rand(v[j][i],b[j][i],t[i],ts)
            b[j][i+1] = 0
            #(1) acceleration
            if (b[j+1][i] == 0 and b[j][i] == 0) or (t[i] > ts):
                v[j][i+1] = min(v[j][i], vmax)
            #(2) breaking rule
            d[j] = x[j+1][i] - x[j][i]
            deff[j] = d[j] + max (min (d[j+1],v[j+1][i]) -gap_safe, 0)
            t[j] = min(d[j] / (0.000001 + v[j][i]), ts)
            v[j][i+1] = min(deff[j], v[j][i])
            if v[j][i+1] < 0:
                sys.stdout.write('%d %d %d %d, ' % (j, i, x[j+1][i], x[j][i]))
                sys.stdout.write('%d %d %d %d' % (d[j],deff[j],
                    t[j],v[j][i+1]))
                sys.exit(0)
            if v[j][i+1] < v[j][i]:
                b[j][i+1] = 1

            #(3) randomization and braking
            if random() < p:
                v[j][i+1] = max(v[j][i+1] -1, 0)
                if p == pb: b[j][i+1] = 1
            #(4) car motion
            x[j][i+1] = x[j][i] + v[j][i+1]
        
            
        #for k in range(lens):
        #    if x[k][i] >  lenmax: x[k][i] -= lenmax
            
        # sort by x[n]
        for k in range(lens):
            for l in range(k+1,lens):
                if x[k][i] > x[l][i]:
                    x[k][i],x[l][i] = x[l][i],x[k][i]
                    v[k][i],v[l][i] = v[l][i],v[k][i]
                    b[k][i],v[l][i] = b[l][i],v[k][i]
                    d[k],d[l] = d[l],d[k]
                    t[k],t[l] = t[l],t[k]
                    deff[k],deff[l] = deff[l],deff[k]
        # print
        for k in range(road_len):
            line_x = column(x, i)
            line_v = column(v, i)
            if k in line_x:
                ind = line_x.index(k)
                sys.stdout.write('(%d)' % ind)
                sys.stdout.write('%d' % (line_v[ind]))
            else: sys.stdout.write('.')
        sys.stdout.write('\n')


if __name__ == '__main__':
    main()

