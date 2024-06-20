# remove_spacers_from_RAD
Removing custom spacers for our new RAD library protocol Jun 2024

Note, this is currently designed only for TAA (Msel) cut sites, with custom spacers listed below:
^(TAA)
^TG(TAA)
^ATC(TAA)
^GTTCC(TAA)
^CCGCGG(TAA)

This initial version also assumes paired reads.  If you need to run it on single reads, simply input the same file for input1 and input2, and delete the second outputs.  e.g.
./remove_spacers_from_RAD.py first.mod.fq first.mod.fq -m1 pass.1.fq -m2 pass.2.fq -n1 fail.1.fq -n2 fail.2.fq
   Processed paired-end FASTQ files "first.mod.fq" and "first.mod.fq". Matched sequences written to "pass.1.fq" and "pass.2.fq". Non-matching sequences written to "fail.1.fq" and "fail.2.fq".
   pass.2.fq and fail.2.fq can be deleted.

To do:
Add handling if there is no second read (see above for current fix)
Add handling for other enzymes as spacers are designed
