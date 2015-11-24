import os
 
# The top argument for walk
topdir = '/home/jayligt/Project_files'
# The extension to search for
exten = '.dssp'
logname = 'findfiletype.log'
# What will be logged
results = str()
 
for dirpath, dirnames, files in os.walk(topdir):
    for name in files:
        if name.lower() == '101m':
            # Save to results string instead of printing
            results += '%s\n' % os.path.join(dirpath, name)
 
# Write results to logfile
with open(logname, 'w') as logfile:
    logfile.write(results)
