import os
import zipfile
import requests
import streamlit as st
import uuid
import json
import shutil

def generate_uuids():
    return str(uuid.uuid4()), str(uuid.uuid4())

def modify_files_with_delay(source_dir, delay, packname, description, startfile):
    manifest_path = os.path.join(source_dir, 'manifest.json')
    timer_path = os.path.join(source_dir, 'functions', 'timer.mcfunction')
    tick_path = os.path.join(source_dir, 'functions', 'tick.mcfunction')
    
    # Generate new UUIDs
    uuid1, uuid2 = generate_uuids()

    # Read and replace in manifest.json
    with open(manifest_path, 'r') as file:
        manifest_data = file.read()
    original_manifest_data = manifest_data
    modified_manifest_data = manifest_data.replace('uuid1', uuid1).replace('uuid2', uuid2).replace('timedelay', str(delay)).replace('packname', packname).replace('packdescription', description)
    
    # Read and replace in timer.mcfunction
    with open(timer_path, 'r') as file:
        timer_data = file.read()
    modified_timer_data = timer_data.replace('timedelay', str(delay))
    
    # Read and replace in tick.mcfunction
    with open(tick_path, 'r') as file:
        tick_data = file.read()
    modified_tick_data = tick_data.replace('startfile', startfile)
    
    # Write modified data back to files
    with open(manifest_path, 'w') as file:
        file.write(modified_manifest_data)
    with open(timer_path, 'w') as file:
        file.write(modified_timer_data)
    with open(tick_path, 'w') as file:
        file.write(modified_tick_data)

    return original_manifest_data, timer_data, tick_data

def revert_files(source_dir, original_manifest_data, original_timer_data, original_tick_data, backup_dimensions):
    manifest_path = os.path.join(source_dir, 'manifest.json')
    timer_path = os.path.join(source_dir, 'functions', 'timer.mcfunction')
    tick_path = os.path.join(source_dir, 'functions', 'tick.mcfunction')
    
    # Revert changes in manifest.json
    with open(manifest_path, 'w') as file:
        file.write(original_manifest_data)
    
    # Revert changes in timer.mcfunction
    with open(timer_path, 'w') as file:
        file.write(original_timer_data)

    # Revert changes in tick.mcfunction
    with open(tick_path, 'w') as file:
        file.write(original_tick_data)

    # Restore dimensions if backup exists
    dimensions_path = os.path.join(source_dir, 'dimensions')
    if backup_dimensions:
        shutil.move(backup_dimensions, dimensions_path)

def zip_files_to_mcaddon(source_dir, output_filename):
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(source_dir))  # Exclude source_dir from path
                zipf.write(file_path, arcname)

def upload_to_fileio(file_path):
    with open(file_path, 'rb') as file:
        response = requests.post('https://file.io', files={'file': file})
    response_data = response.json()
    return response_data.get('link')

st.title('`LOstDev404s` MCADDON Custom Value Manager')

main_option = st.selectbox('Choose a pack:', ['Random Item Skyblock', 'Unfinished'])

if main_option == 'Random Item Skyblock':
    ris_option = st.selectbox('Choose a version:', ['Normal', 'No Void Gen (Beta)'])
    
    if ris_option:
        delay = st.number_input('How many seconds delay do you want? (Only integers are allowed.)', min_value=1, step
