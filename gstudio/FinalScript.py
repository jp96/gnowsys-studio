import re
import collections
import itertools
from yagoHarvest import *

def SystemType():
	filename = raw_input("Enter file Name:")
	in_file = file(filename,"r")
	out_file = file("SystemType.txt","w+")
	for line in in_file:
		line = line.decode("unicode_escape")
		line = line.encode("ascii","ignore")
		values = line.split("\t")
		if values[2]:
			for list in values[2].strip("wordnetyagowikicategory"):
					out_file.write(re.sub("[^\ a-zA-Z()<>\n""]"," ",list))

# Eliminate Duplicate Entries from extracted data using regular expression

def FSystemType():
	lines_seen = set()
	outfile = open("Output.txt","w+")
	infile = open("SystemType.txt","r+")
	object_call()
	for line in infile:
		if line not in lines_seen:
				l = line.lstrip()
# Below reg exp is used to handle Camel Case.
				outfile.write(re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', l).lower())
				lines_seen.add(line)
	infile.close()
	outfile.close()

def read():
	infile = open("Output.txt","r+")
	for line in infile:
		line = line.rstrip()
#		print line
		create_system_type(line)

def SystemPrior():
	filename = raw_input("Enter file Name:")
	in_file = file(filename,"r")
#	out_file = file("System.txt","w+")
	for line in in_file:
		values = line.split("\t")
		values = values
		if values[1]:
			sys1=""
			for list in values[1]:
				list = re.sub("[^\D0-9a-zA-Z()]"," ",list).lstrip()
				list = re.sub("[<>]","",list)
				list = re.sub("_"," ",list)
				sys1+=list
#				out_file.write(list)
#			out_file.write("	")
		if values[3]:
			sys2=""
			for list in values[3]:
					list = re.sub("[^\D0-9a-zA-Z()]"," ",list)
					list = re.sub("[<>]","",list)
					list = re.sub("_"," ",list)
					sys2+=list
#					out_file.write(list)
#			out_file.write("\n")
		s1 = sys1.lstrip()
		s2 = sys2.lstrip()
		s1 = s1.rstrip()
		s2 = s2.rstrip()
		add_prior_nodes(s1,s2)
		
# Call below function to extract only third column from file
def System_Col():
	filename = raw_input("Enter file Name:")
	in_file = file(filename,"r")
	out_file = file("System.txt","w+")
	for line in in_file:
		values = line.split("\t")
		if values[3]:
			for list in values[3]:
					list = re.sub("[^\D0-9a-zA-Z()]"," ",list)
					list = re.sub("[<>\n""]","",list)
					list = re.sub("_"," ",list)
					out_file.write(list)
			out_file.write("\n")


# Eliminate Duplicate Entries from extracted data using regular expression

def FSystem_Col():
	lines_seen = set()
#	outfile = open("Output.txt","w+")
	infile = open("System.txt","r+")
	for line in infile:
		if line not in lines_seen:
				l = line.lstrip()
				l = re.sub("\n","",l)
#				outfile.write(smart_str(l))
				create_systems(l,"Wikipage","")
				lines_seen.add(line)
	infile.close()
#	outfile.close()


def Tag():
	filename = raw_input("Enter file Name:")
	in_file = file(filename,"r")
	out_file = file("Tag.txt","w+")
	for line in in_file:
		line = line.decode("unicode_escape")
		line = line.encode("ascii","ignore")
		values = line.split("\t")
		if values[1]:
			for list in values[1]:
				list = re.sub("[^\\a-z0-9A-Z()<>]","",list)
				list = list.replace('_',' ')
				out_file.write(list)
			out_file.write("	")
		if values[2]:
			for list in values[2]:
				list = re.sub("[^\\a-z0-9A-Z()<>\n]"," ",list)
				list = list.replace('"','')
				out_file.write(list)


# Eliminate Duplicate Entries from extracted data using regular expression

def FTag():
#	outfile = open("Output.txt","w+")
	infile = open("Tag.txt","r+")

	D = collections.OrderedDict()
	for line in infile:
		key, value = line.split('\t')
		if key not in D:
			D[key] = []
		D[key].append(value.strip())

	for key, values in D.items():
# Otherway to write()		outfile.write(key + "	" + ','.join(values) + '\n\n')
#		outfile.write("%s\t%s\n" % (key,','.join(values)))
		create_systems(key,'Wikipage',','.join(values))
	infile.close()
#	outfile.close()


def AttributeType():
	cnt=0
	lines_seen = set()
#	outfile = open("Output.txt","w+")
	infile = open("AttributeType","r+")
	for line in infile:
		if line not in lines_seen:
			l = line.lstrip()
			l = re.sub("[<>\n]","",l)				# Below reg exp is used to handle Camel Case.
			create_attribute_type(re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', l).lower(),"Wikipage")
#			create_system_type(re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', l))
			lines_seen.add(line)
			cnt=cnt+1
	infile.close()
#	outfile.close()
#	print "Conversion done ",cnt


def Attribute():
	filename = raw_input("Enter file Name:")
	in_file = file(filename,"r")
	filename = filename.replace('.tsv','')
#	out_file = file("Attribute.txt","w+")

	for line in in_file:
############## Below two line code is used to handle non ascii character##############
		line = line.decode("unicode_escape")
		line = line.encode("ascii","ignore")
######################################################################################
		values = line.split("\t")
		if values[1]:
			str1 = ""
			for list in values[1]:
				list = re.sub("[^\Da-z0-9A-Z()]","",list)
				list = list.replace('_',' ')
#				out_file.write(list)
				str1 += list
#			out_file.write("	")
		if values[2]:
			str2 = ""
			for list in values[2]:
				list = re.sub("[^\Da-z0-9A-Z\n]"," ",list)
				list = list.replace('"','')
				list = list.replace('_',' ')
#				out_file.write(list)
				str2 += list
		s1 = str1.lstrip()
		s1 = s1.rstrip()
		s2 = str2.lstrip()
		s2 = s2.rstrip()
#		print s1+s2
		create_attributes(s2,s1,re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', filename).lower())

def RelationType():
	filename = raw_input("Enter file Name:")
	in_file = file(filename,"r")
#	out_file = file("Relation.txt","w+")
	for line in in_file:
		values = line.split("\t")
		if values[0]:
			str1 = ""
			for list in values[0]:
				list = re.sub("[^\Da-z0-9A-Z()]","",list)
				list = list.replace('_',' ')
#				out_file.write(list)
				str1 += list
#			out_file.write("	")
		if values[1]:
			str2 = ""
			for list in values[1]:
				list = re.sub("[^\Da-z0-9A-Z\n]"," ",list)
				list = list.replace('"','')
				list = list.replace('_',' ')
#				out_file.write(list)
				str2 += list
		s1 = str1.lstrip()
		s1 = s1.rstrip()
		s2 = str2.lstrip()
		s2 = s2.rstrip()
		create_relation_type(s1,s2,"Wikipage","Wikipage")


def Relation():
	filename = raw_input("Enter file Name:")
	in_file = file(filename,"r")
	filename = filename.replace('.tsv','')
#	out_file = file("Relation.txt","w+")
	for line in in_file:
		line = line.decode("unicode_escape")
		line = line.encode("ascii","ignore")
		values = line.split("\t")
		if values[1]:
			str1 = ""
			for list in values[1]:
				list = re.sub("[^\Da-z0-9A-Z()]","",list)
				list = list.replace('_',' ')
#				out_file.write(list)
				str1 += list
#			out_file.write("	")
		if values[2]:
			str2 = ""
			for list in values[2]:
				list = re.sub("[^\Da-z0-9A-Z\n]"," ",list)
				list = list.replace('"','')
				list = list.replace('_',' ')
#				out_file.write(list)
				str2 += list
		s1 = str1.lstrip()
		s1 = s1.rstrip()
		s2 = str2.lstrip()
		s2 = s2.rstrip()
#		print s1+s2
		create_relations(re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', filename).lower(),s1,s2)
