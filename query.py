#	query.py
#===========================================================================

# This is used to read in the corpus and to do spot checks for frequency of 
# key terms or noun phrases. it will show you the document name and how it
# appears in the sentence.

#===========================================================================

#	Import the modules here

import glob
import os
import re
import sys

rgx = False
case = False

#	This prints what each term does function does

def print_help():
	print(':help\tprint this message')
	print(':regex\ttoggle regex (off by default)')
	print(':case\ttoggle case sensitivity (off by default)')
	print(':exit\tquit the program')
	print()


def run_query(ip, txts):
	found = 0
	for fn, txt in txts.items():
		search_txt = txt
		if not case:
			search_txt = txt.lower()
			ip = ip.lower()
		if rgx:
			pattern = re.compile(ip)
			pos = pattern.search(search_txt)
		else:
			pattern = re.compile(r'\b' + ip + r'\b')
			pos = pattern.search(search_txt)
		if pos is not None:
			found = found + 1
			pos = pos.span()[0]
			#lp = search_txt.rfind('\n', 0, max(0, pos - 1))
			#if lp == -1:
			#	lp = search_txt.rfind('.', 0, max(0, pos - 1))
			#if lp == -1:
			#	lp = max(0, pos - 50)
			lp = max(0, pos - 50)
			#rp = search_txt.find('.', pos)
			#if rp == -1:
			#	rp = search_txt.rfind('\n', 0, pos)
			#if rp == -1:
			#	rp = min(len(txt), pos + 50)
			rp = min(len(txt), pos + len(ip) + 70)
			fn_pos = fn.rfind("/") + 1
			print(fn[fn_pos:(fn_pos+20)] + "\t" + txt[(lp + 1):(rp + 1)].replace("\n", " "))
	print("Found " + str(found) + " results")

if len(sys.argv) < 2:
	print('Function: Search the content of text files')
	print('Usage: python3 query.py /path/to/txt/directory')
	print()
	exit(0)

txts = dict()

#	For this you will write in Anaconda the following:
#	python query.py c:\users\path\Name\here

for fn in glob.glob(os.path.join(sys.argv[1], '*.txt')):
	with open(fn, 'r') as f:
		txts[fn] = f.read()

print_help()
while True:
	ip = input('> ').strip()
	if ip == ":exit":
		break
	elif ip == ":quit":
		break
	elif ip == ":help":
		print_help()
	elif ip == ":regex":
		rgx = not rgx
		if rgx:
			print("Regex on")
		else:
			print("Regex off")
	elif ip == ":case":
		case = not case
		if case:
			print("Case sensitivity on")
		else:
			print("Case sensitivity off")
	else:
		run_query(ip, txts)

