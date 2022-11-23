import os 
import spacy
import pandas as pd
from utils import change_date_format
from extract import *
from database import add_row, select_last_id


## Excel proccessing functions 
def process_row(row):
    # TABLE DWH_PATIENT
    lastname = row["NOM"].upper()
    firstname = row["PRENOM"].upper()
    birth_date = change_date_format(row["DATE_NAISSANCE"])
    sex = row["SEXE"]
    maiden_name = process_female_name(row["SEXE"])
    address = row["ADRESSE"]
    phone = row["TEL"]
    zip_code = row["CP"]
    city = row["VILLE"]
    death_date = row["DATE_MORT"]
    country = row["PAYS"]
    latitude, longitude = process_coordinates(row['PAYS'],row['CP'])
    death_code = row['DATE_MORT']
    update_date = get_update_date()
    upload_id = "Null" # Since we do not have any updates for now

    
    #TABLE DWH_PATIENT_IPPHIST
    hospital_patient_ID = row["HOSPITAL_PATIENT_ID"]
    origin_patient_ID = "SIH"
    upload_id = "Null"
    master_patient_ID = get_master_ID()


    DWH_PATIENT_table_data =  {
        "LASTNAME" : lastname,
        "FIRSTNAME" : firstname,
        "BIRTH_DATE" : birth_date,
        "SEX" : sex,
        "MAIDEN_NAME" : maiden_name,
        "RESIDENCE_ADDRESS" : address,
        "PHONE_NUMBER" : phone,
        "ZIP_CODE" : zip_code,
        "RESIDENCE_CITY" : city,
        "DEATH_DATE" : death_date,
        "RESIDENCE_COUNTRY" : country,
        "RESIDENCE_LATITUDE" : latitude,
        "RESIDENCE_LONGITUDE" : longitude,
        "DEATH_CODE" : death_code,
        "UPDATE_DATE" : update_date,
        "BIRTH_COUNTRY" : country,
        "BIRTH_CITY" : city,
        "BIRTH_ZIP_CODE" : zip_code,
        "BIRTH_LATITUDE" : latitude,
        "BIRTH_LONGITUDE" : longitude,
        "UPLOAD_ID" : upload_id
    }

    DWH_PATIENT_IPPHIST_data = {
        "HOSPITAL_PATIENT_ID" : hospital_patient_ID,
        "ORIGIN_PATIENT_ID" : origin_patient_ID,
        "MASTER_PATIENT_ID" : master_patient_ID,
        "UPLOAD_ID" : upload_id
    }

    return DWH_PATIENT_table_data, DWH_PATIENT_IPPHIST_data


def procces_all_data():
    data = pd.read_excel("export_patient.xlsx")
    for _, row in data.iterrows():
        DWH_PATIENT_table_data, DWH_PATIENT_IPPHIST_data = process_row(row)
        add_row(DWH_PATIENT_table_data, "drwh.db", "DWH_PATIENT")
        # get select from table the last id 
        patient_num = select_last_id("drwh.db", "DWH_PATIENT")
        DWH_PATIENT_IPPHIST_data["PATIENT_NUM"] = patient_num
        add_row(DWH_PATIENT_IPPHIST_data, "drwh.db", "DWH_PATIENT_IPPHIST")



# Document Processing functions
def process_file(file):    
    nlp = spacy.load('fr_core_news_sm') 
    patient_num = file.split('_')[0]  #extraction du IPP
    id_doc_source = file.split('_')[1].split('.')[0] #extraction id doc

    document_type = file.split('_')[1].split('.')[1] 

    #si l'origine  DOSSIER_PATIENT/RADIOLOGIE_SOFTWARE
    document_origin_code = get_document_origin(file)
    displayed_text = get_text(f"fichiers source/{file}", document_origin_code)
    #diviser le text en tokens 
    doc = nlp(displayed_text)
    tokens = [token.text for token in doc if (not token.is_punct) and (not token.is_space)]
    #date du document  
    document_date = get_date(displayed_text, tokens)
    author = get_author(displayed_text, tokens)
    title = get_title(tokens)
    extractconcept_done_flag = 1
    extractcontext_done_flag = 1
    enrgene_done_flag = 0
    enrichtext_done_flag = 1
    update_date = get_update_date()
    upload_id = "Null" # Since we do not have any updates for now

    file_date = {
        "DOCUMENT_TYPE" : document_type,
        "ID_DOC_SOURCE" : id_doc_source,
        "PATIENT_NUM" : patient_num,
        "TITLE" : title,
        "DOCUMENT_ORIGIN_CODE" : document_origin_code,
        "DOCUMENT_DATE" : document_date,
        "DISPLAYED_TEXT" : displayed_text,
        "AUTHOR" : author,
        "EXTRACTCONTEXT_DONE_FLAG" : extractcontext_done_flag,
        "EXTRACTCONCEPT_DONE_FLAG" : extractconcept_done_flag,
        "ENRGENE_DONE_FLAG" :enrgene_done_flag,
        "ENRICHTEXT_DONE_FLAG" : enrichtext_done_flag,
        "UPDATE_DATE" : update_date,
        "UPLOAD_ID" : upload_id
    }
    return file_date


def process_files():
    file_list = os.listdir("fichiers source")
    for file in file_list:
        file_data = process_file(file)
        add_row(file_data, "drwh.db", "DWH_DOCUMENT")

procces_all_data()