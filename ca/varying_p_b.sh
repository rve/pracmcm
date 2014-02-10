#!/bin/env bash
for i in 0.86 0.90 0.94 0.99
do
    #echo $i
    pypy varying_p_b.py $i
done
