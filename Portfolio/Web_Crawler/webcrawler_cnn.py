# Tera Parish       txp200011
# Bridgette Bryant  bmb180001
import os
import re
from bs4 import BeautifulSoup
import requests
import urllib
import ssl
ssl.match_hostname = lambda cert, hostname: True
ssl._create_default_https_context = ssl._create_unverified_context


def crawl(count, que, file):
    #print("In crawl")
    #print("count: ", count)
    # If we have reached our maximum count, return
    if count == 7:
        return
    if len(que) == 0:
        return

    r = requests.get(que.pop())
    data = r.text
    soup = BeautifulSoup(data, features="lxml")

    # write urls to a file

    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        #print(link_str)
        if 'Ukraine' in link_str or 'ukraine' in link_str or 'Russia' in link_str or 'russia' in link_str:
            #print("contains key word!")
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
                #print('MOD:', link_str)
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if link_str.startswith('http') and 'linkedin' not in link_str and 'instagram' not in link_str and 'facebook' not in link_str and 'twitter' not in link_str and 'google' not in link_str and 'buzzfeed' not in link_str and 'subscription' not in link_str and 'suscrip' not in link_str and link_str not in que:
                file.write(link_str + '\n')
                que.append(link_str)
                #print("saved: ", link_str)
                count += 1
                # If we have reached our maximum count, return
                if count == 7:
                    return
                #print("count 2: ", count)
                crawl(count, que, file)
                #print("count 3: ", count)
                # If we have reached our maximum count, return
                if count == 7:
                    return
    return

def is_visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


def scrape(urls):
    #print(os.listdir())
    os.chdir("dem_urls")
    #print(os.listdir())
    for cur_url in urls:
        # Creates the text file name for each url
        file_name = cur_url.replace("/", "")
        file_name = file_name.replace(":", "")
        file_name = file_name.replace("?", "")
        file_name = file_name.replace("<", "")
        file_name = file_name.replace("\"", "")
        file_name = file_name.replace("\\", "")
        file_name = file_name.replace("|", "")
        file_name = file_name.replace("*", "")
        file_name = file_name.replace("#", "")
        file_name = file_name.replace("=", "")
        file_name = file_name.replace("_", "")
        file_name = file_name.replace("-", "")
        file_name = file_name.replace(".", "") + '.txt'

        file_name = file_name.replace("https", "")
        #print("filename: ", file_name)
        # Create a new file to write to for each url
        with open(file_name, 'w', encoding='utf-8') as file:
            #print("cur_url: ", cur_url)
            try:
                html = urllib.request.urlopen(cur_url)
                soup = BeautifulSoup(html, features="lxml")
                data = soup.findAll(text=True)
                result = filter(is_visible, data)
                temp_list = list(result)  # list from filter
                temp_str = ' '.join(temp_list)
                #print(temp_str)
                # Write all the text to the file
                file.write(temp_str)
                file.close()
            except:
                # We get here when a website detected our scraper
                # I chose to respect the websites policy and print this instead
                # of using a workaround to prevent detection.
                print("Error occurred scraping website (likey anti-scraper our bot-detected): ", cur_url)
                file.close()
                # Deletes empty file
                os.remove(file_name)

if __name__ == '__main__':
    # the queue to hold our urls for crawl
    que = []
    count = 0

    # Add our starting URLS to the queue
    que.append('https://www.cnn.com/europe/live-news/russia-ukraine-war-news-10-09-22/index.html')




    with open('dem_urls.txt', 'w') as file:
        file.write('https://www.cnn.com/europe/live-news/russia-ukraine-war-news-10-09-22/index.html' + '\n')




        crawl(count, que, file)


    unique_urls_found = set()

    # Read in the file of urls and save only the unique ones (it will likely have many repeats)
    with open('dem_urls.txt', 'r') as file:
        urls_found = file.read().splitlines()

    # Close the file
    file.close()
    for u in urls_found:
        #print(u)
        unique_urls_found.add(u)
    print(unique_urls_found)
    print("number of urls: ", len(unique_urls_found))

    # Scrape all the text from the unique urls
    scrape(unique_urls_found)


    # end of program
    print("end of crawler")