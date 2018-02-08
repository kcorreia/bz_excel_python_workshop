


"""

Can download Anaconda package on Windows, Mac, Linux
https://www.anaconda.com/download/

macOS and OSX have Python 2.7 install.

Suggest installing and using latest Python 3.x version

One common issue with Python 2 vs 3 is print requires parentheses:
	print 'my text'
		works in Python 2 but not Python 3
	print('my text')
		works with Python 2 and Python 3

"""



########################################################################



import pandas as pd
import html5lib

url='https://simple.wikipedia.org/wiki/List_of_U.S._states'
# reads the html source file and loads each table in a pandas dataframe
f_states=pd.read_html(url) 

# check number of tables
len(f_states)

# access first table using indicies (starts at zero)
# the header is included within the table
df=f_states[0]


# get dataframe column names
df.columns
# column names as a list
df.columns.tolist()

# get dataframe indicies
df.index
# indicies as a list
df.index.tolist()

# retreive index=9, column=1: Florida
df[1][9]


# convert columns to lists
state_codes=df[0][1:].tolist()
state_names=df[1][1:].tolist()

# create a sublist of states that end with the letter a
states_a=[]
for state_name in state_names:
	if state_name.lower()[-1]=='a':
		states_a.append(state_name)

states_a

# sublist can also be created with something called list comprehension
# this yields the same output as the above function
# this is what people refer to as Pythonic (one liner, easy to read)
states_a=[state_name for state_name in state_names if state_name.lower()[-1]=='a']

# lists can be combined into tuples with zip
states_tuple=zip(state_codes,state_names)
# 'de-tuple' using zip(*)
state_codes_de,state_names_de=zip(*states_tuple)

# create a dictionary using dictionary comprehension
states_dict={state_code:state_name for state_code,state_name in states_tuple}

states_dict['WA']




# write table to file, with tab separated, do not include header
# or indices in output
# \t is the tab delimitter
df.to_csv('states.txt',sep='\t',header=None,index=False)

########################################################################


import pandas as pd
import html5lib

url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_L'

fsa=pd.read_html(url)



# we can iterate the dataframe using iterrows() function
for index,row in fsa[0].iterrows():
	# iterate over columns in the table
	for col in fsa[0].columns:
		# use column and index to retrieve table values
		name=fsa[0][col][index]
		# display FSA only if Brampton or Milton in cell
		if 'Brampton' in name:
			name
		elif 'Milton' in name:
			name


########################################################################

# urllib can be used to download webpages
import urllib
# Recommended to parse HTML
# previously I used basic functions in Python such as split and find
from bs4 import BeautifulSoup



def get_lat_long(fsa):
	"""
	Load 3 letter FSA into function, get Lat/Long via Wikipedia
	"""
	request=urllib.urlopen('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_'+fsa[0:1])
	# request will always return with no errors but this doesn't mean the website loaded properly
	# you should check the status via getcode()
	# 200 means the webpage loaded properly
	# 404 means it did not load
	# there are other codes but these are the two most important
	if request.getcode()==200:
		# convert request into string (what you see in page source on your web browser)
		page=request.read()
		# load string into beautiful soup
		soup = BeautifulSoup(page, 'html.parser')
		# itereate over all td tags. Return list of td if fsa in text contained within td
		# since there is likely only once match we use only the first item in the list with [0]
		# example is shown below for L9T fsa
		"""
		<td width="11.1%" valign="top"><b>L9T</b><br />
		<span style="font-size: smaller; line-height: 125%;"><a href="/wiki/Milton,_Ontario" title="Milton, Ontario">Milton</a></span></td>
		"""
		match=[td for td in soup.find_all('td') if fsa in td.text][0]
		# get the url contained within the matched fsa-td
		url_city=match.find('a')['href']
		url='https://en.wikipedia.org'+url_city
		# open the city webpage on Wikipedia
		request=urllib.urlopen(url)
		# could have another request check for 200/404
		page=request.read()
		soup = BeautifulSoup(page, 'html.parser')
		# retreive lat/long from span tags
		# <span class="geo">43.50833; -79.88333</span>
		coords=soup.find('span',{'class':'geo'}).text
		print(filter(None,match.text.split('\n')))
		return coords



get_lat_long('V3M')


########################################################################


import pandas as pd
import xml.etree.ElementTree as ET
from Bio import SeqIO


# join combines list of strings into one string with specificed insertion between strings
# in this case it is %20 for space encoding
search_terms='%20'.join(['xylose','reductase','saccharomycotina'])
# you can try building urls on uniprot website and port them to Python by adding columns in your query
# current query has a limit of 10 entries
url='http://www.uniprot.org/uniprot/?sort=score&desc=&compress=no&query='+search_terms+'&fil=&limit=10&force=no&preview=true&format=tab&columns=id,entry%20name,reviewed,protein%20names,genes,organism'

# empty columns are filled with empty strings via fillna() function
uniprot=pd.read_csv(url,sep='\t').fillna('')


"""

Write fasta files of entries in dataframe

"""

# iterate over each row in the dataframe
for index,row in uniprot.iterrows():
	entry=uniprot['Entry'][index]
	url='http://www.uniprot.org/uniprot/'+entry+'.fasta'
	# access fasta text file via url
	page=urllib.urlopen(url).read()
	# write to file
	# \n is a new line character
	# \r\n is sometimes used with Windows
	# this file method appends via 'a'
	# you can also read files via 'r'
	# or (over)write via 'w'
	open('XR.fasta','a').write(page+'\n')



"""

Rename fasta to only include Entry name
old fasta header: >sp|O74237|XYL1_CANTE NAD(P)H-dependent D-xylose reductase OS=Candida tenuis GN=XYL1 PE=1 SV=1
new fasta header: >XYL1_CANTE

"""

# create an empty list
my_records=[]
# iteraete over each re
for seq_record in SeqIO.parse('XR.fasta','fasta'):
	# get the last text field in the id
	seq_record.id=seq_record.id.split('|')[-1]
	seq_record.description=''
	my_records.append(seq_record)

# write the list of records as a fasta file
SeqIO.write(my_records, "XR_renamed.fasta", "fasta")

"""
Access xml files for all entries in dataframe to download citation information
Write to file

root.getchildren()

"""



for index,row in uniprot.iterrows():
	organism=uniprot['Organism'][index]
	print(organism)
	print('\n')
	entry=uniprot['Entry'][index]
	url='http://www.uniprot.org/uniprot/'+entry+'.xml'
	page=urllib.urlopen(url).read()
	# load xml into Element Tree to parse xml file
	root=ET.fromstring(page)
	# find all tags with citations
	# finding tags requires some practice with ET
	citations=root.findall(".//{http://uniprot.org/uniprot}citation")
	# iterate over all citation tags
	for citation in citations:
		# get text contained within citation tags
		title=citation.find(".//{http://uniprot.org/uniprot}title").text
		# find pubmed ID's within citation tags
		pubmeds=[dbref.attrib['id'] for dbref in citation.findall(".//{http://uniprot.org/uniprot}dbReference") if dbref.attrib['type']=='PubMed']
		pubmed=';'.join(pubmeds)
		print('\t'+pubmed+'\t'+title)
		# write pubmed's to file
		open('XR_papers.txt','a').write('\t'.join([organism,pubmed,title])+'\n')
	print('\n\n\n\n')



########################################################################


import pandas as pd

# search for term within database/db in NCBI
# can search other dbs like nuccore, gene, protein, pubmed or other file types
# more details: https://www.ncbi.nlm.nih.gov/books/NBK25499/
record=pd.read_json('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=genome&term=saccharomycotina&retmax=1000&retmode=json')

# get ids from search results in genomes
genomes=record['esearchresult']['idlist']

###################

# retreive each organism name by requesting individual id's
# this is a slower process than next method

for genome in genomes:
	record=pd.read_json('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=genome&id='+genome+'&retmax=1000&retmode=json')
	org=record['result'][genome]['organism_name']
	print(org)


###################

# retreive organism names by requesting list of id's
# this is faster than previous method

ids=','.join(genomes)
record=pd.read_json('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=genome&id='+ids+'&retmax=1000&retmode=json')
genomes_uids=record['result']['uids']

for uid in genomes_uids:
	org=record['result'][uid]['organism_name']
	print(org)




########################################################################


"""

Send automated emails

"""

# if you are using gmail you need to generate an app password:
# https://security.google.com/settings/security/apppasswords

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText 
username='USERNAME'
password='PASSWORD'
fromaddr = "from@gmail.com"
toaddr = "to@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test script"
body = 'Test email message.'
msg.attach(MIMEText(body, 'plain'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(username,password)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()




########################################################################

"""

Find emails in Inbox from bill.gross@gmail.com with subject 'CEF analysis'
Downloads attachments

"""

import imaplib
import email

mail_server='smtp.gmail.com'
username='USERNAME'
password='PASSWORD'

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(username, password)
# using this flag keeps unread flag on emails
readonly = True
# can also try getting all emails not in inbox
mail.select("INBOX", readonly)
result, data = mail.search(None, "ALL")

id_list=data[0].split(' ')


# process the last 50 emails
for id_current in id_list[-200:]:
	result, data = mail.fetch(id_current, "(RFC822)") # fetch the email body (RFC822) for the given ID
	print(id_current,email_message['To'],email_message['From'],email_message['Subject'])
	raw_email=data[0][1]
	email_message = email.message_from_string(raw_email)
	if 'CEF analysis' in email_message['Subject'] and email_message['From']=='bill.gross@gmail.com':
		msg = email.message_from_string(raw_email)
		for part in list(msg.walk()):
			#if part.get('Content-Disposition') is None:
			if part.get_filename()==None:
				# print part.as_string()
				continue
			fileName = part.get_filename()
			print(fileName)
			fileName=email_message['Date']+'_'+fileName
			# can create new folders with os
			fp = open(fileName, 'wb')
			fp.write(part.get_payload(decode=True))
			fp.close()




########################################################################

# class and function example to download attachments
# https://stackoverflow.com/questions/6225763/downloading-multiple-attachments-using-imaplib

import email
import imaplib
import os

class FetchEmail():
    connection = None
    error = None
    def __init__(self, mail_server, username, password):
        self.connection = imaplib.IMAP4_SSL(mail_server)
        self.connection.login(username, password)
        self.connection.select(readonly=False) # so we can mark mails as read
    def close_connection(self):
        """
        Close the connection to the IMAP server
        """
        self.connection.close()
    def save_attachment(self, msg, download_folder="/Users/kcorreia/Downloads"):
        """
        Given a message, save its attachments to the specified
        download folder (default is /tmp)
        return: file path to attachment
        """
        att_path = "No attachment found."
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            att_path = os.path.join(download_folder, filename)
            if not os.path.isfile(att_path):
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
        return att_path
    def fetch_unread_messages(self):
        """
        Retrieve unread messages
        """
        emails = []
        (result, messages) = self.connection.search(None, 'UnSeen')
        if result == "OK":
            for message in messages[0].split(' '):
                try: 
                    ret, data = self.connection.fetch(message,'(RFC822)')
                except:
                    print("No new emails to read.")
                    self.close_connection()
                    exit()
                msg = email.message_from_string(data[0][1])
                if isinstance(msg, str) == False:
                    emails.append(msg)
                response, data = self.connection.store(message, '+FLAGS','\\Seen')
            return emails
        self.error = "Failed to retreive emails."
        return emails
    def parse_email_address(self, email_address):
        """
        Helper function to parse out the email address from the message
        return: tuple (name, address). Eg. ('John Doe', 'jdoe@example.com')
        """
        return email.utils.parseaddr(email_address)








########################################################################



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert



"""
You can use selenium to control a web browser
I have found that I need to periodically update the driver to get my code to work
https://sites.google.com/a/chromium.org/chromedriver/downloads

Check out my uoftmedstore scrapping scripts for another example
https://github.com/kcorreia/uoftmedstore_scrape
"""

browser = webdriver.Chrome('/Users/kcorreia/Downloads/chromedriver_2018_mac')

seqid='>PHO3.2'
sequence='MQLNNYIAFLALATACLAKTILLTNDDSWAATNIRATYYQLKDAGHDVYLVAPVSQRSGW\
GGKFDVPSSPTLETDGEFAYVKAGEPSWGHEVDDDHIWYFNGTPASAVAFALNYVFPYYF\
AEKGNNVTVDLVVSGPNEGTNMSPGMYTLSGTMGATYNSVYRGYPAVAFSGSNGNNSFFK\
DSLDLEDKLDPSTIYANLVVDFVAQLFTAQGDNSRTLPLGVGINVNFPPVGYQNESCIAP\
KWVNTRLTGAYASGADLAYNATSNSFIWQQTSWSGLQVCYNGDCSLPSENLIVQYTECST\
SVSAFSVDYDAKLSLSQEVTALLEPLFS'


browser.get('http://phobius.sbc.su.se/')

text='\n'.join(['>'+seqid,sequence,''])
browser.find_element_by_name("protseq").clear()
browser.find_element_by_name('protseq').send_keys(text)
browser.find_element_by_xpath("//input[@type='submit']").click()
# can parse new file to get image or raw data




