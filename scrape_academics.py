import requests
from bs4 import BeautifulSoup

ssl_verify_path = 'ch.pem'
url = 'https://genealogy.math.ndsu.nodak.edu/id.php?id=13141'
page = requests.get(url,verify=ssl_verify_path)


soup = BeautifulSoup(page.content,'html.parser')

# Get all of the fields I want, and print so it is neat
name = soup.find('h2')
name_string = name.text.strip()

mathsci = name.find_next('p')
mathsci_link = name.find_next('a')
mathsci_string = mathsci_link['href']

# The spans are nested, so pull the full string which gives [phd, university, year]
# Split list into two to combine everything but year, then get year as last element
degree_year = mathsci.find_next('span')
degree_year_string = degree_year.text.strip().rsplit(None,1)[1] # probably want as date for db

college = degree_year.find_next('span')
college_string = college.text.strip()

dissertation = college.find_next('div')
dissertation_string = dissertation.text.strip().split('\n')
dissertation_string_final = dissertation_string[len(dissertation_string)-1]

classification = dissertation.find_next('div')
classification_string = classification.text.strip()
classification_split_text = classification_string.split(':')[1]


# It is combined on an em dash
# Need to regex to remove
import re
classification_split_utf = re.sub(u'\u2014','--',classification_split_text)

classification_number = str(classification_split_utf.split('--')[0]).strip()
classification_name_string = classification_split_utf.split('--')[1]

academic = {
    "Name": name_string,
    "MathSci": mathsci_string,
    "Degree Year": degree_year_string,
    "University": college_string,
    "Dissertation Title": dissertation_string_final,
    "Math Genre Number": classification_number,
    "Math Subfield": classification_name_string
}

for attribute in academic:
    print(academic[attribute])
