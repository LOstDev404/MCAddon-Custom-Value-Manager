import os
import zipfile
import requests
import streamlit as st
import uuid
import json
def generate_uuids():
    return str(uuid.uuid4()), str(uuid.uuid4())

def modify_files_with_delay(source_dir, delay):
    manifest_path = os.path.join(source_dir, 'manifest.json')
    timer_path = os.path.join(source_dir, 'functions', 'timer.mcfunction')

    uuid1, uuid2 = generate_uuids()

    with open(manifest_path, 'r') as file:
        manifest_data = file.read()
    original_manifest_data = manifest_data
    modified_manifest_data = manifest_data.replace('uuid1', uuid1).replace('uuid2', uuid2).replace('timedelay', str(delay))

    with open(timer_path, 'r') as file:
        timer_data = file.read()
    modified_timer_data = timer_data.replace('timedelay', str(delay))

    with open(manifest_path, 'w') as file:
        file.write(modified_manifest_data)
    with open(timer_path, 'w') as file:
        file.write(modified_timer_data)

    return original_manifest_data, timer_data

def revert_files(source_dir, original_manifest_data, original_timer_data):
    manifest_path = os.path.join(source_dir, 'manifest.json')
    timer_path = os.path.join(source_dir, 'functions', 'timer.mcfunction')

    with open(manifest_path, 'w') as file:
        file.write(original_manifest_data)

    with open(timer_path, 'w') as file:
        file.write(original_timer_data)

def zip_files_to_mcaddon(source_dir, output_filename):
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(source_dir))  
                zipf.write(file_path, arcname)

def upload_to_fileio(file_path):
    with open(file_path, 'rb') as file:
        response = requests.post('https://file.io', files={'file': file})
    response_data = response.json()
    return response_data.get('link')

st.title('`LOstDev404s` MCADDON Custom Value Manager')

main_option = st.selectbox('Choose an pack:', ['Random Item Skyblock', 'Unfinished'])

if main_option == 'Random Item Skyblock':
    ris_option = st.selectbox('Choose a version:', ['Normal', 'No Void Gen (Beta)'])

    if ris_option:
        delay = st.number_input('How many seconds delay do you want? (Putting anything other then numbers will cause an error.)', min_value=0, step=1)

        if st.button('Get download link'):
            if ris_option == 'Normal':
                source_directory = 'RIS'
                output_file = f'Random Item Skyblock {delay} Seconds.mcaddon'
            elif ris_option == 'No Void Gen (Beta)':
                source_directory = 'RISNVG'
                output_file = f'Random Item Skyblock {delay} Seconds) | No Void Gen Beta 0.2.mcaddon'

            original_manifest_data, original_timer_data = modify_files_with_delay(source_directory, delay)

            zip_files_to_mcaddon(source_directory, output_file)

            download_link = upload_to_fileio(output_file)
            st.success(f'Download link: {download_link}')

            revert_files(source_directory, original_manifest_data, original_timer_data)

            os.remove(output_file)
