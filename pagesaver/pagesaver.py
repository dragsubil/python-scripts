import urllib.request


with urllib.request.urlopen('https://parahumans.wordpress.com/') as htmldata:
		htmlfile=open('gertude/file1.html','wb+')
		print(htmldata)
		htmlfile.write(htmldata.read())
		htmlfile.close()