import sys
import pandas as pd
import pysam
import numpy as np

input_human_file = sys.argv[1]
input_chimp_file = sys.argv[2]
output_file = sys.argv[3]

bam_human = pysam.AlignmentFile(input_human_file, "rb")
bam_chimp = pysam.AlignmentFile(input_chimp_file, "rb")

def collect_discordant_reads(bam_human, bam_chimp):
    human = bam_human.fetch(until_eof = True)
    chimp = bam_chimp.fetch(until_eof = True)
    barcode          = []
    chimp_score      = []
    human_score      = []
    chimp_mismatches = []
    human_mismatches = []
    i = 0
    out = pd.DataFrame({'barcode': barcode, 'human_score' : human_score, 'chimp_score': chimp_score, 'human_mismatches' : human_mismatches, 'chimp_mismatches' : chimp_mismatches})
    for read_human, read_chimp in zip(human, chimp):
        if read_human.mapping_quality == 255 or read_chimp.mapping_quality==255: # at least one read matches uniquely
            i += 1
            this_barcode = read_human.get_tag('CR')
            human_nM     = read_human.get_tag('nM')
            chimp_nM     = read_chimp.get_tag('nM')
            if human_nM != chimp_nM:
                if human_nM > chimp_nM: # there are more mismatches in human than chimp
                    chimp_score.append(1)
                    human_score.append(0)
                else: # there are more mismatches in chimp than human. It is human.
                    chimp_score.append(0)
                    human_score.append(1)
                barcode.append(this_barcode)
                chimp_mismatches.append(chimp_nM)
                human_mismatches.append(human_nM)
            if i == 1000000:
            	add = pd.DataFrame({'barcode': barcode, 'human_score' : human_score, 'chimp_score': chimp_score, 'human_mismatches' : human_mismatches, 'chimp_mismatches' : chimp_mismatches})
            	out = out.append(add)
            	out = out.groupby(['barcode'], as_index=False)[['human_score', 'chimp_score', 'human_mismatches', 'chimp_mismatches']].sum()
            	i = 0
            	barcode          = []
            	chimp_score      = []
            	human_score      = []
            	chimp_mismatches = []
            	human_mismatches = []
    return out


#species score: 1 for human 0 for panTro
#groupby Cell barcode and sum each of the two column
def get_species_score(df):
    CB_df = df.groupby(['barcode'], as_index=False)[['human_score', 'chimp_score', 'human_mismatches', 'chimp_mismatches']].sum()
    CB_df['hg_specificity_score'] = CB_df['human_score'] / (CB_df['human_score'] + CB_df['chimp_score'])
    return CB_df

discordant_df = collect_discordant_reads(bam_human, bam_chimp)

assigned_species = get_species_score(discordant_df)

assigned_species.to_csv(output_file, sep = '\t', header = True)
