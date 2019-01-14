"""Script to update files of form 1812.xxxxx.pdf to current versions"""

import requests
import urllib
import keyring
from tkinter import *

# https://pypi.org/project/keyring/#configure-your-keyring-lib
USER = 'fardal@stsci.edu'
token = keyring.get_password('ads', USER)

import sys, os

ACTIONLIST = []
GLOBALMESSAGE = []

def downloadpdf(url, destination):
    from urllib.request import Request
    req = Request(url)  
    headers = requests.utils.default_headers()
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'  # a lie, just trying to get it to work
    r = requests.get(url, headers=headers)
    if os.path.isfile(destination):
        os.rename(destination, destination+'.bak')
    with open(destination, "wb") as downloadfile:
        downloadfile.write(r.content)

        
def arxivupdated(arxivname):
    import xml.etree.ElementTree as ET
    arxivurl = 'http://export.arxiv.org/api/query?search_query=id:%s' % arxivname
    data = urllib.request.urlopen(arxivurl).read().decode('utf-8')
    root = ET.fromstring(data)
    versioned_id = ''
    # print(root)
    # print(root.tag)
    # print(root.attrib)
    for child in root:
        if child.tag.endswith('entry'):
            for grandchild in child:
                if grandchild.tag.endswith('id'):
                    # print(grandchild.tag, grandchild.attrib)
                    versioned_id = grandchild.text
                    break
            break
    # print('versioned id:')
    # print(versioned_id)
    version = int(versioned_id.split('v')[-1])
    # print('version: ', version)
    if version > 1:
        # print('Updated version available')
        return True
    else:
        return False


def update():
    for action in ACTIONLIST:
        downloadpdf(action['url'], action['destination'])

        
class NotifyFrame(Frame):
    def __init__(self, parent=None):
        # print('in notify frame')
        Frame.__init__(self, parent)
        message = '\n'.join([action['name']+': '+action['message'] for action in ACTIONLIST])
        win = Frame()
        win.pack()
        Label(win, text=message, justify=LEFT).pack(side=TOP)
        buttonframe = Frame(win)
        buttonframe.pack(side=BOTTOM, expand=NO)
        Button(buttonframe, text='OK', command=self.proceed).pack(side=LEFT)
        Button(buttonframe, text='Cancel',  command=win.quit).pack(side=RIGHT)
        self.win = win
        
    def proceed(self):
        update()
        self.win.quit()
        
    
class NotifyNoUpdateFrame(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        message = 'Found nothing to update.'
        win = Frame()
        win.pack()
        Label(win, text=message).pack(side=TOP)
        buttonframe = Frame(win)
        buttonframe.pack(side=BOTTOM, expand=NO)
        Button(buttonframe, text='OK', command=win.quit).pack(side=LEFT)
        
    
def notify():
    if len(ACTIONLIST) > 0:
        NotifyFrame().mainloop()
    else:
        NotifyNoUpdateFrame().mainloop()
    
    
def checkupdate(filename):
    if os.path.isdir(filename):
        for f in os.listdir(filename):
            checkupdate(os.path.join(filename, f))
    else:
        if os.path.splitext(filename)[1] == '.pdf':
            checkupdatefile(filename)

    
def checkupdatefile(filename):
    # print('checking filename: ', filename)
    arxivname = os.path.splitext(os.path.basename(filename))[0]
    try:
        month, index = arxivname.split('.')
        month = int(month)
        index = int(index)
    except ValueError:
        return  # assume not arxiv file
    
    r = requests.get("https://api.adsabs.harvard.edu/v1/search/query?q=identifier:arXiv:%s&fl=first_author,year,identifier,alternate_bibcode,bibcode,property,esources&rows=1" % arxivname, \
                     headers={'Authorization': 'Bearer ' + token})
    info = r.json()['response']['docs'][0]
    bibcode = info['bibcode']
    if 'PUB_PDF' in info['esources']:
        # print('Published')
        puburl = 'https://ui.adsabs.harvard.edu/link_gateway/%s/PUB_PDF' % bibcode
        # print('should download this file: ', puburl)
        ACTIONLIST.append(arxivaction(arxivname, 'Update to published', puburl, filename))
        
    else:
        # print('Not published')
        if arxivupdated(arxivname):
            arxivurl = 'https://ui.adsabs.harvard.edu/link_gateway/%s/EPRINT_PDF' % bibcode
            ACTIONLIST.append(arxivaction(arxivname, 'Update arxiv', arxivurl, filename))
    if len(ACTIONLIST) > 100:
        raise Exception('file list too long.')  # intended for small set of files

    
def arxivaction(arxivname, message, url, destination):
    return dict(name=arxivname, message=message, url=url, destination=destination)


if __name__ == "__main__":
    GLOBALMESSAGE.append(sys.argv)
    for argument in sys.argv[1:]:
        checkupdate(argument)
    notify()
