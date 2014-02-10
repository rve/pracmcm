#!/bin/env bash
for i in {1..13}
do
    pypy v_max_sym.py $i
done
