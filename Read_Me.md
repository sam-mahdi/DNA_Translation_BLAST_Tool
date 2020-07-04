This tool takes a sequence input, translates it, and runs BLAST to determine the identity of the sequence. It can determine forward and reverse sequences, additionally it will accept both and combine the 2 translated portion at their overlapping point. 

Written in Python3, uses selenium and google chrome webdriver. 

To use, simply type in the the script name, -f flag for forward, -r for reverse (if both -f and then -r). 
for both
```python DBT.py -f forward_sequence.txt -r reverse sequence.txt```
for forward/reverse individually 
```python DBT.py -f forward_sequence.txt```
```python DBT.py -r reverse.sequence.txt```

Output will consist of any reading frames found, and you then will choose which sequence to use for BLAST. You can also choose alignment, which will compare your sequence with a predicted sequence, obtained from a file containing what your sequence should, and prints out any amino acids that don't align, and the % aligned. 

Additionally, an option is presented if you wish to import sequence into expasy and calculate pI, molecular weight, and exctinction coefficient, as well as save your translated sequence as a txt file. 
