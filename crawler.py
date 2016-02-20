import time

def time_execution(code):
	start = time.clock()
	result = eval(code)
	run_time = time.clock() - start
	return result, run_time

def get_next_target(page):
	start_link = page.find('<a href=')
	if start_link == -1:
		return None, 0
	#get the start quote of URL
	start_quote = page.find('"', start_link)
	#get the end quote of URL
	end_quote = page.find('"', start_quote + 1)
	url = page[start_quote + 1:end_quote]
	return url, end_quote

def get_all_links(page):
	links = []
	while True:
		url, endpos = get_next_target(page)
		if url:
			links.append(url)
			page = page[endpos:]
		else:
			break
	return links

def union(item1, item2):
	for p in item2:
		if p not in item1:
			item1.append(p)

def get_page(url):
	try:
		import urllib
		return urllib.urlopen(url).read()
	except:
		return ""

def crawl_web(seed):
	crawled = []
	to_crawl = [seed]
	index = {}
	graph = {}
	while to_crawl:
		page = to_crawl.pop()
		if page not in crawled:
			content = get_page(page)
			add_page_to_index(index, page, content)
			outlinks = get_all_links(content)
			graph[page] = outlinks
			union(to_crawl, outlinks)
			crawled.append(page)
	return index, graph

def add_to_index(index, keyword, url):
	if keyword in index:
		index[keyword].append(url)
	else:
		index[keyword] = [url]

def lookup(index, keyword):
	if keyword in index:
		return index[keyword]
	else:
		return None

def add_page_to_index(index, url, content):
	words = content.split()
	for item in words:
		add_to_index(index, item, url)

def make_big_index(size):
	index = []
	letters = ['a', 'a', 'a', 'a', 'a', 'a', 'a']
	while len(index) < size:
		word = make_string(letters)
		add_to_index(index, word, 'fake')
		for i in range(len(letters) - 1, 0, -1):
			if letters[i] < 'z':
				letters[i] = chr(ord(letters[i]) + 1)
				break
			else:
				letters[i] = 'a'
	return index

def computing_ranks(graph):
	d = 0.8
	numLoops = 10

	ranks = {}
	npages = len(graph)
	for page in graph:
		ranks[page] = 1.0 / npages;

	for i in range(0, numLoops):
		newranks = {}
		for page in graph:
			points = (1 - d) / npages
			for node in graph:
				if page in graph[node]:
					points = points + d * (ranks[node])
			newranks[page] = points
		ranks = newranks
	return ranks

index, graph = crawl_web("http://home.ustc.edu.cn/~sa614220/")
ranks = computing_ranks(graph)
print ranks

