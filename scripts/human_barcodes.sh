#!/bin/bash

awk 'NR>1 && $7>=0.8 && $3>=5 {print "CB:Z:" $2}' $1



