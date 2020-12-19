from bs4 import BeautifulSoup
import requests, urllib, os, json, argparse
import terminal_banner, termcolor, platform, datetime

op = ''

banner_text = """
 **       ** ****     ** **   ** ******** ** ****     ** *******   ******** *******  
/**      /**/**/**   /**/**  ** /**///// /**/**/**   /**/**////** /**///// /**////** 
/**      /**/**//**  /**/** **  /**      /**/**//**  /**/**    /**/**      /**   /** 
/**      /**/** //** /**/****   /******* /**/** //** /**/**    /**/******* /*******  
/**      /**/**  //**/**/**/**  /**////  /**/**  //**/**/**    /**/**////  /**///**  
/**      /**/**   //****/**//** /**      /**/**   //****/**    ** /**      /**  //** 
/********/**/**    //***/** //**/**      /**/**    //***/*******  /********/**   //**
//////// // //      /// //   // //       // //      /// ///////   //////// //     // 
"""
desc = "Find Links for Computer Science or any other Topics on Medium or GeeksforGeeks"
dev_info = """
v1.1
Developed by: Saksham Singh
"""

if(platform.system() == 'Windows'):
    os.system('cls')
if (platform.system() == 'Linux'):
    os.system('clear')

banner = terminal_banner.Banner(banner_text)
print(termcolor.colored(banner.text,'cyan'), end="")
print(termcolor.colored(desc,'white', attrs=['bold']), end = "")
print(termcolor.colored(dev_info,'yellow'))

def create_url_medium(query, count='10'):
    global url
    url = "https://medium.com/search/posts?q="+urllib.parse.quote(query)+"&count="+count
    
def create_urlgeeksforgeeks(query,count='10'):
	global url
	url = "https://www.geeksforgeeks.org/search/"+query

def do_medium():
    global op
    create_url_medium(query,count)
    print("[+] Finding atmost %s articles on medium..." %count)
    
    try:
        page = requests.get(url)
    except requests.ConnectionError:
        print("[-] Can't connect to the server. Are you connected to the internet?")
        exit()

    soup = BeautifulSoup(page.content, 'html.parser')
    # print(page.content)
    print("[+] FOUND")
    print("[+] Listing articles...")
    for divs in soup.find_all('div', class_='postArticle-content'):
        for anchors in divs.find_all('a'):
            for h3 in anchors.find_all('h3'):
                try:
                    op += "-"*70 + "\n" + h3.contents[0] + ": " + anchors['href'] + "\n"
                except:
                    pass
    print(op)

argp = argparse.ArgumentParser(usage = "scraper.py -t TYPE -q QUERY -c [COUNT]")
argp.add_argument("-t","--type",required= True)
argp.add_argument("-q","--query",required= True)
argp.add_argument("-c","--count")
argp.add_argument("-o","--output")
parser = argp.parse_args()
type = parser.type
query = parser.query
count = parser.count
output = parser.output
if(count == None): count = '10'


def do_geeksforgeeks():
    global op
    create_urlgeeksforgeeks(query,count)
    print("[+] Finding atmost %s articles on GeeksforGeeks..." %count)
    
    try:
        page = requests.get(url)
    except requests.ConnectionError:
        print("[-] Can't connect to the server. Are you connected to the internet?")
        exit()

    soup = BeautifulSoup(page.content, 'html.parser')
    # print(page.content)
    print("[+] FOUND")
    print("[+] Listing articles...")
    for divs in soup.find_all('div', class_='postArticle-content'):
        for anchors in divs.find_all('a'):
            for h3 in anchors.find_all('h3'):
                try:
                    op += "-"*70 + "\n" + h3.contents[0] + ": " + anchors['href'] + "\n"
                except:
                    pass
    print(op)

argp = argparse.ArgumentParser(usage = "scraper.py -t TYPE -q QUERY -c [COUNT]")
argp.add_argument("-t","--type",required= True)
argp.add_argument("-q","--query",required= True)
argp.add_argument("-c","--count")
argp.add_argument("-o","--output")
parser = argp.parse_args()
type = parser.type
query = parser.query
count = parser.count
output = parser.output
if(count == None): count = '10'

do_medium() if(type == 'medium') else do_geeksforgeeks()

if(output):
    try:
        file = open(output,"w", encoding= "UTF-8")
        file.write("LinkFinder Scan Results at %s" %datetime.datetime.now()+"\n\n")
        file.write("Query: %s for %s results from %s\n\n" %(query, count, type))
        file.write(op)
        file.close()
        print("Output written to file %s" %output)
    except FileExistsError:
        print("Writing to output failed: File already exists")
    except IOError:
        print("Writing to file failed. Does the path exists? Check permissions and disk space.")
