#!/bin/env bash
for i in {1..13}
do
    pypy beta.py $i
done
