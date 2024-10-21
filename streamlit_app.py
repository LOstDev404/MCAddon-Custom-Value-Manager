import os
import zipfile
import requests
import streamlit as st
import uuid
import json
import shutil
st.set_page_config(
    page_title="MCAddon Manager",
    page_icon="mcaddon-logo.ico"
)
def generate_uuids():
    return str(uuid.uuid4()), str(uuid.uuid4())

def modify_files_with_delay(source_dir, delay, is_void_gen):
    manifest_path = os.path.join(source_dir, 'manifest.json')
    tick_path = os.path.join(source_dir, 'functions', 'tick.json')
    timer_path = os.path.join(source_dir, 'functions', 'timer.mcfunction')
    
    uuid1, uuid2 = generate_uuids()
    with open(manifest_path, 'r') as file:
        manifest_data = file.read()
    original_manifest_data = manifest_data
    
    if is_void_gen:
        modified_manifest_data = manifest_data.replace(
            'packname', f'Random Item Skyblock ({delay} Seconds) | No Void Gen Beta 0.2'
        ).replace(
            'packdescription', '§l§dNo Void Gen §f| §l§bInstructions: §r§fPut this on a §l§6new world §r§fduring world creation. §f| §l§bPack created by: §r§aLOde404 / Grexzn'
        )
        start_replacement = 'randomstartnvg'
    else:
        modified_manifest_data = manifest_data.replace(
            'packname', f'Random Item Skyblock ({delay} Seconds) | 1.1'
        ).replace(
            'packdescription', '§l§cDO NOT PUT ON PRE-EXISTING WORLDS! §f| §l§bInstructions: §r§fPut this on a §l§6new world §r§fduring world creation. §f| §l§bPack created by: §r§aLOde404 / Grexzn'
        )
        start_replacement = 'randomstart'
    
    modified_manifest_data = modified_manifest_data.replace('uuid1', uuid1).replace('uuid2', uuid2).replace('timedelay', str(delay))

    with open(tick_path, 'r') as file:
        tick_data = file.read()
    original_tick_data = tick_data
    modified_tick_data = tick_data.replace('startfile', start_replacement)

    with open(timer_path, 'r') as file:
        timer_data = file.read()
    modified_timer_data = timer_data.replace('timedelay', str(delay))

    with open(manifest_path, 'w') as file:
        file.write(modified_manifest_data)
    with open(tick_path, 'w') as file:
        file.write(modified_tick_data)
    with open(timer_path, 'w') as file:
        file.write(modified_timer_data)

    return original_manifest_data, original_tick_data, timer_data

def revert_files(source_dir, original_manifest_data, original_tick_data, original_timer_data):
    manifest_path = os.path.join(source_dir, 'manifest.json')
    tick_path = os.path.join(source_dir, 'functions', 'tick.json')
    timer_path = os.path.join(source_dir, 'functions', 'timer.mcfunction')

    with open(manifest_path, 'w') as file:
        file.write(original_manifest_data)
    with open(tick_path, 'w') as file:
        file.write(original_tick_data)
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
#---------------------------------------- UI Starts Here ----------------------------------------

st.title('MCADDON Custom Value Manager')
st.write('**Made by `LOstDev404`**')

main_option = st.selectbox('Choose a pack / option:', ['Random Item Skyblock', '-Changelogs-'])

if main_option == 'Random Item Skyblock':
    ris_option = st.selectbox('Choose a version:', ['Normal', 'No Void Gen (Beta)'])
    if ris_option:
        delay = st.number_input('How many seconds delay do you want?:', min_value=1, step=1)

        if st.button('Get download link'):
            source_directory = 'Packs/LOstDev404/RandomItemSkyblock'
            if ris_option == 'Normal':
                output_file = f'Random Item Skyblock {delay} Seconds.mcaddon'
                is_void_gen = False
            elif ris_option == 'No Void Gen (Beta)':
                output_file = f'Random Item Skyblock {delay} Seconds | No Void Gen Beta 0.2.mcaddon'
                is_void_gen = True

            original_manifest_data, original_tick_data, original_timer_data = modify_files_with_delay(source_directory, delay, is_void_gen)

            dimensions_path = os.path.join(source_directory, 'dimensions')
            if is_void_gen and os.path.exists(dimensions_path):
                shutil.move(dimensions_path, dimensions_path + '_disabled')
            elif not is_void_gen and os.path.exists(dimensions_path + '_disabled'):
                shutil.move(dimensions_path + '_disabled', dimensions_path)

            zip_files_to_mcaddon(source_directory, output_file)
            download_link = upload_to_fileio(output_file)
            st.success(f'Download link: {download_link}')

            revert_files(source_directory, original_manifest_data, original_tick_data, original_timer_data)
            
            if os.path.exists(dimensions_path + '_disabled'):
                shutil.move(dimensions_path + '_disabled', dimensions_path)

            os.remove(output_file)

if main_option == '-Changelogs-':
    st.markdown("## **`Addon Manager | 0.13`:**")
    st.markdown("- Fixed a formatting issue in Random Item Skybock's 'manifest.json' (in the pack description) that was causing the pack to not work on realms.\n - Renamed 'RIS' to 'RandomItemSkyblock' and moved it to 'Packs/LOstDev404/RandomItemSkyblock'.\n - Made the web icon have MCAddon logo, and MCAddon Manager text.\n - Date: *10/20/2024*")
    st.write("--------------------------------------------------------------------------")
    st.markdown("## **`Addon Manager | 0.12`:**")
    st.markdown("- Added changelogs.\n - Date: *10/19/2024*")
