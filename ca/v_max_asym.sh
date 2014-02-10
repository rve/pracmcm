#!/bin/env bash
for i in {1..13}
do
    pypy v_max_asym.py $i
done
