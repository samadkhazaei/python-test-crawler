from requests.api import get
import validators
import requests
from bs4 import BeautifulSoup

def get_link_qty(links):
    cont = 0
    for l in links:
        cont += 1
        if type(links[l]) == list:
            cont += len(links[l])
    return cont

def get_all_links(url, links, limit):
    linkqty = get_link_qty(links)     
    if linkqty >= limit:
        return links
    else:
        print("[+] Getting all links from: " + url)
        reqs = requests.get(url)
        content = reqs.text    
        soup = BeautifulSoup(content, 'html.parser')    
        tmpArr = []

        for link in soup.find_all('a'):    
            href = link.get('href')
            if href is not None:
                if(validators.url(href)):
                  tmpArr.append(link.get('href'))

        currentUrl = reqs.url 
        currentUrlQty = 0
        if(len(tmpArr) > 0) and (currentUrl not in links):
            links[str(currentUrl)] = tmpArr
            currentUrlQty = len(tmpArr)
        else:
            links[str(currentUrl)] = 'No links found'
        
        newQty = get_link_qty(links)        
        
        if newQty < limit :
            print("[+] Remaining =", limit - newQty) 
            print("==========================================")
            if type(links[str(currentUrl)]) is list and limit - newQty > currentUrlQty + 3:            
                for link in links[str(currentUrl)]:        
                    newLinks = get_all_links(str(link), links, limit)
                    if get_link_qty(newLinks) >= limit:
                        return newLinks
            else:
                return links
        else :        
            return links

print("Please insert Url (with 'http or https'):")
url = input()
if validators.url(url) :
    print("Url is valid")
    print("Please insert limit of links for crawling: ")
    limit = int(input())
    links = get_all_links(str(url), {}, limit)
    print("please enter your file name to save links:")
    file_name = input()
    file = open(file_name, "w")
    for link in links:
        file.write(link + "\n")
        if(type(links[link]) == list):
            for l in links[link]:
                file.write("    "+ l + "\n")        
else:
    print("Url is not valid")

