########################
##Auteur: Jay Ligtvoet##
##Versie 1.0          ##
##Bugs: None found    ##
########################

import os
import bz2
hsspent = []
pathpdb = "/mnt/cmbi4/pdb/flat"
pathdssp = "/mnt/cmbi4/dssp"
pathhssp = "/mnt/cmbi4/hssp"
import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)

def aanstuur():                                                 #Aanstuur functie : Hier worden alle andere functies aangeroepen
    startpos1 = ""
    hsspent = hsspwalk()                                        #Alle PDB id's verzamelen die zich bevinden in HSSP
##    for entry in hsspent:
##        if hsspent[0] == "3fi0":
##            break
##        else:
##            print hsspent[0]
##            del hsspent[0]
##    hsspent = ["3fi0", "Bla1" , "bla2"]            
    for entry in hsspent:
        print entry
        AAhssp, Idshssp = hssp(entry)                                    #Door HSSP files lezen en data ophalen (elke file loopt onderstaand proces door)
        
        if "##" in AAhssp:                                      #Als er iets is fout gegaan, staat dat in deze "if" en "elif" en word het proces van deze file afgekapt.
            logging.warning(AAhssp)
        elif "lijn" in AAhssp:
            logging.warning(AAhssp)
        elif "SEQLENGTH" in AAhssp:
            logging.warning(AAhssp)
        else:
            
            AAdssp, Idsdssp = dssp(entry)                       #Als alles goed is met de HSSP file word de DSSP files doorgenomen(met de PDB id's van HSSP)
            if 'hoeveelheid' in AAdssp:                         #Als er hier iets mis gaat word dat weer afgekapt en geprint in de "if" en "elif"
                logging.warning(AAdssp)
            elif 'ID' in AAdssp:
                logging.warning(AAdssp)
            else:
                startposdssp = Idsdssp[0].split()               #startpositie bepalen van de HSSP file(weten bij welke PDB ID deze begint)
                if len(startposdssp) == 1:
                    tussen = startposdssp[0]
                    startposdssp.append(tussen[0:len(startposdssp[0])-1])
                    startposdssp.append(tussen[len(startposdssp[0])-1:len(startposdssp[0])])
                    del startposdssp[0]
                    tussen = []
                AApdb, IdsPdbo , pdbStrand = ReadPDB(entry, startposdssp)     #PDB entry word doorgenomen, met de PDb id's van HSSPs
                if "PDB file" in AApdb:
                    logging.warning(AApdb)
                else:
                    startposhssp = Idshssp[0].split()               #startpositie bepalen van de HSSP file(weten bij welke PDB ID deze begint)
                    if len(startposhssp) == 1:
                        tussen = startposhssp[0]
                        startposhssp.append(tussen[0:len(startposhssp[0])-1])
                        startposhssp.append(tussen[len(startposhssp[0])-1:len(startposhssp[0])])
                        del startposhssp[0]
                    AAhsdb , IdsPdbh = hsdb(entry, startposhssp)    #Bij deze functie word er speciaal gekeken naar de startpositie van de HSSP file. Dit is omdat HSSP niet alles van de PDB entry pakt.
                    if "PDB file" in AAhsdb:
                        logging.warning(AAhsdb)
                    else:
                        check = compare(entry,AAhsdb, AAdssp, AApdb, \
                                    AAhssp, Idshssp, Idsdssp,IdsPdbo,\
                                    IdsPdbh, pdbStrand, startposhssp ,\
                                    startposdssp)#In deze functie word alle inhoud van alle files met elkaar vergeleken. (DSSP met PDB en HSSP met HSDB (aparte PDB inhoud voor HSSP))
                    
                        if "Geen verschillen" not in check:             #Print alleen maar als er een verschil is gevonden tussen de files
                            logging.info(check)


def hssp(entry):
    try:
        hssp_file =("{}/{}.hssp.bz2".format(pathhssp,entry))
    except IOError:
        return "Deze HSSP file is verdwenen("+entry+")", "nope"
    
    bz2_file = bz2.BZ2File(hssp_file)
    found_alignments = False
    readh = False
    first_one = False
    line = None
    AAhssp = []
    startpos3 = []
    lengths = {}
    protein_count = 0
    seq_count = 0
    number_of_allignments = 0
    while True:
        line = bz2_file.readline()
        if line == "":
            break
        line = line.rstrip('\n')
        
            
        if not found_alignments:
            if line.startswith('## ALIGNMENTS'):
                number_of_allignments += 1
                found_alignments = True
                readh = False
                bz2_file.readline()
        else:
            
            # Alignment section ends when we find another comment (probably)
            if line.startswith('##'):
                found_alignments = False
                first_one = False
                continue
            
            if len(line) < 51:
                return entry+" Er is een regel die standaard informatie mist(Regel is kleiner dat 51 char.)"

            if AAhssp == []:
                first_one = True
                
            if first_one == True:
                if line[14:16].islower():                           #Er kunnen ook kleine letters in de aminozuren voorkomen. Dit zijn allemaal Cysteine's. Hier worden ze dus vervangen door de 1 letter code.
                    AAhssp.append("C")
                    startpos3.append(line[7:13])
                else:
                    AAhssp.append(line[14:16])                      #Voeg aminozuur toe bij de lijst genaamd AAhssp. Hier komen alle aminozuren in te staan.
                    startpos3.append(line[7:13])
                if "! " != line[14:16] and "!*" != line[14:16]:
                    seq_count +=1

        if "NALIGN  " in line:                                  #Dit is de hoeveelheid proteinen die hij allignt (Staat bovenaan de file). Dit moet natuurlijk kloppen met de hoeveelheid die in de file staat.
            protein_notation = line[10:15]
        elif "SEQLENGTH  " in line:
            seq_length = line[10:15]                                #Dit gaat over hoe groot de sequentie is.

        if readh == True:
            protein_count += 1
        elif "NR.    ID" in line:
            readh = True
            
    if int(protein_notation) != (protein_count):
        return entry+" HSSP: \nHet aantal lijnen onder ## PROTEINS("+protline+") staan niet gelijk aan het nummer van NALIGN("+str(protcount)+")" , "nope"
    elif int(seq_length) != int(seq_count):
        return entry+" HSSP: \nSEQLENGTH ("+seq_length.replace(" ","")+") komt niet overeen met de lengte van de sequentie onder 'allignment'("+str(seq_count)+")", "nope"

##    import pprint
##    pprint.pprint(lengths)
    bz2_file.close()                                    #Sluit bestand
    return AAhssp, startpos3
            
        
def hssp_old(entry):                                                #In deze functie word er gelezen door de HSSP file. Welke PDB ID gebruikt moet worden voor de HSSP file word meegegeven door def "aanstuur"
    startpos3 = []
    protcount = 0                                               #Variabelen declareren
    seqcount = 0
    AAhssp = []
    door = False
    readh = False
    checklen = False
    lengthch = False
    eersteregel = False
    fl = True
    hsspfile =("{}/{}.hssp.bz2".format(pathhssp,entry))         #Openen van de HSSP file
    uncompressedData = bz2.BZ2File(hsspfile)                    #Sinds de HSSP files in deze databank gecompressed zijn naar een .bz2 formaat, moeten deze uigepakt worden voordat deze ingelezen kunnen worden. Dat gebeurd hier.
    
    for i, line in enumerate(uncompressedData):
        print i, line
        if "NALIGN  " in line:                                  #Dit is de hoeveelheid proteinen die hij allignt (Staat bovenaan de file). Dit moet natuurlijk kloppen met de hoeveelheid die in de file staat.
            protline = line[10:15]
        elif "SEQLENGTH  " in line:
            seqlen = line[10:15]                                #Dit gaat over hoe groot de sequentie is. 
        elif "## ALIGNMENTS" in line and door==False and AAhssp==[]:
            readh = False
            door = True
            checklen = True
        elif "## ALIGNMENTS" in line and door==True:
            readh = False
            door= False
            checklen = True
        elif "## ALIGNMENTS" in line:
            readh = False
        elif "## SEQUENCE" in line:
            checklen = False
            lengthch = True
        elif "## INSERTION" in line:
            lengthch = False
        elif " SeqNo  PDBNo AA" in line:
            pass
        elif lengthch == True:
            print len(line)

            if len(line) == 131 and eersteregel ==False:
                eersteregel = True
            elif len(line) != 130 and eersteregel == True:      #Als de regel langer is dan de standaard (Hij hoord standaard 130 te zijn) moet dit worden weergegeven.
                #return entry+" HSSP: \nEr is iets mis in de lengte onder de kop  ## instertion (Lengte van 1 van de regels is "+str(len(line))+") op ID "+line[7:13], "nope"
                print line[7:13]
                assert False

        elif readh == True:
            protcount += 1
        elif checklen == True and door ==True and fl == True:   #Dit is het eerste aminozuur.
            if line[14:16].islower():                           #Er kunnen ook kleine letters in de aminozuren voorkomen. Dit zijn allemaal Cysteine's. Hier worden ze dus vervangen door de 1 letter code.
                AAhssp.append("C")
                startpos3.append(line[7:13])
            else:
                AAhssp.append(line[14:16])                      #Voeg aminozuur toe bij de lijst genaamd AAhssp. Hier komen alle aminozuren in te staan.
            startpos3.append(line[7:13])
            seqcount +=1
            fl = False
        elif checklen == True and door==True and line[14:16].replace(" ","").islower(): #Als er een kleine letter in voorkomt moet dit worden vervangen door een Cysteine.
            seqcount +=1
            AAhssp.append("C")
            startpos3.append(line[7:13])
        elif checklen == True and door==True and not line[14:16].islower():
            if "!" in line:
                AAhssp.append(line[14:16])
                startpos3.append(line[7:13])
            else:
                seqcount +=1
                AAhssp.append(line[14:16])
                startpos3.append(line[7:13])
        elif "NR.    ID" in line:
            readh = True

    AAhssp = [x.strip(' ') for x in AAhssp]                     
    uncompressedData.close()                                    #Sluit bestand
    
    if int(protline) != protcount:
        return entry+" HSSP: \nHet aantal lijnen onder ## PROTEINS("+protline+") staan niet gelijk aan het nummer van NALIGN("+str(protcount)+")" , "nope"
    elif int(seqlen) != int(seqcount):
            return entry+" HSSP: \nSEQLENGTH ("+seqlen.replace(" ","")+") komt niet overeen met de lengte van de sequentie onder 'allignment'("+str(seqcount)+")", "nope"

    else:
        return AAhssp,startpos3

def dssp(entry):
    dsspfile = open("{}/{}.dssp".format(pathdssp,entry))        #Open DSSP bestand
    read = False
    count = 0
    AA = []
    lenerr = ""
    startpos2 = []
    for line in dsspfile:
        if read == True:
            if len(line) != 137:                                #Hier is ook een check om te kijken of de lengte van de regels voldoen aan het formaat.
                lenerr += entry+" DSSP: \nID '"+line[0:9]+"' klopt niet qua lengte.\n"
                count +=1
            elif line[0:5] == "    1":                          #Eerste positie
                AA.append(line [13:14])
                startpos2.append(line[6:13])
                count +=1
            elif "!*" in line:                                  #Er kunnen uitroeptekens voorkomen (Ev. icm een astrix) Deze zijn niet standaard en er moet later rekening mee gehouden worden ( In compare)
                AA.append("!*")
                startpos2.append(line[6:13])
            elif "!" in line:
                AA.append("!")
                startpos2.append(line[6:13])
            else:
                if line[13:14].islower():                       #Hier geld ook dat er kleine letters kunnen voorkomen. Dit zijn ook Cysteine's.
                    if line[6:13] != startpos2[-1]:
                        AA.append("C")
                        count +=1
                        startpos2.append(line[6:13])
                else:
                    if line[6:13] != startpos2[-1]:
                        AA.append(line [13:14])
                        count +=1
                        startpos2.append(line[6:13])
        if "#" in line:
            read = True
        if "TOTAL NUMBER OF RESIDUES" in line:
            residues = line[0:5]
        

    dsspfile.close()                                            #Sluit bestand
    if count != int(residues):
        return entry+" DSSP: \nhoeveelheid resideus klopt niet(nummer bovenin file("+residues+") klopt niet " \
        "met hoeveelheid residues onderaan bestand("+str(count)+")" , "nope"
    elif lenerr != "":
        return lenerr , "nope"
    else:
        return AA, startpos2
        
def hsdb(entry, startposhssp):
    try:
        pdbfile = open ("{}/pdb{}.ent".format(pathpdb,entry), "r")  #Pdb file voor HSSP.
    except IOError:
        return "Deze HSSP entry heeft geen PDB file!("+entry+")", "nope"
    seq = ""
    hetSeq = ""
    pdbids = []
    maypdbids = []
    addHet = False
    start = False
    read = False
    startpdb = 2
    i = 0
    dioxy = ['DA', 'DC', 'DG', 'DT', 'DI', "5CM", "5NC"]        #Deze kunnen zich voordoen in de sequentie, maar worden niet opgenomen in de HSSP file.
    for line in pdbfile:
        if startposhssp[1] == line[21:22] and startposhssp[0] == line[22:27].replace(" ",""):   #Hier word gekeken of de PDB_ID en de strand overeenkomen met de startpositie van de HSSP file.
            read = True
        if startposhssp[1] != line[21:22]:
            if line[21:22].replace(" ","") != "":
                read = False
                
        if line.startswith('HETATM') and start == True and read == True:                        #HETATM kunnen soms toegevoegd worden. Deze worden toegevoegd aan HSSP als daarna nog een ATOM of een TER regel voorkomt. Als een van deze tags niet meer na de HETATM voorkomt, worden deze genegeerd.
            if line[22:27] not in pdbids and line[22:27] not in maypdbids:
                hetSeq = hetSeq + line[17:20]+" "
                maypdbids.append(line[22:27])
                addHet = True

        elif line.startswith('ATOM') and start == True and read == True:     #Als de regel begint met ATOM moet deze altijd toegevoegd worden (vanaf het startpunt)
            if addHet == True:
                addHet = False                                                                      #Hier word ook eventueel de HETATM toegevoegd, mocht deze voorgaand aanwezig geweest zijn.
                seq = seq + hetSeq
                pdbids.extend(maypdbids)
                maypdbids = []
                hetSeq = ""
            if line[22:27] != pdbids[-1]:
                AA = line[17:20]+" "
                seq = seq + AA
                pdbids.append(line[22:27])

        elif line.startswith('ATOM') or line.startswith('HETATM'):                              #Dit word de eerste regel die hij tegenkomt waar hij toegevoegd moet worden( nadat de startpositie gevalideerd is)
            if  start == False and line[17:20].replace(" ","") not in dioxy and read == True:
                startpdb = line[22:27]
                AA = line[17:20]+" "
                seq = seq + AA
                start = True
                if line.startswith('HETATM'):
                    maypdbids.append(line[22:27])
                    addHet = True
                else:
                    pdbids.append(line[22:27])

      
    result=Convert(seq)                                                                         #Hier zet hij de 3 letterige code om naar de 1 letterige code.
    pdbfile.close()                                                                             #Sluit het pdb bestand
    return result, pdbids                                                                       #Teruggeven van alle resultaten (Aminozuur sequentie (1 letter code) + lijst met Id's)

    

def pdb():                                                                                      #Dit is een dictionairy met alle 20 aminozuren. Bij onbekende aminozuren word deze omgezet naar een X.
    seq1 = []
d = {'ALA':'A', 'VAL':'V', 'PHE':'F', 'PRO':'P', 'MET':'M',
     'ILE':'I', 'LEU':'L', 'ASP':'D', 'GLU':'E', 'LYS':'K',
     'ARG':'R', 'SER':'S', 'THR':'T', 'TYR':'Y', 'HIS':'H',
     'CYS':'C', 'ASN':'N', 'GLN':'Q', 'TRP':'W', 'GLY':'G',
     'UNK':'X', ' ':''}


def ReadPDB(entry, startposdssp):

    seq = ""
    hetSeq = ""
    pdbids = []
    maybe = []
    strand = []
    maybeStrand = []
    addHet = False
    start = False
    read = False
    startpdb = 2
    i = 0
    nmr = "0"
    try:
        pdbfile = open ("{}/pdb{}.ent".format(pathpdb,entry), "r")
    except IOError:
        return "Deze HSSP entry heeft geen PDB file!("+entry+")", "nope", "nope"
    dioxy = ['DA', 'DC', 'DG', 'DT', 'DI', "5CM", "5NC", "5IU","A","C", "G", "U", "I"]
    
    for line in pdbfile:
        if startposdssp[1] == line[21:22] and startposdssp[0] == line[22:27].replace(" ",""):
            if line.startswith("HETATM") or line.startswith("ATOM"):
                read = True
        if "MODEL        1" in line:
            nmr = "1"
        elif "MODEL        " in line and nmr == "1":
            nmr = "2"
        if nmr == "0" or nmr == "1":
            if line.startswith('HETATM') and start == True and read == True:
                if line[22:27] not in maybe and line[22:27] not in pdbids:
                    if line[17:20].replace(" ","") not in dioxy :
                        hetSeq = hetSeq + line[17:20]+" "
                        maybe.append(line[22:27])
                        maybeStrand.append(line[21:22])
                        addHet = True
                        
            elif line.startswith("TER") and start == True and read == True:
                if addHet == True:
                    addHet = False
                    seq = seq + hetSeq
                    pdbids.extend(maybe)
                    strand.extend(maybeStrand)
                    maybe = []
                    maybeStrand = []
                    hetSeq = ""
            
            elif line.startswith('ATOM') and start == True and line[17:20].replace(" ","") not in dioxy and read == True :
                if addHet == True:
                    addHet = False
                    seq = seq + hetSeq
                    pdbids.extend(maybe)
                    strand.extend(maybeStrand)
                    maybe = []
                    maybeStrand = []
                    hetSeq = ""

                if line[22:27].replace(" ","") != pdbids[-1].replace(" ",""):
                    AA = line[17:20]+" "
                    seq = seq + AA
                    pdbids.append(line[22:27])
                    strand.append(line[21:22])
            
            elif line.startswith('ATOM') or line.startswith('HETATM'):
                if  start == False and line[17:20].replace(" ","") not in dioxy:
                    AA = line[17:20]+" "
                    seq = seq + AA
                    if line.startswith("HETATM"):
                        maybe.append(line[22:27])
                        addHet = True
                    else:
                        pdbids.append(line[22:27])
                    start = True
    result=Convert(seq)
    pdbfile.close()
    return result , pdbids , strand


def Convert(seq):
    seq1 = []
    seq = seq.replace("\n","")
    lijst = seq.split()
    
    for item in lijst:
        try:
            seq1 = seq1 + [d[item]]
        except KeyError:
            seq1.append("X")
    return seq1

def compare(entry, AAhsdb, AAdssp, AApdb, AAhssp, Idshssp, Idsdssp , IdsPdbo,IdsPdbh, pdbStrand, startposhssp ,startposdssp):
    try:
        startpospdbh = IdsPdbh[0]
    except IndexError:
        return "\nDe start PDB ID die in de hssp file("+entry+") staat staat niet in de pdb entry zelf"
    try:
        startpospdbo = IdsPdbo[0]
    except IndexError:
        return "\nDe start PDB ID die in de dssp file("+entry+") staat staat niet in de pdb entry zelf"
    
    mismatch = ""
    pdbdssp = AApdb
    pdbhssp = AApdb
    a = 0
    s = 0
    zoek= False
    if startposdssp[0] != startpospdbo.replace(" ",""):
        startzoek = True
        while startzoek == True:
            try:
                if startposdssp[0] == IdsPdbo[0+s].replace(" ",""):
                    for w in range(s):
                        s = 0
                        del IdsPdbo[0+w]
                        del pdbdssp[0+w]
                        startzoek = False
                else:
                    s += 1
            except IndexError:
                print startposdssp
                print IdsPdbo
                print s

    e = 0
    enz = 0
    for stuff in Idsdssp:
        tussen = Idsdssp[e]
        Idsdssp[e] = tussen[0:len(Idsdssp[e])-1]
        dsspStrand = tussen[len(Idsdssp[e])-1:len(Idsdssp[e])]
        e+=1
    try:
        for i in xrange(1,len(pdbdssp)):
            if AAdssp[i] == "!" or AAdssp[i] == "!*":
                zoek = True
                while zoek == True:

                    if IdsPdbo[i+a].replace(" ","") == Idsdssp[i+1].replace(" ","") and pdbStrand[i+a] == dsspStrand[i+1]:
                        if a == 0:
                            del AAdssp[i]
                            del Idsdssp[i]
                            zoek = False
                        else:
                            del AAdssp[i]
                            del Idsdssp[i]
                            for q in range(a):
                                del IdsPdbo[i]
                                del pdbdssp[i]
                            zoek = False
                            a = 0
                            q = 0
                    else:
                        a += 1
            
            elif AAdssp[i] != pdbdssp[i]:
                if enz <4:
                    mismatch += "\n"+entry+"DSSP("+str(AAdssp[i])+")/PDB("+str(pdbdssp[i])+") positie: "+ str(IdsPdbo[i])+ " op strand " + str(pdbStrand[i])
                    enz +=1
                else:
                    mismatch += "and more...."
                    
    except IndexError:
        pass
    
    if startposhssp[0] != startpospdbh.replace(" ",""):
        startzoek = True
        while startzoek == True:
            if startposhssp[0] == IdsPdbh[0+s].replace(" ",""):
                for w in range(s):
                    s = 0
                    del IdsPdbh[0+w]
                    del AAhsdb[0+w]
                    startzoek = False

            else:
                s += 1

    enz = 0
    f = 0
    for stuff in Idshssp:
        tussen = Idshssp[f]
        Idshssp[f] = tussen[0:len(Idshssp[f])-1]
        hsspStrand = tussen[len(Idshssp[f])-1:len(Idshssp[f])]
        f+=1
    try:
        for j in xrange(1,len(AAhssp)):
            if AAhssp[j] == "!" or AAhssp[j] == "!*":
                    zoek = True
                    while zoek == True:
                        if IdsPdbh[j+a].replace(" ","") == Idshssp[j+1].replace(" ","")and pdbStrand[j+a] == hsspStrand[j+1]:
                            if a == 0:
                                del AAhssp[j]
                                del Idshssp[j]
                                zoek = False
                            else:
                                del AAhssp[j]
                                del Idshssp[j]
                                for q in range(a):
                                    del IdsPdbh[j]
                                    del AAhsdb[j]
                                    zoek = False
                                a = 0

                        else:
                            a += 1
            elif AAhssp[j] != AAhsdb[j]:
                if enz < 4:
                    mismatch += "\n"+entry+"HSSP("+str(AAhssp[j])+")/PDB("+str(AAhsdb[j])+") positie: "+ str(IdsPdbh[j])+" op strand " + str(hsspStrand[i])
                    enz += 1
                else:
                    mismatch += "and more...."
                    
    except IndexError:
        pass

    if mismatch == "":
        return "Geen verschillen gevonden tussen de bestanden"
    else:
        return mismatch

def hsspwalk():
    toevoeg = False
    for file in os.listdir(pathhssp):
        filext = os.path.splitext(file)[0]  #Filename without extention
        filename = filext[:-5]
        if filename == "3fi0":
            toevoeg = True
        if toevoeg == True:
            hsspent.append(filename)               #list with all filenames of hssp
    return hsspent
    
aanstuur()
