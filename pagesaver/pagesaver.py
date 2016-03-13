#!usr/bin/env python3
import re
import urllib.request

#function to extract link from the line

fileno=1  #global variable

def linkExtract(file_line):
	pattern1=re.compile(r'href=(.*?)>')         #regex patteren to look for the link in the "href='www.somewebsite.com/somelink.html'" part of each line
	linktup=pattern1.search(file_line).groups()  #forms a tuple with one element containing the raw string link
	link1=linktup[0]
	link1=link1[1:-1]						    #removes the unwanted quotes from the ends
	return link1
	
#function to parse each line to find link
def fileParse(link_file):
	for i in link_file:
		link1=linkExtract(i)
		pageSave(link1)                            #passes link to pageSave function

		
#NOTE: VERY IMPORTANT: change how the file name is obtained. maybe extract the name along with the link in the linkExtract function
def pageSave(page_link):
	file_name="pages/file{}.html".format(fileno)              
	with urllib.request.urlopen(page_link) as page_object:
		with open(file_name,'ab+') as file1:
			file1.write(page_object.read())

testlink='http://www.diveintopython3.net/regular-expressions.html'

pageSave(testlink)
	
	
		
		
		



