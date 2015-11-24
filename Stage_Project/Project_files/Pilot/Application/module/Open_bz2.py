import bz2

file1 =("/mnt/cmbi4/hssp/101m.hssp.bz2")
uncompressedData = bz2.BZ2File(file1)
for line in uncompressedData:
    print line
