""" Crawl http://abcnotation.com to get dataset of traditional musics. """

import requests
import bs4
import time
import pickle
import os.path
import argparse
import re

root_url = 'http://abcnotation.com'
index_url = root_url + '/searchTunes?q=C:trad&f=c&o=a&s=0'

parser = argparse.ArgumentParser()
parser.add_argument('--num-pages', '-n', default=500, type=int,
                    help='Number of pages to be searched for musics.')
args = parser.parse_args()

def get_links(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "lxml")
    links = []
    for el in soup.findAll('li'):
        tune_link = el.find('a', href=True, text='tune page')
        if tune_link:
            links.append(root_url + tune_link['href'])
    next_url = soup.find('a', href=True, text='next')
    print(next_url)
    if next_url:
        next_url = root_url + next_url['href']
    return links, next_url

def crawl_links(index_url):
    all_links = []

    links, next_url = get_links(index_url)
    all_links += links
    count = 1
    while next_url is not None and count < args.num_pages:
        time.sleep(0.5) # Be nice
        links, next_url = get_links(next_url)
        all_links += links
        count += 1

    return all_links

def get_musics(links):
    pattern = re.compile('^([A-Za-z]):')

    musics = []
    for url in links:
        # Get only musics from this guy. Let's make things easier for the network
        if 'dl.dropboxusercontent.com/u/4496965' not in url:
            continue
        time.sleep(0.5) # Be nice
        print(url)
        try:
            response = requests.get(url, timeout=5)
            soup = bs4.BeautifulSoup(response.text, "lxml")
            text = soup.select('textarea')[0].get_text().lstrip(' \n').rstrip('\n')
            res = ''
            good = False
            for l in text.split('\n'):
                p = pattern.match(l)
                if pattern.match(l):
                    c = p.group(1)
                    if c in ['Q', 'M', 'L', 'K']: # Fields to keep
                        res += l
                        res += '\n'
                else:
                    if l[0] != '%': # Ignore comment line
                        # Strip spaces and newlines
                        good = True
            res += '\n'
            if good:
    	           musics.append(text.encode('ascii',errors='ignore'))
            else:
                print 'Bad:\n%s' % text.encode('ascii',errors='ignore')
        except Exception, e:
            print e
        if len(musics) == 10:
            print 'Writing!'
            yield musics
            musics = []

if not os.path.exists('links.pkl'):
    links = crawl_links(index_url)
    pickle.dump(links, open('links.pkl', 'wb'))
else:
    links = pickle.load(open('links.pkl', 'rb'))

musics = get_musics(links)

try:
    os.remove("input.txt")
except:
    pass

with open("input.txt", "a") as f:
    for chunk in musics:
        f.write('\n\n'.join(chunk))
