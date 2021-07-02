#!/bin/bash

sbatch /project2/gilad/kenneth/Pipelines/HumanChimp/snakemake_solo.batch \
"-s /project2/gilad/kenneth/Pipelines/HumanChimp/Snakefile_solo" \
"--cluster-config /project2/gilad/kenneth/Pipelines/HumanChimp/cluster_solo.json" \
"--configfile /project2/gilad/kenneth/HumanChimpEBs/Batch1/config.yaml" \
"--config proj_dir=/project2/gilad/kenneth/HumanChimpEBs/Batch1/"
