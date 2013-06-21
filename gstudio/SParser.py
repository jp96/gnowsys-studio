import re
from gstudio.yagoHarvest import *
def extract():
	filename = raw_input("Enter file Name:")
	in_file = file(filename,"r")
	out_file = file("SystemType.txt","w+")
	for line in in_file:
		line = line.decode("unicode_escape")
		line = line.encode("ascii","ignore")
		values = line.split("\t")
		if values[3]:
			for list in values[3]:
					list = re.sub("[^\D0-9a-zA-Z()]"," ",list)
					list = re.sub("[<>\n]","",list)
					list = re.sub("_"," ",list)
					out_file.write(list)
			out_file.write("\n")


# Eliminate Duplicate Entries from extracted data using regular expression

def finalextract():
	lines_seen = set()
#	outfile = open("Output.txt","w+")
	infile = open("SystemType.txt","r+")
	for line in infile:
		if line not in lines_seen:
				l = line.lstrip()
				l= re.sub("\n","",l)
				create_systems(l,"Wikipage","")
				lines_seen.add(line)
	infile.close()
#	outfile.close()
