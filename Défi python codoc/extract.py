import time
from datetime import datetime
import docx2txt
import fitz
import re
from utils import get_coordinates

# Functions to Extract from excel data
def process_coordinates(pays, CP):
        if '(Anglicized)' in pays:
            pays = pays.replace(" (Anglicized)", "")
        address = f"{CP}, {pays}"
        coordinates = get_coordinates(address)
        if coordinates:
            return coordinates
        else:
            address = pays
            time.sleep(2)
            return get_coordinates(address)

def process_female_name(sexe):
    if sexe == "M":
        return 0
    else:
        return None

def find_death_code(date):
    if str(date) == "nan":
        return 0
    else:
        return 1

def get_origin():
    return "SIH"

def get_update_date():
    return datetime.today().date()

def get_master_ID():
    """
    ???
    """
    return 1

#  Functions to extract from documents

def get_text(file_path,origin_code):
    txt = ""
    if origin_code == 'DOSSIER_PATIENT':
        doc = fitz.open(file_path)
        for page in doc :
            txt = txt + str(page.get_text())
    else:
        txt = docx2txt.process(file_path)
    txt = txt.replace('\n'," ")
    txt = re.sub("\s+"," ",txt)
    return txt.lower()

def get_date(displayed_text, tokens):
        date_extract_pattern = "[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}"
        date = re.findall(date_extract_pattern, displayed_text)
        if len(date) == 1 :
            return date[0]
        else:
            return tokens[tokens.index('du')+1]

def get_author(displayed_text, tokens):
    #author du fichier
    if 'dr' in tokens:
        return displayed_text.split('dr')[-1]
    else:
        return None

def get_title(tokens):
    if "ordonnance" in tokens :
        return "ordonnance"
    elif "consultation" in tokens:
        return 'compte de rendu de consultation'
    else:
        return "compte de rendu hospitalisation"

def get_document_origin(file):
    if (file.split('_')[1]).split('.')[1] == 'pdf':
        return "DOSSIER_PATIENT"
    else : 
        return "RADIOLOGIE_SOFTWARE"

