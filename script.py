#!/usr/bin/python3

## Asigment 2
# B185114
import os
import sys
import subprocess
import re

## SEARCH
prot = input("What protein family do you want to study? ")
org = input("In which organisms? ")
taxtree =  prot+'[Protein Name] AND "' + org +'" [Organism] NOT Partial NOT Predicted'
valid_name = True
while valid_name:
    set_file_name = input('How do you want to name the file containing all the sequences of your search? ').replace(' ', '_')
    for c in set_file_name:
        if not((c == '_') or c.isalnum()):
            print('The name you introduced is not valid.\nPlease do not use any special characters appart from a simple space,\nwhich is transformed into an underscore.')
        else:
            valid_name = False
subprocess.run('esearch -db protein -query "%s" | efetch -db protein -format fasta > %s.fa' %(taxtree,set_file_name), shell=True)
print('All files will be storaged in your working directory.')
print('The results of your seach have been storage in the file %s.fa'%set_file_name)

file = open('%s.fa'%set_file_name, 'r')
seq_lines = file.readlines() #list with \n
file.close()
if seq_lines == []:
    print('\nThere are no results for your search. \nPlease, run the program again with a different search.')
    quit()
full_entries = []
seqs = []
seq = ''
species = []
for line in seq_lines:
    if line[0]== '>':
        full_entries.append(line.split(' ')[0][1:])
        seqs.append(seq)
        seq = ''
        sp = ''
        s = False
        for c in line:
            if c == '[':         ##### NO LO PILLA !!!!!!!!
                s = True
            elif c == ']':
                s = False
            if s:
                sp += c
        species.append(sp[1:])
    else:
        seq += line.strip('\n')
seqs.append(seq)
entry_to_seq = dict(zip(full_entries, seqs[1:]))

print('There are ' +str(len(full_entries))+ ' entries from ' +str(len(list(set(species)))) +' different species: ' + str(list(set(species))))
x = True
while x:
    cont = input('Do you want to continue to the analysis? (y/n): ')
    if cont == 'y':
        x = False
    elif cont == 'n':
        x = False
        quit()
    else:
        print("Please, answer with 'y' for 'yes' or 'n' for 'no'")

# 250 most similar sequences
if len(full_entries) > 250:
    msa = subprocess.check_output('clustalo -i %s.fa --output-order=tree-order'%set_file_name, shell=True).decode('utf-8').split('\n')
    file250 = open('250top_%s.fa'%set_file_name, 'w+')
    s = re.findall(r'>.+\..', msa)
    for i in range(250):
        s[i]
        file250.write(s[i][1:] + '\n' + entry_to_seq[s[i]] + '\n')
    file250.close()
    print('Since your search has more than 250 results, a selection of the most similar 250 sequences has been made and storaged in the file 250top_%s.fa'%set_file_name)

    # aligned sequences and conservation plot
    subprocess.run('clustalo -i 250top_%s.fa -o aligned_250top_%s.msf --outfmt msf'%(set_file_name,set_file_name), shell=True)
    print('The alignment has been made. The results are storaged in the file aligned_250top_%s.msf'%set_file_name)
    subprocess.run("plotcon  aligned_250top_%s.msf -winsize 4 -graph x11"%set_file_name, shell=True)                           DESCOMENTARRRR!!! lo comento por que mi terminal muerwe, no se por que
    subprocess.run("plotcon aligned_250top_%s.msf -auto -winsize 4 -graph svg -goutfile plot_%s"%(set_file_name,set_file_name), shell=True)
    print('The corservarion plot is done and storaged in the file plot_250top_%s.svg'%set_file_name)
else:
    # aligned sequences and conservation plot
    subprocess.run('clustalo -i %s.fa -o aligned_%s.msf --outfmt msf'%(set_file_name,set_file_name), shell=True)
    print('The alignment has been made. The results are storaged in the file aligned_%s.msf'%set_file_name)
    subprocess.run("plotcon aligned_%s.msf -winsize 4 -graph x11"%set_file_name, shell=True)                               DESCOMENTARRRR!!! lo comento por que mi terminal muerwe, no se por que
    subprocess.run("plotcon aligned_%s.msf -auto -winsize 4 -graph svg -goutfile plot_%s"%(set_file_name,set_file_name), shell=True)
    print('The corservarion plot is done and storaged in the file plot_%s.svg'%set_file_name)

# motifs
filemot = open('summary_motifs_%s.txt'%set_file_name, 'w+')
for name in list(entry_to_seq.keys()):
    fileseq = open('%s.txt'%name, 'w+')
    fileseq.write(entry_to_seq[name])
    fileseq.close()
    subprocess.run("patmatmotifs %s.txt -auto -full -outfile motifs_%s.txt"%(name,name), shell=True)
    filem = open('motifs_%s.txt'%name, 'r')
    motifs_lines = filem.readlines() #list with \n
    filem.close()
    filemot.write('Protein ID:' + name + '\t')
    for line in motifs_lines:
        if '# Hit' in line:
            filemot.write(line.strip('# \n') + '\n')
        elif '# Motif' in line:
            filemot.write(line.strip('# \n') + '\t')
        elif '# Count' in line:
            filemot.write(line.strip('# \n') + '\n')
    filemot.write('----------------------------------------------------------------\n')
print('A file named as every protein accesion number has been created containing the protein secuence in it.')
print('A file containing the detailed motifs found for each sequence has been created under the name motif_[protein ID].txt')
print('Also, a file containing a summary of the motifs encountered for all sequences has been storaged named summary_motifs_%s.txt'%set_file_name)

#EXTRA
# pepstats
y = True
while y:
    st = input('Do you want to get the statistics for the proteins in your search? (y/n): ')
    if st == 'y':
        y = False
        for name in list(entry_to_seq.keys()):
            subprocess.run("pepstats %s.txt -auto -outfile %s.pepstats"%(name,name), shell=True)
        print('The files containing the statistics for each protein have been created under the name [protein ID].pepstats')

    elif st == 'n':
        y = False
    else:
        print("Please, answer with 'y' for 'yes' or 'n' for 'no'")

# back-translation
z = True
while z:
    bt = input('Do you want to back-translate the proteins in your search? (y/n): ')
    if bt == 'y':
        z = False
        a = True
        while a:
            amb = input('Do you want to back-translate to a ambiguous nucleotide sequence? (y/n): ')
            if amb == 'y':
                a = False
                for name in list(entry_to_seq.keys()):
                    subprocess.run("backtranambig %s.txt -auto -outfile backtransamb_%s.txt"%(name,name), shell=True)
                print('The files containing the back-translate for each protein have been created under the name backtransamb_[protein ID].txt')
            elif amb == 'n':
                a = False
                for name in list(entry_to_seq.keys()):
                    subprocess.run("backtranseq %s.txt -auto -outfile backtrans_%s.txt"%(name,name), shell=True)
                print('The files containing the back-translate for each protein have been created under the name backtrans_[protein ID].txt')

            else:
                print("Please, answer with 'y' for 'yes' or 'n' for 'no'")
    elif bt == 'n':
        z = False
    else:
        print("Please, answer with 'y' for 'yes' or 'n' for 'no'")

