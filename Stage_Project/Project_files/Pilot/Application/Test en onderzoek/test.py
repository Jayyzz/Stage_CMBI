import os
pathpdb = "/mnt/cmbi4/pdb/flat"
pdbent = []
nothere = []
def pdbwalk():
    for file in os.listdir(pathpdb):
        filext = os.path.splitext(file)[0]  #Filename without extention
        filename = filext[3:]               #Filename without the "PDB"
        pdbent.append(filename)             #list with all filenames of pdb
    mapsearch(pdbent, 'bdb', '/mnt/cmbi4')


def mapsearch(pdbent, databank , data_root):
    for entry in pdbent:
        # TODO: '{}'.format() = string formatting
        normal_path = '{}/{}/{}/{}/{}.{}'.format(data_root, databank, entry[1:3], entry, entry, databank)
        why_not_path = '{}/{}/{}/{}/{}.{}'.format(data_root, databank, entry[1:3], entry, entry, 'whynot')
        if not os.path.exists(normal_path):
            if not os.path.exists(why_not_path):
                nothere.append(entry)
    return nothere
pdbwalk()
