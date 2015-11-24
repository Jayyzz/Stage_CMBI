import os
dssp = []
hssp = []
pathdssp = "/mnt/cmbi4/dssp"
pathhssp = "/mnt/cmbi4/hssp3"

for file in os.listdir(pathdssp):
        filename = os.path.splitext(file)[0]#Filename without extention
        dssp.append(filename)               #list with all filenames of dssp

for file in os.listdir(pathhssp):
        filext = os.path.splitext(file)[0]  #Filename without extention
        filename = filext[:-5]
        hssp.append(filename)               #list with all filenames of hssp

set1 = set(hssp)
set2 = set(dssp)

onlyInHSSP = set1- set2

print onlyInHSSP

if onlyInHSSP != set([]):
    print (list(onlyInHSSP))
