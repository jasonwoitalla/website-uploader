from bs4 import BeautifulSoup
import os

output_file = True

tracker_code = '''window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

gtag('config', 'G-45WN5BP4LL');'''

def parse_page(index):
    print("Parsing", index)
    with open(index, encoding='utf8') as fp:
        soup = BeautifulSoup(fp, "lxml")

    for style in soup.find_all('style'):
        if style.get('id') == "et-builder-module-design-10-cached-inline-styles":
            print("Replaced a background image url")
            unicode_str = str(style.string)
            style.string.replace_with(unicode_str.replace("http://localhost/jasonwoitalla/website/wp-content/uploads/2020/12", "images"))
    
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
    
    src1 = soup.new_tag('script')
    src1['async'] = None
    src1['src'] = 'https://www.googletagmanager.com/gtag/js?id=G-45WN5BP4LL'
    print(src1)

    src2 = soup.new_tag('script')
    src2.append(tracker_code)
    print(src2)
    
    soup.head.append(src1)
    soup.head.append(src2)
    print(soup.head)

    # save changes
    if output_file:
        html = soup.prettify("utf-8")
        with open(index, "wb") as file:
            file.write(html)

direcotry = 'website'
count = 0
for root, dirnames, filenames in os.walk(direcotry):
    for filename in filenames:
        if filename.endswith('.html'):
            fname = os.path.join(root, filename)
            count += 1
            parse_page(fname)

print("Total Pages Changed", count)