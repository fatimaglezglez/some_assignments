## IMPORTS
import subprocess
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna, generic_protein



## FUNCTION DEFINITIONS
def type(file_name): # fasta file
    file = open(file_name, 'r')
    lines = file.readlines()
    file.close()
    sequ = Seq(lines[1])
    if sequ == Seq(lines[1], generic_protein): ## it should be true for both prot and dna
            if sequ == Seq(lines[1], generic_dna):
                type = 'nucleotide'
            else:
                type = 'protein'
    else:
        type = 'ERROR'
    return type

def type_seq(seq): # seq
        if seq == Seq(seq, generic_protein): ## it should be true for both prot and dna
                if seq == Seq(seq, generic_dna):
                    type = 'nucleotide'
                else:
                    type = 'protein'
        else:
            type = 'ERROR'
        return type


## telling the user what they can do with this program
print('This program will enable you to do any BLAST (Basic Local Alignment Search Tool) analysis you desire without the need of a browser. ')


## STEP 1: what is the database


## REMOVE WHILES AND CHANGE FOR ELSE SAYING YOU MUST ANSWER Y OR N AND EXIT

# database
valid_answer = True
remote = False
while valid_answer:
    own = input ('Do you want to create your own database? (y/n) If you do not, you can use an existing one. ').lower()
    if own == 'y':
        # creation of database with makeblastdb
        own_file = input ('Do you have a file containing the sequences for your database in fasta format? (y/n) ').lower()
        if own_file == 'y':
            database_file = input('Plase, provide the name of the file containing the sequences for the database in fasta format. \nBe sure that the file is located in your current working directory or that you provide its full path: ')
            database_name = database_file.replace('.fasta', '').replace('.fa', '')
            database_type = type ('database_file')
            subprocess.run('makeblastdb -in %s -dbtype %s -out %s'%(database_file, database_type[0:4], database_name), shell=True)

        elif own_file == 'n':
            type = input('Do you want a protein or gene database? (protein/gene) ').lower().replace(' ','')
            if type == 'protein':
                database_type = type
                t = '[Protein Name]'
                gene = input("What protein do you want for your data base? ")
            if type == 'gene':
                t = '[Gene Name]'
                gene = input("What gene do you want for your data base? ")
            org = input("In which organism(s)? ")
            taxtree =  gene + t +'AND "' + org +'" [Organism]'
            database_name = 'database'
            subprocess.run('esearch -db %s -query "%s" | efetch -db %s -format fasta > database.fa' %(type,taxtree,type), shell=True) ## delete afterwards
            if type == 'gene':
                database_type == 'nucleotide'
            subprocess.run('makeblastdb -in database.fa -dbtype %s -out %s'%(database_type[0:4], database_name), shell=True)
        valid_answer = False

    elif own == 'n':
        remote = True
        print('These are the databases provided by NCBI:')
        subprocess.run('update_blastdb.pl --showall [*]', shell=True)
        all_db = subprocess.check_output('update_blastdb.pl --showall [*]', shell=True).decode('utf-8').split('\n')
        database_name = input('Please, type the database you whish to use: ')
        if database_name in all_db:
          valid_answer = False
          database_type = input('Please, specify if your database is made from nucleotide sequences or protein secuences: (nucleotide/protein) ')

        else:
            print('You have to write an existing database from the list shown. ')
    else:
        print("Please, answer with 'y' for yes and 'n' for no. ")


## STEP 2: do the search

        # creation of database with makeblastdb
q_file = input ('Do you have a file containing your query in fasta format? (y/n) ').lower()
if q_file == 'y':
    query_file = input('Plase, provide the name of the file with your query in fasta format. \nBe sure that the file is located in your current working directory or that you provide its full path: ')
    query_type = type(query_file)
elif q_file == 'n':
    stop = True
    while stop:
        q_seq = input('Paste the query sequence here: ').upper()
        print('Be aware that if you paste something other than the sequence the program will run errors. ')
        print('Your sequence is %s'%q_seq)
        correct_seq = input('Do you want to continue? (y/n) ').lower()
        if correct_seq == 'y':
            stop = False
        query_type = type_seq(q_seq)
        file_q = open('query', 'w')
        file_q.write(q_seq)
        file_q.close()
        query_file = 'query'
    else:
        print("Please, answer with 'y' for yes and 'n' for no ")

# what blast for each type
print('You want to analyse a %s query with a %s database'%(query_type,database_type))
if query_type == 'nucleotide':
    if database_type == 'nucleotide':
        analysis = 'blastn'
    elif database_type == 'protein':
        analysis = 'blastx'
elif query_type == 'protein':
    if database_type == 'nucleotide':
        analysis = 'tblastn'
    elif database_type == 'protein':
        analysis = 'blastp'
print('Therefore, the program will be using %s'%analysis)

if remote:
    subprocess.run('%s -db %s -query %s -outfmt 7 -out %s.out -remote'%(analysis,database_name, query_file, query_file), shell=True)
else:
    subprocess.run('%s -db %s -query %s -outfmt 7 -out %s.out'%(analysis,database_name, query_file, query_file), shell=True)
print('A file named %s.out has been created holding the results of the BLAST analysis.'%query_file)

