import os
import time
import sqlite3
#from flask_debugtoolbar import DebugToolbarExtension
from contextlib import closing

pdbent, dssp, hssp ,carb, nores, nucacid, nothere, nothereighter = ([] for i in range(8)) #makes 7 lists with names mentioned before
check = {}
pathdssp = "/mnt/cmbi4/dssp"    #location of the map with all the dssp files
pathpdb = "/mnt/cmbi4/pdb/flat" #location of the map with all the pdb files
pathhssp = "/mnt/cmbi4/hssp3"    #location of the map with all the hssp files
why_not_dssp = open ("/home/jayligt/Project_files/WHY_NOT/DSSPannotated_comments2.txt")   #why_not file with all the pdb entry's with an exception in it of the dssp database.
why_not_hssp = open ("/home/jayligt/Project_files/WHY_NOT/HSSPannotated_comments.txt")   #why_not file with all the pdb entry's with an exception in it of the hssp database.


def hsspfind():
    for file in os.listdir(pathdssp):
        filename = os.path.splitext(file)[0]#Filename without extention
        dssp.append(filename)               #list with all filenames of dssp

    for file in os.listdir(pathhssp):
        filext = os.path.splitext(file)[0]#Filename without extention
        filename = filext[:-5]
        hssp.append(filename)               #list with all filenames of hssp
    print hssp

    for entry in dssp:
        if entry not in hssp:
            nothere.append(entry)
            
    for line in why_not_hssp:
        #All lines with no PDB:
        if "No hits found:" in line:
            status = "nohit"
        elif "Not enough sequences in PDB file of length 25:" in line:
            status = "notenoughseq"
        elif "empty protein, or no valid complete residues:" in line:
            status = "empty"
        #PDB lines:
        else:
            split = line.split(',')
            check[split[1].rstrip('\n')] = [status]   #removes "HSSP" and "\n" and takes the why_not status with it.

    for entry in nothere:
        if entry in check:                  #takes the why_not status and checks it where it belongs.
            if check[entry] == ['nohit']:
                carb.append(entry)
            elif check[entry] == ['notenoughseq']:
                nores.append(entry)
            elif check[entry] == ['empty']:
                nucacid.append(entry)
            else:
                print "Onbekende why_not exceptie"  #if the entry is there but doesn't belong in one of those 3 above.
            
        else:
            nothereighter.append(entry)
    #print ', ' .join(nothereighter)

hsspfind()
