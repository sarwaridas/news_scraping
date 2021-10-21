readme.txt

#===========================================================================

FOLDERS

	archive

old files that we don't need right now but hang on to just in case.

	scraps

folder of scrap files, mostly for scripts.

#===========================================================================

FILES

	download_newspaper.py

this script downloads the text of the selected URLs obtained from the key 
term search in retrieve_urls.py.

	environment.yml

this is used to tell anaconda which packages (e.g. python, beautifulsoup) to 
install and use as prerequisites for the web scraping scripts, i.e. to 
manage the environment. Anaconda "solves" the environment by determining 
which versions of the packages are mutually compatible. You can turn on and off 
environments using conda  to enable different sets of packages for different 
projects.

	notice.txt

this is the list of search terms that are used to scrape relevant URLs; the
list of these words is read into retrieve_urls.py.

	noticeURL.log

this is a log of all the URLs pulled with retrieve_urls.py given the list of
words set in notice.txt.

	previous_searches.log

this is generated to show the series of search combinations used in search.py.

	query.py

this is used to read in the corpus and to do spot checks for frequency of 
key terms or noun phrases. it will show you the document name and how it
appears in the sentence.

	retrieve_urls.py

this is to pull the relevant URLs from newspaper domains based on the key
terms specified in notice.txt.

	state.txt

this is to include "North Carolina" in the search so that this reduces the 
likelihood that boil notices for samed-named towns from other states do not
appear in the corpus.

	urls.txt

this is the list of newspaper domains from which we search for relevant URLs
with information relating to boil notices.

#===========================================================================