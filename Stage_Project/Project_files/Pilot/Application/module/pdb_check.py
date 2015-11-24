import os
import csv
count = {}
parse = []
pathpdb = "/mnt/cmbi4/pdb/flat" #location of the map with all the psb files
#pathpdb = "/home/jayligt/Project_files/Pdb"

def fileopener():
    
    csvfile =  open('/home/jayligt/Project_files/Pilot/Application/module/wegschrijf.csv', 'wb')
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(['id','remark','atom'])
    for file in os.listdir(pathpdb):
        filext = os.path.splitext(file)[0]  #Filename without extention
        filename = filext[3:]               #Filename without the "PDB"
        openfile = open (pathpdb+"/"+file)
        pdbcount(openfile , filename, csvwriter)
    print "Klaar!"
##    print parse

def pdbcount(openfile, filename, csvwriter):
    remark = 0
    atom = 0
    count = {}
    for line in openfile:
        #splitline = line.split("\t")

        if line.startswith("REMARK"):
            remark +=1
        elif line.startswith("ATOM  "):
            atom +=1
        elif line.startswith("HETATM"):
            atom +=1

    csvwriter.writerow([filename,remark,atom])
    
##    count["id"]     =filename
##    count["remark"] =remark
##    count["atom"]   =atom
##    parse.append(count)
    
    
fileopener()
