# SPYS.ONE TOOLS
# Created By. LuthfiZXC
# Github    : https://github.com/LuthfiZXC
# Youtube   : https://www.youtube.com/luthfizxc
# Facebook  : https://www.facebook.com/luthfi.syaifullah.90

#----- PLEASE DON'T RECODE OR REUPLOAD THIS SCRIPT -----#

#----- Importing Module -----#
import os
import re
import sys
import datetime
from os import name, system, getcwd
from time import sleep

try:
    import js2py
    import requests
    from tqdm import tqdm
    from bs4 import BeautifulSoup

except ModuleNotFoundError:
    system('pip install js2py')
    system('pip install requests')
    system('pip install bs4')
    system('pip install tqdm')
    import js2py
    import requests
    from tqdm import tqdm
    from bs4 import BeautifulSoup


#----- Color Format -----#
R = '\033[31m'
G = '\033[32m'
Y = '\033[33m'
B = '\033[34m'
M = '\033[35m'
C = '\033[36m'
W = '\033[37m'
BR= '\033[91m'
BG= '\033[92m'
BY= '\033[93m'
BB= '\033[94m'
BM= '\033[95m'
BC= '\033[96m'
BW= '\033[97m'


#----- All Variables Here -----#
web = 'http://spys.one'
spys = [
    '/squid-proxy/',
    '/mikrotik-proxy/',
    '/en/socks-proxy-list/',
    '/en/https-ssl-proxy/',
    '/en/http-proxy-list/',
    '/en/non-anonymous-proxy-list/',
    '/en/anonymous-proxy-list/',
]
filename = [
        'squid',
        'mikrotik',
        'socks',
        'http_ssl',
        'http',
        'NOA',
        'Anonim'
    ]
name = [
        'Squid Proxy',
        'Mikrotik Proxy',
        'Socks Proxy',
        'Http SSL Proxy',
        'Http Proxy',
        'Non Anonim Proxy',
        'Anonim Proxy'
    ]
ua = {
  'User-Agent':'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'
  }
proxies = []    #Variable to save proxy list
sort = []       
algorithm = 0   #Just variable to choose decrypt algorithm

#----- Get File Directory -----#
loc = getcwd()
if '\\' in loc:
    loc = loc.replace('\\', '/')

if not os.path.exists('data'):
    os.mkdir('data')


#----- Function to open txt files -----#
def file(self):
    file = open('data/'+filename[self]+'.txt', 'a+')
    return file

#----- Welcome Text -----#
def welcome():
    print(f'''{BG}
   ____ ___ __  __ ____   ____   _  __ ____
  / __// _ \\\ \/ // __/  / __ \ / |/ // __/  \x1B[3mTools\x1b[23m
 _\ \ / ___/ \  /_\ \ _ / /_/ //    // _/  
/___//_/     /_//___/(_)\____//_/|_//___/  {BR}V{BM}1.2{BG}
\x1B[3m{BY} Created by Luthfi ZXC\x1B[23m{BC}
#------------------------------------------------#{W}''')

#----- Menu List -----#
def menu():
    print(f'{B}MENU :')
    #-- Autocreate List --#
    for i,j in enumerate(name):
        print(f'{BG}    [{i+1}] {j}')
    print('\n    [99] Run All')
    print(f'{R}    [0]  Exit{W}')

#----- Clear Screen Function -----#
def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


#----- Get Current Time -----#
def time():
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return now


#----- Function to print text without newline -----#
def prints(self):
    return sys.stdout.write(self)


#----- Function to sort data -----#
def sorting(sort, data):
    pjg = len(sort)
    for i in range(pjg-1,0,-1):
        for j in range(i):
            if sort[j]<sort[j+1]:
                temp = sort[j]
                temp1 = data[j]
                sort[j] = sort[j+1]
                data[j] = data[j+1]
                sort[j+1] = temp
                data[j+1] = temp1

#----- Data To Be Sent To Target -----#
def data1(show,country,anm,ssl,type):
    data = {
        'xpp'   :show,
        'tldc'  :country,
        'xf1'   :anm,
        'xf2'   :ssl,
        'xf5'   :type
    }
    return data


def data2(show,anm,ssl,port,types):
    data={
        'xpp':show,
        'xf1':anm,
        'xf2':ssl,
        'xf4':port,
        'xf5':types
    }
    return data

#----- Function To Get Proxy and Decrypting Port From Target -----#
def decrypt(html):
    global proxies
    data = {}
    proxies = []

    soup = BeautifulSoup(html, 'html.parser')

    #-- Auto determine decrypting method --#
    try:
        rumus = re.search(r'type=\"text/javascript\">eval\((.*?)\)\n</', html).group(1)
        algorithm = 0

    except AttributeError:
        rumus = re.search(r'</table><script type=\"text/javascript\">(.*?);</script>', html).group(1)
        algorithm = 1

    #-- Getting target index --#
    target = soup.find_all('tr', onmouseover="this.style.background='#002424'")
    print(f'\r[-] Catching {len(target)} proxies...')
    print(f'{G}[-] Decrypting Port{W}')

    #-- Decrypting Port --#
    for i in tqdm(target,desc='[-] Process', bar_format='{l_bar}\033[32m{bar}\033[37m| '):
        port=''
        ip = re.search(r'class=\"spy14\">(.*?)<script', str(i)).group(1)
        raw_port = re.search(r'font>\"\+(.*?)\)<', str(i)).group(1)
        #-- Using ALGORITHM 1 --#
        if algorithm == 0:
            split_port = raw_port.replace('(', '').replace(')', '').split('+')
            
            #-- decrypting required port value --#
            for i in split_port:
                if not i in data:
                    dat = f'''eval({rumus}); a = {i}'''
                    parsed_port = str(js2py.eval_js(dat))
                    data[i]=parsed_port

            #-- merge port --#
            for j in split_port:
                port += data[j]
                
            #-- Saving Proxy to "proxies" variable --#
            proxies.append(ip+':'+port)

        #-- Using ALGORITM 2 --#
        else:
            split_port = re.findall(r'\((.*?)\^', raw_port)
            port = ''
            parsing = {}
            rms = rumus.split(';')

            for i in rms:
                if '^' in i:
                    j = i.split('^')[0].split('=')
                    a = j[0]
                    b = j[1]
                    parsing[a] = b

            for k in split_port:
                port += parsing[k]

            proxies.append(ip+':'+port)
    print(f'{G}[✓] Done{W}')

#----- Run Task -----#
def run(self):
    if self == '0':
        exit()

    elif self == '99':
        for a in range(0,7):
            run(a+1)
            print('\n#------------------------------------------------#')

    elif self == '':
        main()

    else:
        mode = int(self)
        print(f'{BR}             - {name[mode-1]} List -')
        print(f'{G}[-] Sending request to \n{B}    {web+spys[mode-1]}')
        r = requests.post(web + spys[0], data=data1(5, 0, 0, 0, 0), headers= ua, timeout=10)
        decrypt(r.text)
        sleep(0.5)
        file(mode-1).write(f'  #---- {time()} ----#\n')
        for i in tqdm(proxies, desc='[-] Writing', bar_format='{l_bar}\033[32m{bar}\033[37m| '):
            file(mode-1).write(i+'\n')
        file(mode-1).write('\n\n')
        print(f'{G}[✓] Done{W}')
        print(f'{Y}Proxy list saved to:\n{loc}/data/{filename[mode-1]}.txt{W}')

#----- MAIN Function -----$
def main():
    clear()
    welcome()
    menu()
    mode = input('\nSelect : ')

    try:
        clear()
        welcome()
        run(mode)
    except requests.exceptions.ConnectionError:
        print(f' {R}Connection Error...\n Please check your network !')

    except (ValueError, IndexError, TypeError):
        print(f' {R}[!] Invalid Command!')
        input(f'    Press enter to return to menu{W}')
        main()
    input('\nPress enter to return to menu.')

    main()


if __name__ == '__main__':
    main()
