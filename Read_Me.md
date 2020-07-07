This is the DNA_Translation_Blast Tool Version 2. 

This version works exclusively with genewhiz (if you have sequences from other sites, use version 1) using Selenium

Designed for Chrome, but you can add your own webdriver if you wish. 

This version will log into Genescript, use the project_id provided to search for your sample, and extract all of the sequenced data. Then it will translate all your sequences, and print them out. 

Auto-Mode uses a size-cut off of 50 amino acids, and is used exclusively to check sequence data. It will only printout protein sequences that are larger than that. It will print out all samples it finds, and end the program. 

If you wish to run BLAST, save your DNA and Protein sequence files, run expasy, use manual mode. It works in a similar way, but prints out all the open reading frames (>above 20 amino acids), and enables you to choose which ones to save/run against BLAST. 

To run, type in program name, followed by project ID ```python DNB_V2.py sample_id```

This version no longer contains overlay mode (it does not combine forward and reverse sequences). May be implemented in future version, for now use DTB_V1 for that. 
