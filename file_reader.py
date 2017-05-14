"""
Script to export the Whatsapp group contacts to Google export format
"""

import glob,shutil, re
from bs4 import BeautifulSoup
from google_contacts_conf import GOOGLE_CONTACTS_CONF
# Config files...
root_path = './whatsapp_contacts/'
path = "{}/*.txt".format(root_path)
files = glob.glob(path)
output_folder = '{}output'.format(root_path)

OUTPUT_CONF = [key for key, val in GOOGLE_CONTACTS_CONF]


def is_no(contact):	
	# import pdb; pdb.set_trace()
	num_format = re.compile("^[-+]?[0-9]+")
	isnumber = re.match(num_format,contact)
	return isnumber

def concatenate(contact):
    contact = contact.split()    
    return u"".join(contact)


def find_nos(html, name_prefix):
    # Number of Contact in your group
    content = []
    number_of_contact = 0
    c = 0
    # BeautifulSoup object html content as argument
    soup = BeautifulSoup(html, "lxml")

    # for loop goes through every span in html content
    for i in soup.find_all('span'):
    	c = c+1
        # if we found span element with class attribute "emojitext ellipsify" and its title attribute on None
        if i.get('class') == ['emojitext', 'ellipsify'] and i.get("title") is not None:
            phone = concatenate(i.get_text())
            if is_no(phone):
            	content.append({'phone':phone, 'name':'{}{}'.format(name_prefix,c),'phone_type':'Mobile'})
            	# content.append(['',phone])


    print "The Total Number of Contacts are %s" % (len(content),)
    return content


def m():
	for file in files:
		file_obj = open(file, 'r')
		file_content = file_obj.read()
		file_name = file_obj.name.split('/')[-1].split('.')[0]		
		a = find_nos(file_content,file_name)
		print "####### Content of file: {}" .format(file)
		
		# Writing to FIle....
		print output_folder

		new_file = "{}/{}.csv".format(output_folder, file_name)
		print new_file
		new_file_obj = open(new_file, 'w')

		new_file_obj.write('{}\n'.format(','.join(OUTPUT_CONF)))
		i = 0
		for x in a:

			res = []
			for key, val in GOOGLE_CONTACTS_CONF:
				res.append(x.get(val,''))
			
			st = '{}\n'.format(','.join(res))

			new_file_obj.write(st)
		new_file_obj.close()
			

if __name__ == "__main__":
	m()

