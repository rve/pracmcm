#!/bin/env bash
for i in 0.40 0.45 0.50 0.55 0.60
do
    #echo $i
    pypy p_0.py $i
done
