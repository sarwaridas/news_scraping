#	download_newspaper.py
#===========================================================================
#
#	This script downloads the text of the selected URLs 
#	obtained from the key term search in retrieve_urls.py.
#
#===========================================================================

#	Import the modules here

from random import random
from re import sub
from time import sleep
from unicodedata import normalize
from urllib.request import urlopen
import csv
import html2text
import os
import requests
import PyPDF2
import sys

h = html2text.HTML2Text()
h.ignore_links = False

#	Conditional statements

if len(sys.argv) < 2:
	print('Function: Download the text of provided URLs')
	print('Usage: python3 download.py /path/to/urls/here.csv [/path/to/downloads/folder]')
	print('The urls must be the last column of the CSV')
	print('If no download folder is provided, content will be downloaded to ./downloads')
	print()
	exit(0)

#	This generates a log of the searches completed

log_loc = sys.argv[1] + ".log"
already_done = []
if os.path.isfile(log_loc):
	with open(log_loc, 'r') as log:
		already_done = [line.strip() for line in log]
log = open(log_loc, 'a')

#	This generates a folder "downloads_newspaper" which holds the 
#	.txt documents from the selected URLs.

download_loc = 'downloads_newspaper'
if len(sys.argv) > 2:
	download_loc = sys.argv[2]
if not os.path.exists(download_loc):
	os.makedirs(download_loc)
print('Downloading to ' + download_loc)

# 	Peeking to determine csv format
# 	with open(sys.argv[1], 'r') as csvfile:

# 	try:
# 		sample = csvfile.read(1024)
# 		with_header = csv.Sniffer().has_header(sample)
# 		dialect = csv.Sniffer().sniff(sample, delimiters=',\t|')
# 	except:
# 		with_header = True
# 		dialect = "unix"

#	To actually retrieve the urls to be downloaded

urls = []
with open(sys.argv[1], 'r') as csvfile:
	reader = csv.reader(csvfile)
	next(reader)
	for row in reader:
		urls.append(row[-1])

#	This notes whether a url has already been searched (since the 
#	same URL may appear for more than one search term combination)
#	and says 'don't pull text from this repeat.

overlap = set(urls).intersection(set(already_done))
if len(overlap) != 0:
	print('Skipping ' + str(len(overlap)) + ' already-searched URLs')
urls = list(set(urls) - set(already_done))

#	If the URL meets the baseline criteria for a web address, then
#	we continue with pulling data. If this doesn't work, the console
#	will print a "404 error. Another issue that may arise is that
#	the website will have non-readable text (e.g., image-based PDFs).
#	In this case, you'll get a message 'Could not extract text from.'

#	There is a .5 second delay between attempts to pull text so that
#	we're not kicked out for being a bot.

for url in urls:
	log.write(url + "\n")
	log.flush()
	# weed out headers -- URLs must have a period
	period = url.rfind('.')
	if period == -1:
		continue
	print(url)
	filename = url[url.rfind('/') + 1:]
	try:
		resource = urlopen(url)
		content_type = resource.headers.get_content_type()
		source = resource.read()
	except:
		print("\t*404/403/etc*")
		continue

	if 'application/pdf' in content_type:
		filename = sub(r"[^a-zA-Z0-9\._-]", "_", filename)
		if filename[-4:] != '.pdf':
			filename = filename + '.pdf'
		location = os.path.join(download_loc, filename)
		with open(location, 'wb') as outf:
			outf.write(source)
		try:
			pdf_text = ""
			with open(location, 'rb') as pdfFileObj:
				pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
				pages = [page.extractText() for page in pdfReader.pages]
				pdf_text = "\n\n".join(pages)
			with open(location[:-4] + ".txt", 'w') as outf:
				outf.write(pdf_text)
		except:
			print("Could not extract text from " + url)

	elif 'text/html' in content_type:
		filename = sub(r"[^a-zA-Z0-9\._-]", "_", filename)
		if filename[-4:] != '.txt':
			filename = filename + ".txt"
		location = os.path.join(download_loc, filename)
		encoding = resource.headers.get_content_charset()
		if encoding is None:
			encoding = 'utf-8' # just guessing
		try:
			html_content = source.decode(encoding, 'ignore')
			rendered_content = html2text.html2text(html_content)
			with open(location, 'w') as outf:
				outf.write(rendered_content)
		except:
			print("Could not extract text from " + url)
			continue

	else:
		print('\t*has unknown content type "' + content_type + '" and is ignored*')

	sleep(0.5 + random())


log.close()
