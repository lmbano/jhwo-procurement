import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import time
import pandas as pd
import os
import shutil

# find more emojis here : https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="JHWO Procurement",
                   page_icon=":tada:", layout="wide")

#######################
# Page title

####################

def save_file(file, local_directory, file_name):
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)
    file.seek(0)
    file_data = file.read()
    with open(os.path.join(local_directory, file_name), "wb") as f:
        f.write(file_data)


def check_file_save(file, service_id, selected_service_code_key, file_name):
    if file:
        try:
            if selected_service_code_key is None:
                print("Folder name not found" + selected_service_code_key)
            else:
                local_directory = selected_service_code_key+service_id
                save_file(file, local_directory, file_name)
                st.success("File saved as '{}' in the directory '{}'!".format(
                    file_name, local_directory))
        except Exception as e:

            print(f'An error occurred while uploading the file: {e}')


def get_key(dictionary, value):
    for key in dictionary:
        if dictionary[key] == value:
            return key
        return None


def find_keys(dictionary, value_list):
    keys = []
    for key, val in dictionary.items():
        if val == value_list:
            keys.append(key)
    return keys


def find_key(dictionary, value):
    return [key for key, val in dictionary.items() if val == value]


def get_value(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return None


dict_1 = {
    'ACCOMMODATION, CONFERENCING': ['JHWO/001'],
    'STATIONERY, PRINTING':  ['JHWO/002'],
    'REFRESHMENTS, LUNCH, TEAS AND CLEANING': ['JHWO/003'],
    'SERVICE STATION, VEHICLE REPAIR AND SERVICE': ['JHWO/004'],
    'ICT-COMPUTERS, SOFTWARE AND ACCESSORIES': ['JHWO/005'],
    'INTERNET, AIRTIME':  ['JHWO/006'],
    'COURIER': ['JHWO/007'],
    'PHARMACEUTICAL, MEDICAL SUPPLIERS':  ['JHWO/008'],
    'OFFICE FURNITURE': ['JHWO/009'],
    'HARDWARE, BUILDING MATERIAL, CHEMICALS': ['JHWO/010'],
    'IEC MATERIAL:FLYERS,BANNER, BILLBOARD PRINTING, IEC MATERIAL: T-SHIRTS,SHIRTS,HATS,FABRIC BRANDING':  ['JHWO/011'],
    'SOLAR SYSTEM': 'JHWO/012',
    'ELECTRICAL SUPPLIES AND SERVICES': ['JHWO/013'],
    'SECURITY SERVICES':  'JHWO/014',
    'BOREHOLE DRILLING AND INSTALLATION': ['JHWO/015'],
    'FENCING AND FENCING MATERIALS': ['JHWO/016'],
    'INSURANCE SERVICES': ['JHWO/017'],
    'VEHICLE HIRE SERVICES': ['JHWO/018'],
    'TELEPHONE, VIDEO AND VISUAL SERVICES': ['JHWO/019'],
    'FIRE EQUIPMENT SALES': ['JHWO/020'],
    'MOTORBIKE SALES': ['JHWO/021'],
    'PRINTER, COMPUTERS, PHOTOCOPIERS MAINTENANCE SERVICES': ['JHWO/022'],
    'AIR CONDITIONING SALES': ['JHWO/023'],
    'TRAVEL AGENTS': ['JHWO/024'],
    'CONSULTING SERVICES': ['JHWO/025'],
    'OUTDOOR ADVERTISING': ['JHWO/026'],
    'CONTRACTORS': ['JHWO/027']
}
dict_2 = {

    'JHWO/001': [
        'Hotel accommodation',
        'Conference rooms'],
    'JHWO/002': [
        'Printing',
        'Laminating',
        'Photocopying',
        'Stationery',
        'Office consumables',
        'Sign writing',
        'Computer consumables'],
    'JHWO/003': ['Groceries', 'Lunch', 'Cleaning materials'],
    'JHWO/004': [
        'Motor vehicle spares',
        'Bearings for electric motors, pumps and vehicles',
        'Rebounding of brake lining',
        'wheel drum skimming',
        'Tyres'],

    'JHWO/005': ['Hardware', 'Software', 'Networking', 'Maintenance'],

    'JHWO/006': ['Data bundle', 'Voice airtime'],

    'JHWO/007': ['Courier services'],

    'JHWO/008': [
        'Medical Drugs: Tablets, capsules, injectable, suspensions, vacuolates, creams, lotions,suppositories',
        'Surgical sundries: Bandages, dressings, catheters, blades, cannula, infusion giving sets',
        'Hospital furniture and equipment: Hospital beds, delivery beds, bedside lockers, drug lockers, bathroom scales, baby scales, BP machines, vital monitors, stethoscopes',
        'Disinfectants: Sodium hypochlorite, hand and floor sanitizers, carbolic agents'],

    'JHWO/009': ['Desk',
                 'Chairs visitors',
                 'Swivel chairs',
                 'Pilot desks'],

    'JHWO/010': [
        'Building materials',
        'Paints',
        'Plumbing materials',
        'Electrical materials',
        'Cleaning materials',
        'Protective clothing and uniforms',
        'Chemicals (general)',
        'Refuse bins'],

    'JHWO/011': [
        'Fabric',
        'Designing and sewing of organizational clothing',
        'Flyers',
        'Banner printing',
        'T-shirts ,shirts, hats branding'],

    'JHWO/012': [
        'Solar systems',
        'Tubing and wiring'],

    'JHWO/013': [
        'Electrical materials',
        'Tubing and wiring'],

    'JHWO/014': ['Security services of premises'],
    'JHWO/015': ['Borehole drilling and installation'],
    'JHWO/016': ['Fencing materials'],
    'JHWO/017': [],
    'JHWO/018': [],
    'JHWO/019': [],
    'JHWO/020': [
        'Fire extinguisher sales',
        'Installation',
        'Maintenance and service'],
    'JHWO/021': [
        'Motorbike sales',
        'Motorbike spares',
        'Maintenance and servic'],
    'JHWO/021': ['Repairs and maintenance of computers,laptops,photocopiers etc'],
    'JHWO/022': [
        'Air conditioners',
        'Installation',
        'Maintenance and service'],
    'JHWO/023': [],
    'JHWO/024': [],
    'JHWO/025': [],
    'JHWO/026': [
        'Roadshows services,truck hire,PA system and DJ'],
    'JHWO/027': [
        'Brick layers and plasters',
        'Welders',
        'Electricians',
        'Thatcher’s',
        'Carpenters',
        'Auto electricians',
        'Painters']


}
dict_3 = {
    'Hotel accommodation': 'a',
    'Conference rooms': 'b',
    'Printing': 'a',
    'Laminating': 'b',
    'Photocopying': 'c',
    'Stationery': 'd',
    'Office consumables': 'e',
    'Sign writing': 'f',
    'Computer consumables': 'g',
    'Groceries': 'a',
    'Lunch': 'b',
    'Cleaning materials': 'c',
    'Motor vehicle spares': 'a',
    'Bearings for electric motors, pumps and vehicles': 'b',
    'Rebounding of brake lining': 'c',
    'wheel drum skimming': 'd',
    'Tyres': 'e',
    'Hardware': 'a',
    'Software': 'b',
    'Networking': 'c',
    'Maintenance': 'd',
    'Data bundle': 'a',
    'Voice airtime': 'b',
    'Courier services': 'a',
    'Medical Drugs: Tablets, capsules, injectable, suspensions, vacuolates, creams, lotions,suppositories': 'a',
    'Surgical sundries: Bandages, dressings, catheters, blades, cannula, infusion giving sets': 'b',
    'Hospital furniture and equipment: Hospital beds, delivery beds, bedside lockers, drug lockers, bathroom scales, baby scales, BP machines, vital monitors, stethoscopes': 'c',
    'Disinfectants: Sodium hypochlorite, hand and floor sanitizers, carbolic agents': 'd',
    'Desk': 'a',
    'Chairs visitors': 'b',
    'Swivel chairs': 'c',
    'Pilot desks': 'd',
    'Building materials': 'a',
    'Paints': 'b',
    'Plumbing materials': 'c',
    'Electrical materials': 'd',
    'Cleaning materials': 'e',
    'Protective clothing and uniforms': 'f',
    'Chemicals (general)': 'g',
    'Refuse bins': 'h',
    'Fabric': 'a',
    'Designing and sewing of organizational clothing': 'b',
    'Flyers': 'c',
    'Banner printing': 'd',
    'T-shirts ,shirts, hats branding': 'e',
    'Solar systems': 'a',
    'Tubing and wiring': 'b',
    'Electrical materials': 'a',
    'Tubing and wiring': 'b',
    'Security services of premises': 'a',
    'Borehole drilling and installation': 'a',
    'Fencing materials': 'a',
    'Fire extinguisher sales': 'a',
    'Installation': 'b',
    'Maintenance and service': 'c',
    'Motorbike sales': 'a',
    'Motorbike spares': 'b',
    'Maintenance and servic': 'c',
    'Repairs and maintenance of computers,laptops,photocopiers etc': 'a',
    'Air conditioners': 'a',
    'Installation': 'b',
    'Maintenance and service': 'c',
    'Roadshows services,truck hire,PA system and DJ': 'a',
    'Brick layers and plasters': 'a',
    'Welders': 'b',
    'Electricians': 'c',
    'Thatcher’s': 'd',
    'Carpenters': 'e',
    'Auto electricians': 'f',
    'Painters': 'g'

}


image = Image.open('JHWO.jpg')


col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image(image)

with col3:
    st.write(' ')


# def load_lottieurl(url):
    # r = requests.get(url)
    # if r.status_code != 200:
    #    return None
    # return r.json

# ---LOAD ASSETS----

# lottie_coding = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_2glqweqs.json")
# lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")

# ---  HEADER SECTION ----
with st.container():
    st.subheader("Welcome to Jointed Hands Procurement page: ")
    st.title("For submiting documents ")
    st.write(
        "Please provide all the required documents , for more information go the link below")
    st.write("[ Learn More >> ](https://jointedhands.org)")

# ------ WHAT I DO ---

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("What we do")
        st.write('##')
        st.write(
            """


            JHWO 2022 Theme " EMBRACING SYSTEMS AND QUALITY"

            Strategic Pillars

            1. Health 

            2. Social Development 

            3. Resilient Strengthening 

            4. Disaster Risk Management 

            5. Strategic Information and Knowledge Management 

            

            """
        )
        st.write("find out more about JHWO at : (https://jointedhands.org)")
# File save function

    with right_column:
        st.title("Select servive of goods Category")
        selected_option = st.selectbox(
            "Select service or goods Category:", options=list(dict_1.keys()))
        st.write("You selected: ", selected_option)

        # Get the list of options from the second dictionary using the selected value from the first dictionary
        options = dict_2.get(dict_1.get(selected_option)[0])

        # Create the second dropdown given selected values in list1
        selected_item = ''
        if options:
            selected_item = st.selectbox(
                "Select Service or Goods:", options=options)
            st.write("Selected goods or Service: ", selected_item)
         
        else:
            st.write("No options available for the selected value.")
       
        selected_service=''
        if selected_item is not None:
            selected_service=get_value(dict_3,selected_item)
            print("Pring dictionary value........................... ", selected_service)

            print("printing option 2...................... ", selected_item)

        selected_service_code_key = ''.join(selected_option)
        saving_dir = get_value(dict_1, selected_service_code_key)
        saving_dir = ''.join(saving_dir)
        # Streamlit UI

        
         # Text inputs
        st.header('Company Details and Supporting Documents')
        company_input = st.text_input( "Enter company name : 👇",
                )
        if company_input:
            st.write("Welcome : ", company_input)

            # documents types type=["pdf","docx","txt"])
        date = st.date_input("Pick a date")

            # UI
            
# Saving proof of payment
        proof_of_payment = st.file_uploader(
                "Submit Proof of Payment", type=["pdf"])
        cr14_form = st.file_uploader("Submit CR14 form", type=["pdf","docx","pdf"])
        tax_clearence = st.file_uploader("Submit Valid tax Clearence", type=["pdf"])
        companny_profile = st.file_uploader("Submit Brief company profile", type=["pdf"])
        vat_certificate = st.file_uploader("Submit Vat Certificate or Letter that you are not VAT registered", type=["pdf"])
        praz_certificate = st.file_uploader("Submit PRAZ Cerificate", type=["pdf"])

            # Tracking uploaded files 
        uploaded_files = 0

        if proof_of_payment is not None:
            uploaded_files += 1
        if tax_clearence is not None:
            uploaded_files += 1
        if cr14_form is not None:
            uploaded_files += 1
        if companny_profile is not None:
            uploaded_files += 1
        if vat_certificate is not None:
            uploaded_files += 1
        if praz_certificate is not None:
            uploaded_files += 1

                   
            # Update the progress bar
        progress_bar = st.progress(0)
        progress_bar.progress(int(uploaded_files / 6 * 100))
            
        if uploaded_files < 6:
            st.empty()
        else:
            submit_button = st.button("Submit")
            if submit_button:
                file_name = company_input + " - Proof of payment.pdf"
                check_file_save(proof_of_payment,  "/"+selected_item+"/"+company_input,
                                    saving_dir, file_name)
                file_name = company_input + " - CRF Form.pdf"
                check_file_save(cr14_form, "/"+selected_item+"/"+company_input,
                                    saving_dir, file_name)
                file_name = company_input + " - Tax Clearence.pdf"
                check_file_save(tax_clearence, "/"+selected_item+"/"+company_input,
                                    saving_dir, file_name)
                file_name = company_input + " - Company Profile.pdf"
                check_file_save(companny_profile, "/"+selected_item+"/"+company_input,
                                    saving_dir, file_name)
                file_name = company_input + " - Vat Certificate.pdf"
                check_file_save(vat_certificate, "/"+selected_item+"/"+company_input,
                                    saving_dir, file_name)
                file_name = company_input + " - PRAZ Certificate.pdf"
                check_file_save(praz_certificate, "/"+selected_item+"/"+company_input,
                                    saving_dir, file_name)
                st.write("Files submitted successfully!")
           
  
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

