#!/bin/bash

for name in extractvaspdata makedatajson makefitjson makeintegraljson;
do
    python -m unittest tests/fourier/$name/test_$name.py
done

