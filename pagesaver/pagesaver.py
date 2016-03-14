#!usr/bin/env python3
import re
import urllib.request

#function to extract link and name from the line

prev_name_name=''        

def linkExtract(file_line):

	pattern1=re.compile(r'''		#regex patteren to seperate link, any tag inbetween link and name, and name
	
			href=					#start from the place where href is to get link
			
			(.*?)>					#obtaining the link from the line. '>' at the end specifies end of tag
			
			(<\D*>)?				#accounts for any extra tag that might appear inbetween link and title
			
			(.*?)<					#obtaining the name of the link present in the same line
			
			''', re.VERBOSE)        
			
	try:
		link_and_name_tup=pattern1.search(file_line).groups()   #groups forms a tuple containing the elements obtained in the parantheses of the regex
		
	except AttributeError:										#in case of a line with none of the properties in regex, None is obtained in pattern.search
		return													#this raises AttributeError, so we must got to the next line, hence return a None
		
	#print(link_and_name_tup)
	link1=link_and_name_tup[0]
	name1=link_and_name_tup[2]									#name is actually the third element, second being a potential inbetween tag
	link1=link1[1:-1]						   				 	#removes the unwanted quotes from the ends of the link we got 
	return (link1,name1)
	
#function to parse each line in the html file and call the linkExtract()

def fileParse(link_file):
	for i in link_file:	
		try:													#because of the possibility of an AttributeError from linkExtract, we get a None returned 
			link1,name1=linkExtract(i)							#this leads to a TypeError, which we try-exceptionise and go to next iteration
			
		except TypeError:									
			continue
			
		#print(link1,name1)
		pageSave(link1,name1)                            	    #passes link and name to pageSave function

		
def linkReplace(new_file_name):									#to find and replace hyperlinks at the "previous chapter" and "next chapter" positions
	if prev_name_name=='':										#seperate linkReplace and linkReplaceProper for readability
		prev_name_name=new_file_name
	else:
		linkReplaceProper(prev_name_name,new_file_name)
		prev_name_name=new_file_name
		
		
def linkReplaceProper(prev_name,next_name):
	with open(prev_name,'a+') as file1:
		file1.seek(0)
		linkReplaceRegex(file1,next_name)
	with open(next_name,'a+') as file2
		file2.seek(0)
		linkReplaceRegex(file2,prev_name)
		
def linkReplaceRegex(file_obj,file_name):
	for i in file_obj:
		
	
	
	
	
	

	
#function to save the page with the extracted name, given by the extracted link 
def pageSave(page_link,page_name):
	file_name="pages/{}.html".format(page_name)              
	with urllib.request.urlopen(page_link) as page_object:
		with open(file_name,'wb+') as file1:
			file1.write(page_object.read())
			print('Downloaded: {}.html'.format(page_name))
	linkReplace(file_name)
			
			

#combined unit test

with open('table.html','r+') as file1:
	fileParse(file1)












	
#pageSave unit test
'''
testlink='http://www.diveintopython3.net/regular-expressions.html'

pageSave(testlink)
'''

#linkExtract unit test
'''
testfile_line='<div><strong><a title="View all posts filed under 11.e" href="https://parahumans.wordpress.com/category/stories-arcs-11/arc-11-infestation-stories-arcs-11/11-e/">11.e</a></strong></div>'
	
link1,name1=linkExtract(testfile_line)

print(link1,name1)
'''

