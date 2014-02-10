#!/bin/env bash
for i in {1..13}
do
    #echo $i
    pypy varying_v_max.py $i
done
