#
# Author: Stefan Schick
# Date: 21.01.2012
# Licence: GPLv2
# Version: 0.1
#


import sys
import urllib
import libxml2
import sets

from BeautifulSoup import BeautifulSoup
from httplib import HTTP
from urlparse import urlparse


url_matched = sets.Set()
url_crawled = sets.Set()

def check_url(url):
	p = urlparse(url)
	h = HTTP(p[1])
	h.putrequest('HEAD', p[2])
	h.endheaders()
	if h.getreply()[0] == 200: 
		return 0
	else: 
		return -1


def crawl(url, search_text, depth):
	# Check if URL is valid
	if url.find("http") == -1 or check_url(url) == -1:
		return

	# Mark and Download URL
	url_crawled.add(url)
	fd = urllib.urlopen(url)
	content = fd.read()
	fd.close()

	#print(url)
	# Parse the content
	content_parsed = BeautifulSoup(content)
	
	# Find Text
	if content_parsed.find(search_text) != -1:
		url_matched.add(url)
		#print(url)

	# Chek depth
	if depth == 0:
		return
	
	# Look for further links and crawl them if necessary
	link_tags = content_parsed.findAll(True, attrs={"href" : True})

	for link in link_tags:
		if link['href'] not in url_crawled:
			crawl(link['href'], search_text, depth -1)


def main():
	# Print usage if parameters are wrong
	if len(sys.argv) != 4:
		print("Usage: python2 week1-webcrawler.py $url $searchtext $depth")
		exit()

	url = sys.argv[1]
	search_text = sys.argv[2]
	depth = int(sys.argv[3])

	# Start Crawling
	print("crawling..")
	crawl(url, search_text, depth)

	# Print found URLs
	for u in url_matched:
		print(u)


if __name__ == "__main__":
	main()
