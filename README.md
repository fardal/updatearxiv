# updatearxiv

updatearxiv.py is a quick and dirty Python script to update stored PDF files from arXiv to their current versions: published, if available, or updated arxiv version, if it exists.  It demonstrates use of the APIs for both ADS and arXiv.  Valid ADS account with API token required (it's easy to set up).  

A much simpler script, checkarxiv.py, pulls up the ADS web page corresponding to a single arXiv filename, which will show whether the paper is published, but doesn't update anything.  This doesn't require an ADS token.  

### Use case

When I look at the daily arXiv summary I sometimes say "hm, that could be interesting", and dump a PDF file into a folder on my disk.  Then I ignore it, often for months.  When I do get around to reading some papers, the initial arXiv version is often obsolete.  This script lets me efficiently update to the most recent version.  Those who use sophisticated paper managers are entitled to sneer, if they handle the updating themselves.

### Installing

Usage requires an ADS account and corresponding API access token.  See instructions on the ADS site in the Account menu, "Customize Settings" for how to generate the token.  Edit the script updatearxiv.py to contain your ADS account name.  Then see https://pypi.org/project/keyring/#configure-your-keyring-lib for how to enter this in keyring.  Or just enter the token in the script, if you don't care about keeping it secret.

For command-line usage: stick the script updatearxiv.py somewhere in your path, then say python -B -m updatearxiv [DIRECTORY-OR-PDFFILENAME] [DIRECTORY-OR-PDFFILENAE]...  But if you want to make it a drag and drop app on Mac OS, as I did, see AUTOMATOR.txt.

Using checkupdate.py is done in a similar way, but it doesn't require any account.

### Limitations

This only works on files saved with the default arxiv filenames such as 1812.12345.pdf.  It doesn't know anything about the contents of the PDF file.  So even if you've already updated the paper, it will do so again.  It won't tell you if the paper was rejected.  I currently have it to move the original files to .bak files rather than deleting them, which could be annoying.  There are some ADS entries that lack paper source entries which make the script crash; this seems like an ADS bug, and I haven't bothered to work around it.

### Requirements

Python modules requests, keyring.  On my system I need a customized Python installation rather than the system default.  Also requires the ADS account/token.

