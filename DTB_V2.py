from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import sys

user_input=sys.argv[1]
def get_sequence():
    start_time = time.time()
    print('Starting Program')
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    options.add_argument('log-level=3')
    options.add_argument('--proxy-server="direct://"')
    options.add_argument('--proxy-bypass-list=*')
    driver = webdriver.Chrome(options=options)
    print('Logging in')
    driver.get('https://clims4.genewiz.com/RegisterAccount/Login')
    fill_box = driver.find_element_by_xpath('//*[@id="LoginName"]')
    fill_box.clear()
    fill_box.send_keys('bezsonova@uchc.edu')
    fill_box = driver.find_element_by_xpath('//*[@id="Password"]')
    fill_box.send_keys('IMibes1')
    driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()
    table = driver.find_element_by_xpath('//*[@id="myOrdersTable"]/tbody')
    driver.find_element_by_xpath('//*[@id="hs-eu-confirmation-button"]').click()
    print('\nCompiling Sequences\n')
    for i,td in enumerate(table.find_elements_by_xpath('//*[@id="myOrdersTable"]/tbody/tr/td[4]'),1):
        number_search=re.match('^\d+-',td.text)
        if td.text == (number_search.group(0)+user_input):
            number_of_samples=driver.find_element_by_xpath(f'//*[@id="myOrdersTable"]/tbody/tr[{i}]/td[9]')
            print(f'\n{number_of_samples.text} samples detected\n')
            print(f'\nEstimated time of completion {int(number_of_samples.text)*2} seconds')
            driver.find_element_by_xpath(f'//*[@id="myOrdersTable"]/tbody/tr[{i}]/td[11]/button').click()
            break

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gwzSngrOrderResultPanelRoot"]/table/tbody')))
    seq_list=[]
    table=driver.find_element_by_xpath('//*[@id="gwzSngrOrderResultPanelRoot"]/table/tbody')
    for x,sequence in enumerate(table.find_elements_by_xpath('//*[@id="gwzSngrOrderResultPanelRoot"]/table/tbody/tr/td[9]'),1):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="gwzSngrOrderResultPanelRoot"]/table/tbody//tr[{x}]/td[9]/span[2]'))).click()
        seq_list.append([(WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='gwzViewResultsModalDialog']/div/div/div[2]/div"))).text)])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gwzViewResultsModalDialog"]/div/div/div[3]/button'))).click()
    print(time.time() - start_time)
    driver.close()
    return seq_list


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
                'GGG':'G','TAA':'X',
                'TAG':'X','TGA':'X'}

DNA_complement_dict={'A':'T',
                     'T':'A',
                     'G':'C',
                     'C':'G',
                     'N':'N'}

def rev(global_codon_list):
    return [DNA_complement_dict[codons] for codons in reversed(global_codon_list)]


def codon_translation(global_codon_list):
    codon_triple_list=[]
    open_reading_frame_lists=[[],[],[],]
    for i,codons in enumerate(open_reading_frame_lists,1):
        codon_triple_list.clear()
        open_reading_frame_count=1
        for codons in global_codon_list:
            if open_reading_frame_count<i:
                open_reading_frame_count+=1
                continue
            codon_triple_list.append(codons)
            if len(codon_triple_list) == 3:
                try:
                    amino_acid=dna_codon_dict[''.join(codon_triple_list)]
                    open_reading_frame_lists[i-1].append(amino_acid)
                except:
                    pass
                codon_triple_list.clear()
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




global_codon_list=[]
sequence_list1=[]
def manual_mode():
    global global_codon_list
    global sequence_list1
    for i,sequence in enumerate(get_sequence()):
        title=re.search(r'^>.*\n',sequence[0])
        remove_title=re.sub(r'^>.*\n','',sequence[0])
        global_codon_list=re.sub(r'\n','',remove_title)
        sequences_to_search=find_open_reading_frames(global_codon_list)
        sequence_to_search=[]
        print(f'\nsample {title.group(0)}')
        for number,sequences in enumerate(sequences_to_search,1):
            print(f'row {number} sequence: {sequences}')
            sequence_to_search.append(sequences)
        pick_sequence_to_search=input('indicate which row # sequence to search, if no match, type "n": ')
        if pick_sequence_to_search != 'n':
            sequence_list1.append(sequence_to_search[int(pick_sequence_to_search)-1])
            questionairre_question=input('would you like to search BLAST and or save your sequence and translated protein? (y/n): ')
            if questionairre_question != 'n':
                questionairre(title)
        else:
            reverse_loop(title)
            if sequence_list1 != []:
                questionairre_question=input('would you like to search BLAST and or save your sequence and translated protein? (y/n): ')
                if questionairre_question != 'n':
                    questionairre(title)

def questionairre(title):
    BLAST_question=input('Would you like to run sequence against BLAST? (y/n): ')
    if BLAST_question != 'n':
        BLAST()
    dna_save_file_question=input('Would you like to save your DNA file?\n If yes, please type in the desired filename, else type "n": ')
    if dna_save_file_question != 'n':
        with open(dna_save_file_question,'w') as dna_file:
            dna_file.write(title.group(0)+global_codon_list)
    protein_save_file_question=input('Would you like to save your translated protein sequence?\nIf yes, please type in the desired filename, else type "n": ')
    if protein_save_file_question !='n':
        with open(protein_save_file_question,'w') as protein_file:
            protein_file.write(title.group(0)+'\n'+(''.join(sequence_list1)))
    expasy_question=input('Would you like to generate an expasy file for your protein? (y/n): ')
    if expasy_question != 'n':
        expasy()


def reverse_loop(title):
    global global_codon_list
    global sequence_list1

    global_codon_list=rev(global_codon_list)
    sequences_to_search=find_open_reading_frames(global_codon_list)
    sequence_to_search=[]
    print(f'sample {title.group(0)}')
    for number,sequence in enumerate(sequences_to_search,1):
        print(f'row {number} sequence: {sequence}')
        sequence_to_search.append(sequence)
    pick_sequence_to_search=input('indicate which row # sequence to search, if no match, type "n": ')
    if pick_sequence_to_search != 'n':
        sequence_list1.append(sequence_to_search[int(pick_sequence_to_search)-1])
    else:
        print('\nYour protein was not found in Sequencing\n')
        sequence_list1.clear()


def BLAST():
    driver = webdriver.Chrome()
    driver.get('https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome')
    fill_box = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/div[3]/fieldset/div[1]/div[1]/textarea')
    fill_box.clear()
    fill_box.send_keys(''.join(sequence_list1))
    sumbit_button=driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/div[6]/div/div[1]/div[1]/input')
    sumbit_button.click()
    while True:
        try:
            tmp = driver.title
        except:
            break
def expasy():
    driver = webdriver.Chrome()
    driver.get('https://web.expasy.org/protparam/')
    fill_box = driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/textarea')
    fill_box.clear()
    fill_box.send_keys(''.join(sequence_list1))
    sumbit_button=driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/p[1]/input[2]')
    sumbit_button.click()
    while True:
        try:
            tmp = driver.title
        except:
            print('program done')
            break

protein_size=100
def find_open_reading_frames_auto_mode(global_codon_list):
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
                    if len(sequence_to_add_to_search_list)>protein_size:
                        sequences_to_search.append(''.join(sequence_to_add_to_search_list))
                        sequence_to_add_to_search_list.clear()
                    else:
                        sequence_to_add_to_search_list.clear()
    return sequences_to_search

def reverse_loop_auto(title):
    global global_codon_list
    global sequence_list1

    global_codon_list=rev(global_codon_list)
    sequences_to_search=find_open_reading_frames_auto_mode(global_codon_list)
    sequence_to_search=[]
    print(f'sample {title.group(0)}')
    for number,sequence in enumerate(sequences_to_search,1):
        print(f'row {number} sequence: {sequence}')
        sequence_to_search.append(sequence)
    if sequence_to_search == []:
        print(f'{title.group(0)} not found')

def auto_mode():
    global global_codon_list
    global sequence_list1
    for i,sequence in enumerate(get_sequence()):
        title=re.search(r'^>.*\n',sequence[0])
        remove_title=re.sub(r'^>.*\n','',sequence[0])
        global_codon_list=re.sub(r'\n','',remove_title)
        sequences_to_search=find_open_reading_frames_auto_mode(global_codon_list)
        sequence_to_search=[]
        print(f'\nsample {title.group(0)}')
        for number,sequences in enumerate(sequences_to_search,1):
            print(f'row {number} sequence: {sequences}')
            sequence_to_search.append(sequences)
        if sequences_to_search == []:
            print('\nno forward sequence found, checking reverse sequence\n')
            reverse_loop_auto(title)

def main_loop():
    auto_or_manual_question=input('would you like auto-mode, or manual mode? (type auto for auto-mode, manual for maual mode): ')
    if auto_or_manual_question == 'auto':
        auto_mode()
    else:
        manual_mode()


main_loop()
