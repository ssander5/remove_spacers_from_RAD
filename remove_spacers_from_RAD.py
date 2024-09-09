#!/usr/bin/python

##################################
# Written by Sheri Sanders
# Jun 20, 2024
# with the help of ChatGPT :)
##################################

import argparse
import re

def process_fastq(input_file1, input_file2, output_file_matched1, output_file_matched2, output_file_nonmatched1, output_file_nonmatched2):
    #patterns = ["^TG", "^ATC", "^GTTCC", "^CCGCGG"]  #patterns updated per JL email Sept 9, 2024
    patterns = ["^GG","^CTCAG","^AGACAC","^TCGTCTGC"]
    patterns_regex = "|".join(patterns)
    
    with open(input_file1, 'r') as f_in1, open(input_file2, 'r') as f_in2, \
         open(output_file_matched1, 'w') as f_out_matched1, open(output_file_matched2, 'w') as f_out_matched2, \
         open(output_file_nonmatched1, 'w') as f_out_nonmatched1, open(output_file_nonmatched2, 'w') as f_out_nonmatched2:

        while True:
            # Read four lines at a time from both input files
            header1 = f_in1.readline().strip()
            header2 = f_in2.readline().strip()

            if not header1 or not header2:
                break  # End of files

            seq_line1 = f_in1.readline().strip()
            plus_line1 = f_in1.readline().strip()
            qual_line1 = f_in1.readline().strip()

            seq_line2 = f_in2.readline().strip()
            plus_line2 = f_in2.readline().strip()
            qual_line2 = f_in2.readline().strip()

            # Check if they are valid FASTQ records
            if not (header1.startswith('@') and plus_line1.startswith('+') and
                    header2.startswith('@') and plus_line2.startswith('+')):
                continue  # Not a valid pair of FASTQ records, skip

            # Search for the specific patterns followed by "TAA" in seq_line1
            match1 = re.search(fr'({"|".join(patterns)})TAA', seq_line1)

            if seq_line1.startswith("TAA"):
                # Write matched sequences to output files
                f_out_matched1.write(f'{header1}\n')
                f_out_matched1.write(f'{seq_line1}\n')
                f_out_matched1.write(f'{plus_line1}\n')
                f_out_matched1.write(f'{qual_line1}\n')

                f_out_matched2.write(f'{header2}\n')
                f_out_matched2.write(f'{seq_line2}\n')
                f_out_matched2.write(f'{plus_line2}\n')
                f_out_matched2.write(f'{qual_line2}\n')
            elif match1:
                prefix_length = len(match1.group(1))
                #print(match1.group(1))
                #print(seq_line1)
                #print("PASS \n")
                trimmed_seq_line1 = seq_line1[:match1.start(1)] + seq_line1[match1.end(0)-3:]
                trimmed_qual_line1 = qual_line1[prefix_length:]

                # Write matched sequences to output files
                f_out_matched1.write(f'{header1}\n')
                f_out_matched1.write(f'{trimmed_seq_line1}\n')  # Keep the matched pattern and "TAA"
                f_out_matched1.write(f'{plus_line1}\n')
                f_out_matched1.write(f'{trimmed_qual_line1}\n')  # Trim the quality line accordingly

                f_out_matched2.write(f'{header2}\n')
                f_out_matched2.write(f'{seq_line2}\n')
                f_out_matched2.write(f'{plus_line2}\n')
                f_out_matched2.write(f'{qual_line2}\n')
            else:
                # Write non-matching sequences to output files
                #print(seq_line1)
                #print("FAIL \n")

                f_out_nonmatched1.write(f'{header1}\n')
                f_out_nonmatched1.write(f'{seq_line1}\n')
                f_out_nonmatched1.write(f'{plus_line1}\n')
                f_out_nonmatched1.write(f'{qual_line1}\n')

                f_out_nonmatched2.write(f'{header2}\n')
                f_out_nonmatched2.write(f'{seq_line2}\n')
                f_out_nonmatched2.write(f'{plus_line2}\n')
                f_out_nonmatched2.write(f'{qual_line2}\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process paired-end FASTQ files and modify sequences.')
    parser.add_argument('input_file1', help='Input FASTQ file (read 1)')
    parser.add_argument('input_file2', help='Input FASTQ file (read 2)')
    parser.add_argument('-m1', '--output-matched1', help='Output file for matched sequences from read 1 (default: matched1.fastq)', default='matched1.fastq')
    parser.add_argument('-m2', '--output-matched2', help='Output file for matched sequences from read 2 (default: matched2.fastq)', default='matched2.fastq')
    parser.add_argument('-n1', '--output-nonmatched1', help='Output file for non-matching sequences from read 1 (default: nonmatched1.fastq)', default='nonmatched1.fastq')
    parser.add_argument('-n2', '--output-nonmatched2', help='Output file for non-matching sequences from read 2 (default: nonmatched2.fastq)', default='nonmatched2.fastq')
    
    args = parser.parse_args()
    input_file1 = args.input_file1
    input_file2 = args.input_file2
    output_file_matched1 = args.output_matched1
    output_file_matched2 = args.output_matched2
    output_file_nonmatched1 = args.output_nonmatched1
    output_file_nonmatched2 = args.output_nonmatched2
    
    process_fastq(input_file1, input_file2, output_file_matched1, output_file_matched2, output_file_nonmatched1, output_file_nonmatched2)
    print(f'Processed paired-end FASTQ files "{input_file1}" and "{input_file2}". '
          f'Matched sequences written to "{output_file_matched1}" and "{output_file_matched2}". '
          f'Non-matching sequences written to "{output_file_nonmatched1}" and "{output_file_nonmatched2}".')
