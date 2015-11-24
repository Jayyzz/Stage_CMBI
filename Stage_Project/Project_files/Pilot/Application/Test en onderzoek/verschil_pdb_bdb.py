import os
pdbent = []
pathpdb = "/mnt/cmbi4/pdb/flat"

for file in os.listdir(pathpdb):
        filext = os.path.splitext(file)[0]  #Filename without extention
        filename = filext[3:]               #Filename without the "PDB"
        pdbent.append(filename)             #list with all filenames of pdb

for entry in pdbent:
    try:
        why_not_path = ('/mnt/cmbi4/bdb/{}/{}/{}.whynot'.format(entry[1:3], entry, entry))
        if not os.path.exists(why_not_path): 
            pdb = open('/mnt/cmbi4/pdb/flat/pdb{}.ent'.format(entry))
            bdb = open('/mnt/cmbi4/bdb/{}/{}/{}.bdb'.format(entry[1:3], entry, entry))
    except IOError:            
        print "Kan niet entry "+entry+" vinden"
    for x, y in zip(pdb, bdb):
        x = x.strip()
        y = y.strip()
        if x != y:
                print y
##            if "REMARK   4" in x:
##                print("{0}".format(x[11:15]))
print "KLAAR!"
