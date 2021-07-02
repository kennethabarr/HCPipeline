#!/bin/bash

/project2/gilad/kenneth/software/samtools-1.10/samtools view -b -@ 8 -D CB:$1 -o $2 $3 
/project2/gilad/kenneth/software/samtools-1.10/samtools index -@ 8 $2 