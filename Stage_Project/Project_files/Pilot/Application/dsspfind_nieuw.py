##Author : Jay Ligtvoet.##
##Version 1.2           ##
##Bugs : None known.    ##
##########################
import os
from urllib import urlopen
import time
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
#from flask_debugtoolbar import DebugToolbarExtension
from contextlib import closing

# configuration
DEBUG = True
SECRET_KEY = 'development key'
# creating the application
app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True
app.config['SECRET_KEY'] = '<replace with a secret key>'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

pdbent, dssp, hssp ,carb, nores, nucacid, nothere1,nothere2,nothere3, nothereighter , itshere = ([] for i in range(11)) #makes 9 lists with names mentioned before
check = {}
pathdssp = "/mnt/cmbi4/dssp"    #location of the map with all the dssp files
#pathpdb = "/home/jayligt/Project_files/Pdb"
pathpdb = "/mnt/cmbi4/pdb/flat" #location of the map with all the pdb files
pathhssp = "/mnt/cmbi4/hssp3"    #location of the map with all the hssp files
why_not_dssp = urlopen("http://www.cmbi.ru.nl/WHY_NOT2/entries_file/?databank=DSSP&collection=annotated&listing=comments")  #why_not file with all the pdb entry's with an exception in it of the dssp database.
why_not_hssp = urlopen("http://www.cmbi.ru.nl/WHY_NOT2/entries_file/?databank=HSSP&collection=annotated&listing=comments")   #why_not file with all the pdb entry's with an exception in it of the hssp database.

# TODO: Read about the strategy design pattern
##############################################################################################################################################################################################################
### Routes ###################################################################################################################################################################################################
##############################################################################################################################################################################################################
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/selected', methods=['GET', 'POST'] )
def redirect():
    results = []
    databases = request.form.getlist('databank')
    if "DSSP" in databases:
        results.append(dsspfind())
    if "HSSP" in databases:
        results.append(hsspfind())
    if "BDB" in databases:
        results.append(bdbfind())
    return render_template('results.html', entries =results)

@app.route('/hsspfind')
def hsspfind():

    dssp = dsspwalk()
    hssp = hsspwalk()
    set1 = set(hssp)
    set2 = set(dssp)

    onlyInHSSP = set1- set2
    if onlyInHSSP != set([]):
        return "Entry('s) found in HSSP that doens't exist in DSSP: "+(list(onlyInHSSP))

    else:
        for entry in dssp:
            if entry not in hssp:
                nothere1.append(entry)
                
        nothereighter = why_not_check(why_not_hssp, "hssp", nothere1)
        if nothereighter == []:
            return "HSSP:\nNiets gevonden\n"
        else:
            return "HSSP:<br />"+', ' .join(nothereighter)+"<br />"  

@app.route('/dsspfind')
def dsspfind():
    pdbent = pdbwalk()
    dssp = dsspwalk()

    for entry in pdbent:
        if entry not in dssp:
            nothere2.append(entry)
            
    nothereighter = why_not_check(why_not_dssp, "dssp", nothere2)
    if nothereighter == []:
        return "DSSP:\nNiets gevonden\n"
    else:
        return "DSSP:\n"+ ', ' .join(nothereighter)+"\n"     

# TODO: Read about the single responsibility principle

@app.route("/bdbfind")
def bdbfind():
    # TODO: create separate function
    entrys = pdbwalk()
    check_1 = mapsearch(entrys ,'bdb' , '/mnt/cmbi4')
    if check_1 == []:
        return "BDB:<br />Niets gevonden<br />"
    else:
        return "BDB:<br />"+', ' .join(check_1)+"<br />"     
##############################################################################################################################################################################################################
### Functions ################################################################################################################################################################################################
##############################################################################################################################################################################################################

def pdbwalk():
    for file in os.listdir(pathpdb):
        filext = os.path.splitext(file)[0]  #Filename without extention
        filename = filext[3:]               #Filename without the "PDB"
        pdbent.append(filename)             #list with all filenames of pdb
    return pdbent

def dsspwalk():
    for file in os.listdir(pathdssp):
        filename = os.path.splitext(file)[0]#Filename without extention
        dssp.append(filename)               #list with all filenames of dssp
    return dssp

def hsspwalk():
    for file in os.listdir(pathhssp):
        filext = os.path.splitext(file)[0]  #Filename without extention
        filename = filext[:-5]
        hssp.append(filename)               #list with all filenames of hssp
    return hssp

def mapsearch(pdbent, databank , data_root):
    for entry in pdbent:
        # TODO: '{}'.format() = string formatting
        normal_path = '{}/{}/{}/{}/{}.{}'.format(data_root, databank, entry[1:3], entry, entry, databank)
        why_not_path = '{}/{}/{}/{}/{}.{}'.format(data_root, databank, entry[1:3], entry, entry, 'whynot')
        if not os.path.exists(normal_path):
            if not os.path.exists(why_not_path):
                nothere3.append(entry)
    return nothere3


def why_not_check(why_not_file, databank, nothere):
    for line in why_not_file:
        #All lines with no PDB:
        if line.startswith(databank.upper()):
            split = line.split(',')
            check[split[1].rstrip('\n')] = ["waarde"]   #removes "DSSP" and "\n" and takes the why_not status with it.

    for entry in nothere:
        if entry in check:                  #takes the why_not status and checks it where it belongs.
            if check[entry] == ['waarde']:
                carb.append(entry)
            else:
                print "Onbekende why_not exceptie"  #if the entry is there but doesn't belong in one of those 3 above.
            
        else:
            nothereighter.append(entry)
    return nothereighter

if __name__ == '__main__':
    app.run()

