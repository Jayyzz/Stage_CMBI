import os
import time
start = time.clock() #timer starts here
pdbent, dssp, carb, nores, nucacid, nothere, nothereighter = ([] for i in range(7)) #makes 7 lists with names mentioned before
check = {}
pathdssp = "/mnt/cmbi4/dssp"    #location of the map with all dssp files
pathpdb = "/mnt/cmbi4/pdb/flat" #location of the map with all the pdb files
why_not = open ("/home/jayligt/Project_files/WHY_NOT/DSSPannotated_comments2.txt")   #why_not file with all the pdb entry's with an exception in it of the dssp database.

def namecollector():
    for file in os.listdir(pathpdb):
        filext = os.path.splitext(file)[0]  #Filename without extention
        filename = filext[3:]               #Filename without the "PDB"
        pdbent.append(filename)             #list with all filenames of pdb
        
    for file in os.listdir(pathdssp):
        filename = os.path.splitext(file)[0]#Filename without extention
        dssp.append(filename)               #list with all filenames of dssp

    dsspcheck()
    
def dsspcheck():
    for entry in pdbent:
        if entry not in dssp:
            nothere.append(entry)
            
    why_notcheck()
    
def why_notcheck():
    for line in why_not:
        #All lines with no PDB:
        if "Carbohydrates only:" in line:
            status = "carbo"
        elif "No residues with complete backbone:" in line:
            status = "nobb"
        elif "Nucleic acids only:" in line:
            status = "nuc"
        #PDB lines:
        else:
            split = line.split(',')
            check[split[1].rstrip('\n')] = [status]   #removes "DSSP" and "\n" and takes the why_not status with it.

    for entry in nothere:
        if entry in check:                  #takes the why_not status and checks it where it belongs.
            if check[entry] == ['carbo']:
                carb.append(entry)
            elif check[entry] == ['nobb']:
                nores.append(entry)
            elif check[entry] == ['nuc']:
                nucacid.append(entry)
            else:
                print "Onbekende why_not exceptie"  #if the entry is there but doesn't belong in one of those 3 above.
            
        else:
            nothereighter.append(entry)
##    print carb
##    print nores
##    print nucacid
    print nothereighter
    end = time.clock()            #timer ends here.
    print end - start

namecollector()
        
