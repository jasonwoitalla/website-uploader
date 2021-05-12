from bs4 import BeautifulSoup
import os

def parse_page(index):
    print("Parsing", index)
    with open(index) as fp:
        soup = BeautifulSoup(fp, "lxml")
    for link in soup.find_all('a'):
        href = link.get('href')
        if "#" in href and "index.html" not in href and not href[0] == "#": # this link jumps to a point in the page
            href = href.replace("#", "/index.html#")
        print(href.replace("http://localhost/jasonwoitalla/website", "https://www.jasonwoitalla.com"))
        link['href'] = href.replace("http://localhost/jasonwoitalla/website", "https://www.jasonwoitalla.com") # replaces localhost link to a website link
    
    for image in soup.find_all('img'):
        print(image.get('srcset'))
        print(image.get('sizes'))
        del image['srcset'] # we don't need the dynamic images
        del image['sizes']
    
    for form in soup.find_all('form'):
        print(form.get('action').replace("http://localhost/jasonwoitalla/website", "https://www.jasonwoitalla.com"))
        form['action'] = form.get('action').replace("http://localhost/jasonwoitalla/website", "https://www.jasonwoitalla.com")
    
    for linktag in soup.find_all('link'):
        linktag_href = linktag.get('href')
        if "localhost" in linktag_href:
            print(linktag.get('rel'))
            linktag.decompose() # deletes the link tag that contains localhost

    for src in soup.find_all('script'):
        if "localhost" in str(src.string) and "DIVI" not in str(src.string):
            src.decompose() # deletes whatever these scripts do
            # print(src.string)
    
    # save changes
    html = soup.prettify("utf-8")
    with open(index, "wb") as file:
        file.write(html)

direcotry = 'website'
for root, dirnames, filenames in os.walk(direcotry):
    for filename in filenames:
        if filename.endswith('.html'):
            fname = os.path.join(root, filename)
            parse_page(fname)