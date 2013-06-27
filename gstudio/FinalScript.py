import re
import collections
import ordereddict
import itertools
from yagoHarvest import *

def replace(txt,dict_txt):
        for key in dict_txt:
                txt = txt.replace(key,dict_txt[key])
        return txt
        
dict_txt = {'wordnet':'','yago':'','wikicategory':''}

"""
SystemType() function is used to extract system type from hasDomain.tsv,hasRange.tsv,subclassOf.tsv and type_star.tsv.
when we use subclassOf.tsv we have to extract both 2st and 3nd column turn by turn so use values[1] for 2st column and values[2] for 3nd column value. Remember in .TSV files column index start from 0.
"""
def SystemType():
	filename = raw_input("Enter file Name:")
	in_file = file(filename,"r")
	out_file = file("SystemType.txt","w+")
	for line in in_file:
		line = line.decode("unicode_escape")
		line = line.encode("ascii","ignore")
		values = line.split("\t")
		if values[1]:
                        values[1] = replace(values[1],dict_txt)
                        values[1] = re.sub("[^ a-zA-Z()]"," ",values[1])
                        values[1] = values[1].strip()
                        out_file.write(values[1])
                        out_file.write('\n')
"""
 Onces we have SystemType.txt file generated using SystemType() then call FSystemType() to add data to database tables.
"""
def FSystemType():
	lines_seen = set()
"""
	outfile = open("Output.txt","w+")   
"""
	infile = open("SystemType.txt","r+")
	for line in infile:
		if line not in lines_seen:
				l = line.lstrip()
                                l = re.sub("\n","",l)
"""
 Below reg exp is used to handle Camel Case.
"""
				create_system_type(re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', l).lower())
				lines_seen.add(line)
	infile.close()
"""
	outfile.close() 
 used to check the output in txt file
"""

"""
 SystemPrior() is used to set System in database. For setting up System we have to use yagoWikipediaInfo.tsv. First and third column represents System. So we have to set prior node in System. Below function is used to set prior node in System.
"""

def SystemPrior():
	filename = raw_input("Enter file Name:")
	in_file = file(filename,"r")
"""
	out_file = file("System.txt","w+")   
"""
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
"""
				out_file.write(list)
			out_file.write("	") 
 used to check the output in txt file   
"""
		if values[3]:
			sys2=""
			for list in values[3]:
					list = re.sub("[^\D0-9a-zA-Z()]"," ",list)
					list = re.sub("[<>]","",list)
					list = re.sub("_"," ",list)
					sys2+=list
"""
					out_file.write(list)
			out_file.write("\n")  
used to check the output in txt file   
"""
		s1 = sys1.lstrip()
		s2 = sys2.lstrip()
		s1 = s1.rstrip()
		s2 = s2.rstrip()
		add_prior_nodes(s1,s2)
		
"""
 Call below function to extract only third column from file
 System_Col() is used to Generate System.txt file which is used by FSystem_Col() to add it to the database.
"""
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

def FSystem_Col():
	lines_seen = set()
"""
	outfile = open("Output.txt","w+")   
"""
	infile = open("System.txt","r+")
	for line in infile:
		if line not in lines_seen:
				l = line.lstrip()
				l = re.sub("\n","",l)
"""
				outfile.write(smart_str(l))   
"""
				create_systems(l,"Wikipage","")
				lines_seen.add(line)
	infile.close()
"""
	outfile.close()   
"""

"""
 Tag() is used to set tag in System using hasWikipediaCategory.tsv file.
 Tag() is used to create Tag.txt file which consist of system and all its related tags separated by comma. Finally FTag() is used to set tags in database.
"""
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
"""
 For python version 2.6 or lesser.
 Download and add odereddict-1.1 library from pypi.python.org
"""

def FTag():
"""
	outfile = open("Output.txt","w+")   
"""
	infile = open("Tag.txt","r+")
"""
 Comment below code when python 2.7 is available and uncomment the next commented segment.
"""
	D = ordereddict.OrderedDict()
"""
use only when python version 2.7 or greater is available
	D = collections.OrderedDict()   
"""
	for line in infile:
		key, value = line.split('\t')
		if key not in D:
			D[key] = []
		D[key].append(value.strip())

	for key, values in D.items():
"""
 Otherway to write()		
		outfile.write(key + "	" + ','.join(values) + '\n\n')
		outfile.write("%s\t%s\n" % (key,','.join(values)))   
"""
		create_systems(key,'Wikipage',','.join(values))
	infile.close()
"""
	outfile.close()   
"""

"""
 AttributeType() is used to add Attribute Type in database.
 Use AttributeType txt file to add all the attribute type in database.
"""

def AttributeType():
	lines_seen = set()
"""
	outfile = open("Output.txt","w+")   
"""
	infile = open("AttributeType","r+")
	for line in infile:
		if line not in lines_seen:
			l = line.lstrip()
			l = re.sub("[<>\n]","",l)				
"""
 Below reg exp is used to handle Camel Case.
"""
			create_attribute_type(re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', l).lower(),"Wikipage")
			lines_seen.add(line)
	infile.close()
"""
	outfile.close()   
"""

"""
 Use AttributeType txt file, take one file and process it to add attributes in database.
"""

def Attribute():
	filename = raw_input("Enter file Name:")
	in_file = file(filename,"r")
	filename = filename.replace('.tsv','')
"""
	out_file = file("Attribute.txt","w+")   
"""
	for line in in_file:
"""
 Below two line code is used to handle non ascii character
"""
		line = line.decode("unicode_escape")
		line = line.encode("ascii","ignore")

		values = line.split("\t")
		if values[1]:
			str1 = ""
                        values[1] = replace(values[1],dict_txt)
			for list in values[1]:
				list = re.sub("[^\Da-z0-9A-Z()]","",list)
				list = list.replace('_',' ')
"""
				out_file.write(list)   
"""
				str1 += list
"""
			out_file.write("	")   
"""
		if values[2]:
			str2 = ""
                        values[2] = replace(values[2],dict_txt)
			for list in values[2]:
				list = re.sub("[^\Da-z0-9A-Z\n]"," ",list)
				list = list.replace('"','')
				list = list.replace('_',' ')
"""
				out_file.write(list)   
"""
				str2 += list
		s1 = str1.lstrip()
		s1 = s1.rstrip()
		s2 = str2.lstrip()
		s2 = s2.rstrip()
"""		
		print s1+s2   
"""
		create_attributes(s2,s1,re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', filename).lower())

"""
 RelationType() is used to add Relation Type in database.
 Use RelationType txt file to add all the relation type in database.
"""

def RelationType():
	filename = raw_input("Enter file Name:")
	in_file = file(filename,"r")
"""
	out_file = file("Relation.txt","w+")   
"""
	for line in in_file:
		values = line.split("\t")
		if values[0]:
			str1 = ""
			for list in values[0]:
				list = re.sub("[^\Da-z0-9A-Z()]","",list)
				list = list.replace('_',' ')
"""
				out_file.write(list)   
"""
				str1 += list
"""
			out_file.write("	")   
"""
		if values[1]:
			str2 = ""
			for list in values[1]:
				list = re.sub("[^\Da-z0-9A-Z\n]"," ",list)
				list = list.replace('"','')
				list = list.replace('_',' ')
"""
				out_file.write(list)   
"""
				str2 += list
		s1 = str1.lstrip()
		s1 = s1.rstrip()
		s2 = str2.lstrip()
		s2 = s2.rstrip()
		create_relation_type(s1,s2,"Wikipage","Wikipage")

"""
 Use RelationType txt file, take one file and process it to add relation in database.
"""

def Relation():
	filename = raw_input("Enter file Name:")
	in_file = file(filename,"r")
	filename = filename.replace('.tsv','')
"""
	out_file = file("Relation.txt","w+")   
"""
	for line in in_file:
		line = line.decode("unicode_escape")
		line = line.encode("ascii","ignore")
		values = line.split("\t")
		if values[1]:
			str1 = ""
                        values[1] = replace(values[1],dict_txt)
			for list in values[1]:
				list = re.sub("[^\Da-z0-9A-Z()]","",list)
				list = list.replace('_',' ')
"""
				out_file.write(list)   
"""
				str1 += list
"""
			out_file.write("	")   
"""
		if values[2]:
			str2 = ""
                        values[2] = replace(values[2],dict_txt)
			for list in values[2]:
				list = re.sub("[^\Da-z0-9A-Z\n]"," ",list)
				list = list.replace('"','')
				list = list.replace('_',' ')
"""
				out_file.write(list)   
"""
				str2 += list
		s1 = str1.lstrip()
		s1 = s1.rstrip()
		s2 = str2.lstrip()
		s2 = s2.rstrip()
"""
		print s1+s2   
"""
		create_relations(re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', filename).lower(),s1,s2)
