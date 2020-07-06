from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys

dna_codon_dict={'TTT':'F','TTC':'F',
                'TTA':'L','TTG':'L',
                'CTT':'L','CTC':'L',
                'CTA':'L','CTG':'L',
                'ATT':'I','ATC':'I',
                'ATA':'I','ATG':'M',
                'GTT':'V','GTC':'V',
                'GTA':'V','GTG':'V',
                'TCT':'S','TCC':'S',
                'TCA':'S','TCG':'S',
                'CCT':'P','CCC':'P',
                'CCA':'P','CCG':'P',
                'ACT':'T','ACC':'T',
                'ACA':'T','ACG':'T',
                'GCT':'A','GCC':'A',
                'GCA':'A','GCG':'A',
                'TAT':'Y','TAC':'Y',
                'CAT':'H','CAC':'H',
                'CAA':'Q','CAG':'Q',
                'AAT':'N','AAC':'N',
                'AAA':'K','AAG':'K',
                'GAT':'D','GAC':'D',
                'GAA':'E','GAG':'E',
                'TGT':'C','TGC':'C',
                'TGG':'W','CGT':'R',
                'CGC':'R','CGA':'R',
                'CGG':'R','AGT':'S',
                'AGC':'S','AGA':'R',
                'AGG':'R','GGT':'G',
                'GGC':'G','GGA':'G',
                'GGG':'G'}


DNA_complement_dict={'A':'T',
                     'T':'A',
                     'G':'C',
                     'C':'G',
                     'N':'N'}

def load_file(files):
    codon_list=[]
    with open(files) as seq_result:
        for lines in seq_result:
            if lines.startswith('>') is True:
                continue
            remove_white_spaces=lines.strip().upper()
            for codon in remove_white_spaces:
                codon_list.append(codon)
    return codon_list

def rev(files):
    reverse_codon_list=[]
    codon_list=load_file(files)
    codon_list.reverse()
    for codons in codon_list:
        reversed_codon=DNA_complement_dict[codons]
        reverse_codon_list.append(reversed_codon)
    return reverse_codon_list

def codon_translation(global_codon_list):
    codon_counter=0
    codon_triple_list=[]
    open_reading_frame_lists=[[],[],[],]
    for i in range(3):
        open_reading_frame_count=1
        codon_triple_list.clear()
        codon_counter=0
        for codons in global_codon_list:
            if open_reading_frame_count>=(i+1):
                codon_counter+=1
                codon_triple_list.append(codons)
                if codon_counter == 3:
                    codon_counter=0
                    join_codons=''.join(codon_triple_list)
                    try:
                        amino_acid=dna_codon_dict[join_codons]
                        open_reading_frame_lists[i].append(amino_acid)
                    except:
                        pass
                    if join_codons in {'TAA','TAG','TGA'}:
                        open_reading_frame_lists[i].append('X')
                    codon_triple_list.clear()
            else:
                open_reading_frame_count+=1
    return open_reading_frame_lists

def find_open_reading_frames(global_codon_list):
    sequences_to_search=[]
    sequence_to_add_to_search_list=[]
    add_to_string=False
    for open_reading_frames in codon_translation(global_codon_list):
        for amino_acids in open_reading_frames:
            if amino_acids == 'M':
                add_to_string=True
            if add_to_string is True:
                sequence_to_add_to_search_list.append(amino_acids)
                if amino_acids == 'X':
                    add_to_string=False
                    if len(sequence_to_add_to_search_list)>20:
                        sequences_to_search.append(''.join(sequence_to_add_to_search_list))
                        sequence_to_add_to_search_list.clear()
                    else:
                        sequence_to_add_to_search_list.clear()
    return sequences_to_search

def forward_loop():
    files=sys.argv[2]
    forward_flag=False
    if sys.argv[1] == '-f':
        forward_flag=True
    if forward_flag is True:
        codon_list=load_file(files)
        return codon_list

def reverse_loop():
    if sys.argv[1] == '-f':
        revsere_flag=False
        try:
            if sys.argv[3] == '-r':
                files=sys.argv[4]
                reverse_flag=True
            if reverse_flag is True:
                codon_list=rev(files)
                return codon_list
        except:
            pass
    else:
        files=sys.argv[2]
        reverse_flag=False
        if sys.argv[1] == '-r':
            reverse_flag=True
        if reverse_flag is True:
            codon_list=rev(files)
            return codon_list



def overlay(sequence_list1,sequence_list2):
    new_list1=[word for line in sequence_list1 for word in line]
    new_list2=[word for line in sequence_list2 for word in line]
    temp_list=[]
    modified_list1=[]
    counter=0
    for x in new_list1:
        temp_list.append(x)
        modified_list1.append(x)
        counter+=1
        if counter >= 5:
            if temp_list == new_list2[0:5]:
                break
            else:
                temp_list.pop((0))

    del new_list2[0:5]
    return ''.join(modified_list1+new_list2)


sequence_list1=[]
sequence_list2=[]
global_codon_list=[]
def create_sequence():
    global global_codon_list
    global sequence_list1
    global sequence_list2
    if sys.argv[1] == '-f':
        global_codon_list=forward_loop()
        sequences_to_search=find_open_reading_frames(global_codon_list)
        sequence_to_search=[]
        for sequence,number in zip(sequences_to_search,range(len(sequences_to_search))):
            print(f'row {number} sequence: {sequence}')
            sequence_to_search.append(sequence)
        pick_sequence_to_search=input('indicate which row # sequence to search: ')
        sequence_list1.append(sequence_to_search[int(pick_sequence_to_search)])
        try:
            if sys.argv[3] == '-r':
                global_codon_list=reverse_loop()
                sequences_to_search=find_open_reading_frames(global_codon_list)
                sequence_to_search=[]
                for sequence,number in zip(sequences_to_search,range(len(sequences_to_search))):
                    print(f'row {number} sequence: {sequence}')
                    sequence_to_search.append(sequence)
                pick_sequence_to_search=input('indicate which row # sequence to search: ')
                sequence_list2.append(sequence_to_search[int(pick_sequence_to_search)])
        except:
            pass
    else:
        sequence_to_search=[]
        global_codon_list=reverse_loop()
        sequences_to_search=find_open_reading_frames(global_codon_list)
        for sequence,number in zip(sequences_to_search,range(len(sequences_to_search))):
            print(f'row {number} sequence: {sequence}')
            sequence_to_search.append(sequence)
        pick_sequence_to_search=input('indicate which row # sequence to search: ')
        sequence_list1.append(sequence_to_search[int(pick_sequence_to_search)])

def use_seq_comparison(sequence_list1,sequence_list2):
    list_conversion=list((overlay(sequence_list1,sequence_list2)))
    predicted_sequence_response=input('please type in the name of predicted sequence file: ')
    predicted_sequence=[]
    with open(predicted_sequence_response) as prediction_file:
        for lines in prediction_file:
            remove_white_spaces=lines.strip()
            for amino_acids in remove_white_spaces:
                predicted_sequence.append(amino_acids)

    counter=0
    seq_match=[]
    matched_amino_acids=[]
    unmatched_head_amino_acids=[]
    flag=False
    for amino_acids in list_conversion:
        counter+=1
        seq_match.append(amino_acids)
        if counter >= 5:
            if seq_match == predicted_sequence[0:5]:
                flag=True
            else:
                if flag is True:
                    matched_amino_acids.append(amino_acids)
                else:
                    seq_match.pop(0)
                    unmatched_head_amino_acids.append(amino_acids)
    combined_list=seq_match[0:5]+matched_amino_acids
    count=len(unmatched_head_amino_acids)
    unmatched=0
    for stuff,stuffs in zip(predicted_sequence,combined_list):
        count+=1
        if stuff != stuffs:
            print(f'amino acid {count}{stuffs} different or missing from predicted')
            unmatched+=1

    print(f'{(count-unmatched)/count*100} % match')


def BLAST(sequence_list1,sequence_list2):
    driver = webdriver.Chrome()
    driver.get('https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome')
    fill_box = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/div[3]/fieldset/div[1]/div[1]/textarea')
    fill_box.clear()
    fill_box.send_keys(overlay(sequence_list1,sequence_list2))
    sumbit_button=driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/div[6]/div/div[1]/div[1]/input')
    sumbit_button.click()
    while True:
        try:
            tmp = driver.title
        except:
            break

def expasy(sequence_list1,sequence_list2):
    driver = webdriver.Chrome()
    driver.get('https://web.expasy.org/protparam/')
    fill_box = driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/textarea')
    fill_box.clear()
    fill_box.send_keys(overlay(sequence_list1,sequence_list2))
    sumbit_button=driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/p[1]/input[2]')
    sumbit_button.click()
    while True:
        try:
            tmp = driver.title
        except:
            print('program done')
            break

def write_sequence_file(sequence_list1,sequence_list2):
    with open (file_name,'w') as filename:
        filename.write(overlay(sequence_list1,sequence_list2))

def main_loop():
    create_sequence()
    choice=input('would you like to use BLAST, or sequence alignment to confirm sequence identity (type BLAST or alignment): ')
    if choice == 'alignment':
        use_seq_comparison(sequence_list1,sequence_list2)
    else:
        BLAST(sequence_list1,sequence_list2)
    write_file=input('would you like to save your translated sequence? (y/n) ')
    if write_file == 'y':
        file_name=input('type in name of file, click enter when done: ')
        write_sequence_file(sequence_list1,sequence_list2)
    generate_expasy_question=input('would you like to generate an expasy file? (y/n): ')
    if generate_expasy_question == 'y':
        expasy(sequence_list1,sequence_list2)
    else:
        print('program done')

main_loop()
