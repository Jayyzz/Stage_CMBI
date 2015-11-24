def compare(entry, AAhsdb, AAdssp, AApdb, AAhssp,startposdssp, startposhssp, startpospdb, Idsdssp , IdsPdbo):
    mismatch = ""
    pdbdssp = []
    a = 0
    w = 1
    pdbdssp = AApdb
    zoek= False
    if startposdssp.replace(" ","") != startpospdb.replace(" ",""):
        print startposdssp
        print startpospdb
        eraf = int(startposdssp)-int(startpospdb)
        try:
            for i in range(eraf):
                print "hoi"
                del pdbdssp[eraf-1]
                eraf -= 1
        except IndexError:
            pass    

##        pdbhssp = AApdb
    print entry
    print len(AApdb)
    print len(AAdssp)
    print len(Idsdssp)
##    if entry == "104l":
##    print "Pdb "+str(len(AApdb))
####        print AApdb
##    print "org.dssp "+str(len(AAdssp))
##        print AAdssp
    for i in xrange(1,len(AApdb)):
        
##        try:
##        if entry == "1a1c":
##            print AAdssp[i-1]
##            print pdbdssp[i-1]
##            print Idsdssp[i]
##            print IdsPdbo[i]
        if AAdssp[i] == "!" or AAdssp[i] == "!*":
##            if entry == "148l":
##                
##                print i-1
##                print len(Idsdssp)
##                print Idsdssp
##                print IdsPdbo
##                print len(IdsPdbo)
##                print AAdssp[i-1]
##                print AApdb[i+a].replace(" ","")
##                print AAdssp[i].replace(" ","")
##                print w
##                print Idsdssp[i+w].replace(" ","")
##                print IdsPdbo[i+a-1].replace(" ","")
            zoek = True
            while zoek == True:
                if IdsPdbo[i+a-1].replace(" ","") == Idsdssp[i+w].replace(" ",""):
##                    print "komt ie hier of?"
                    print len(AAdssp)
                    if a == 0:
##                        w += 1
                        del Idsdssp[i]
                        del AAdssp[i]
                        zoek = False
                    for q in range(a):
##                        print "woop"
##                        w += 1
                        a = 0
                        del Idsdssp[i+q]
                        del AAdssp[i+q]
                        zoek = False
##                    print len(AApdb)
##                    print AApdb
                    print len(AAdssp)
##                    print AAdssp
                else:
                    print i
                    a += 1
                    print a
##            if Idsdssp[i+1].replace(" ","") == IdsPdbo[i].replace(" ",""):
##                print "hoi "
####                print Idsdssp
####                print AAdssp
####                print IdsPdbo
####                print pdbdssp
####                print AAdssp[i]
##                del Idsdssp[i]
##                del AAdssp[i]
##                print "Nieuw.dssp "+str(len(AAdssp))
##                
##                print "tof"
##            elif Idsdssp[i].replace(" ","") == IdsPdbo[i-1].replace(" ",""):
##                print "doei"
##                del AAdssp[i]
##                del Idsdssp[i]
##                print AAdssp[i]
##                print AAdssp[i+1]
##                print AAdssp[i+2]
##                print pdbdssp[i-1]
##                print pdbdssp[i]
##                print pdbdssp[i+1]


        elif AAdssp[i-1] != pdbdssp[i-1]:
            mismatch += "\n"+entry+"DSSP("+str(AAdssp[i-1])+")/PDB("+str(pdbdssp[i-1])+") positie: "+ str(IdsPdbo[i])
##        except IndexError:
##            mismatch = "Blah"
    for j in xrange(1,len(AAhssp)+1):
        if AAhssp[j-1] != AAhsdb[j-1]:
            mismatch += "\n"+entry+"HSSP("+str(AAhssp[j-1])+")/PDB("+str(AAhsdb[j-1])+") positie: "+ str(j)
    
    if mismatch == "":
        return "Geen verschillen gevonden tussen de bestanden"
    else:
        return mismatch
