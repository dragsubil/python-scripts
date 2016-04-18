#!usr/bin/env python3


#PageSaver for Worm
#Made to download chapters from the web serial "Worm" (see more at https://parahumans.wordpress.com/)
#The table.html file contains links to all chapters, copied from the Worm Table of Contents page. sampletable.html cotains chapter links for only the first arc.
#Cannot be used for other such web serials unless they a Table of Contents page identical to Worm's.
#Licensed under GNU GPL v3. (C) 2016 dragsubil (www.github.com/dragsubil)
#Requires python 3.x
#Support Worm by reading directly from https://parahumans.wordpress.com/




import re  				#for regular expressions
import urllib.request   #for page downloading facility
import os				#for deleting the temp files and creating the directories



namelist=[]  #holds the list of file links as a list of 'temp_files/xxx.html' which are used when link replacement is done. These file names are obtained from the original table of contents file.

namedict={}  #holds the file links as 'temp_files/xxx.html' along with the corresponding prev chapter and next chapter file links whose names are obtained from the original table of contents file




		
def findAndReplace(tmp_file,dict_key,file_name):

	prevchapfind=re.compile(r'href=.*?>(<\D>)?Last\sChapter<')      #finds the a href tags with previous chapter link
	nextchapfind=re.compile(r'href=.*?>(<\D>)?Next\sChapter<')
	bodyfind=re.compile(r'<body\s.*?>')

	try:
		prevfilename=((namedict[dict_key][0]).split('/'))[1]     #namedict[dict_key][0] contains the previous chapter path "temp_files/xxx.html". we seperate the folder and filename and store the filename 
	except IndexError:
		prevfilename="NothingHere"

	try:
		nextfilename=((namedict[dict_key][1]).split('/'))[1]     #namedict[dict_key][1] contains the next chapter path "temp_files/xxx.html". we seperate the folder and filename and store the filename 
	except IndexError:
		nextfilename="NothingHere"


	new_file_path='pages/{}'.format(file_name)
	
	with open(new_file_path,'w+',encoding='utf-8') as new_file:
		for line in tmp_file:
			chklinenext=nextchapfind.search(line)
			chklineprev=prevchapfind.search(line)
			chklinebody=bodyfind.search(line)

			if chklinenext and chklineprev:	
				a='<p><a href={}>Last Chapter</a>                    <a href={}>Next Chapter</a></p>'.format(prevfilename,nextfilename)

			elif chklinenext:
				a='<p> <a href={}>Next Chapter</a></p>'.format(nextfilename)       #the first 3 if-elifs is used to look for the line in html for the next and previous chapter links 
                                                                                   #a new line is written to point to the locally saved chapter pages
			elif chklineprev:
				a='<p> <a href={}>Last Chapter</a></p>'.format(prevfilename)

			elif chklinebody:
				a=line+'<font face="Calibri">'			#appends the font tag to the body tag to change the font in basic html

			else:
				a=line

			new_file.write(a)
	
	



#to find and replace hyperlinks at the "previous chapter" and "next chapter" positions
def linkReplace():											
	for file_path in namelist:
		with open(file_path,'r+',encoding='utf-8') as tmpfile1:
			file_name=(file_path.split('/'))[1]
			findAndReplace(tmpfile1,file_path,file_name)
		os.remove(file_path)								#deletes the corresponding file from temp_files after creating a new file with changed links in pages dir






	
def addToDict(file_path):
	listlen=len(namelist)
	if listlen==0:
		namedict[file_path]=['','']
		namelist.append(file_path)
		return
	else:
		prev_in_list=namelist[listlen-1]
		namedict[prev_in_list][1]=file_path
		namedict[file_path]=[prev_in_list,'']
		namelist.append(file_path)
	
	
	




	
#function to save the page with the extracted name, given by the extracted link 
def pageSave(page_link,page_name):
	file_path="temp_files/{}.html".format(page_name)              
	with urllib.request.urlopen(page_link) as page_object:
		with open(file_path,'wb+') as file1:
			file1.write(page_object.read())
			print('Downloaded: {} into temp_files'.format(page_name))
			addToDict(file_path)




#creates a new table of contents file in pages dir. replaces each link in the original table of contents file with local file links			
def tableOfContentsReplace(page_name,line):
	with open('pages/tableofcontents.html','a+',encoding='utf-8') as file1:
		if page_name!=None:
			line=re.sub(r'href=.*?>','href="{}.html">'.format(page_name),line)

		file1.write(line)
			




def charRemoval(name1):
		name1=name1.replace(" ","")							#removing some chars because because I'm using the name1(the chapter title) to create the local file link. links do other stuff with those chars that mess with the file link
		name1=name1.replace("#","")
		name1=name1.replace(";","")
		name1=name1.replace(":","")
		name1=name1.replace(",","")
		return name1




   

#function to extract link and name from the line
def linkExtract(file_line):

	pattern1=re.compile(r'''		#regex patteren to seperate link, any tag inbetween link and name, and name from original table of contents file
	
			href=					#start from the place where href is to get link
			
			(.*?)>					#obtaining the link from the line. '>' at the end specifies end of tag
			
			(<\D*?>)?				#accounts for any extra tag that might appear inbetween link and title
			
			(.*?)<					#obtaining the name of the link present in the same line
			
			''', re.VERBOSE)        
			
	try:
		link_and_file_tup=pattern1.search(file_line).groups()   #groups forms a tuple containing the elements obtained in the parantheses of the regex


	except AttributeError:										#in case of a line with none of the properties in regex, None is obtained in pattern.search
		return													#this raises AttributeError, so we must got to the next line in file, hence return a None
		

	link1=link_and_file_tup[0]
	name1=link_and_file_tup[2]									#name is actually the third element, second being a potential inbetween tag
	link1=link1[1:-1]						   				 	#removes the unwanted quotes from the ends of the link we got 
	return (link1,name1)









	
#function to parse each line in the original table of contents html file and call the linkExtract()

def fileParse(link_file):

	for i in link_file:	
		try:													#because of the possibility of an AttributeError from linkExtract, we get a None returned 
			link1,name1=linkExtract(i)							#this leads to a TypeError, which we try-exceptionise and go to next iteration i.e. search the next line of the html file
			name1=charRemoval(name1)							#removes chars from the name that done play well in a URL
			tableOfContentsReplace(name1,i)						
		except TypeError:
			tableOfContentsReplace(None,i)									
			continue

		pageSave(link1,name1)                            	#passes link and name to pageSave function





#deletes the old tableofcontents.html file if it exists. Because the TOC is opened in append later on and repeated usage of this script will lengthen it, not start over
def delOldTOC():
	try:
		os.remove("pages/tableofcontents.html")
	except OSError:
		pass


#creates the folder tenp_files, to hold initially downloaded pages, and the folder pages, to hold the pages with links changed to local
def createFolders():
	if not os.path.exists("pages"):
		os.makedirs("pages")
	if not os.path.exists("temp_files"):
		os.makedirs("temp_files")






#Execution starts here
#each function called below (and inside other functions) can be found,in order, from bottom to top

createFolders()
delOldTOC()

tableofcontents=str(input("please enter name of table of contents file: "))
with open(tableofcontents,'r+',encoding='utf-8') as file1:
	fileParse(file1)

print("Please wait. Changing links to local links")
linkReplace()
print("\n\nDone")









