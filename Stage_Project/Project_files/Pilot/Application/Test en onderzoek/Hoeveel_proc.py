import os
pdbent = []
pathpdb = "/mnt/cmbi4/pdb/flat"
count = 0

for file in os.listdir(pathpdb):
        filext = os.path.splitext(file)[0]  #Filename without extention
        filename = filext[3:]               #Filename without the "PDB"
        pdbent.append(filename)             #list with all filenames of pdb

for entry in pdbent:
    count +=1
    if entry == "1zzj":
        print count
    

