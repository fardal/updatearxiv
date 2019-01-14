
###    #!/Users/fardal/anaconda/bin/python

import sys, os, webbrowser

def checkupdate(filename):
    arxivname = os.path.splitext(os.path.basename(filename))[0]
    url = "https://ui.adsabs.harvard.edu/#abs/arXiv:%s" % arxivname
    webbrowser.open(url)
    
    
if __name__ == "__main__":
    assert(len(sys.argv)==2)
    checkupdate(sys.argv[1])
