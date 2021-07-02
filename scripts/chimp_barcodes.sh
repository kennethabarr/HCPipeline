#!/bin/bash

awk 'NR>1 && $7<=0.2 && $4>=5 {print "CB:Z:" $2}' $1


