#!/bin/env bash
for i in 0.08 0.09 0.1 0.11 0.12
do
    #echo $i
    pypy varying_p_d.py $i
done
