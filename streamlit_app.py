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
def make_mcaddon(mob_eggs, copper, potions, arrows, enchantment_books, source_directory, delay, is_void_gen, output_file, customized):
    backup_randompick_path = 'Packs/LOstDev404/RandomItemSkyblock/functions/randompick.mcfunction_backup'
    backup_randomize_path = 'Packs/LOstDev404/RandomItemSkyblock/functions/randomize.mcfunction_backup'

    shutil.copyfile('Packs/LOstDev404/RandomItemSkyblock/functions/randompick.mcfunction', backup_randompick_path)
    shutil.copyfile('Packs/LOstDev404/RandomItemSkyblock/functions/randomize.mcfunction', backup_randomize_path)
    randompick_path = 'Packs/LOstDev404/RandomItemSkyblock/functions/randompick.mcfunction'
    with open(randompick_path, 'r') as f:
        randompick_data = f.read()
        current_number = 1103
    for _ in range(mob_eggs):
        randompick_data += f"\nexecute as @s[scores={{random={current_number}}}] run function variants/runeggs"
        current_number += 1
    for _ in range(copper):
        randompick_data += f"\nexecute as @s[scores={{random={current_number}}}] run function variants/runcopper"
        current_number += 1
    for _ in range(potions):
        randompick_data += f"\nexecute as @s[scores={{random={current_number}}}] run function variants/runpotions"
        current_number += 1
    for _ in range(arrows):
        randompick_data += f"\nexecute as @s[scores={{random={current_number}}}] run function variants/runarrows"
        current_number += 1
    for _ in range(enchantment_books):
        randompick_data += f"\nexecute as @s[scores={{random={current_number}}}] run function variants/runbooks"
        current_number += 1
    with open(randompick_path, 'w') as f:
        f.write(randompick_data)
    randomize_path = 'Packs/LOstDev404/RandomItemSkyblock/functions/randomize.mcfunction'
    with open(randomize_path, 'r') as f:
        randomize_data = f.read()
    randomize_data = randomize_data.replace('itemamount', str(current_number))
    with open(randomize_path, 'w') as f:
        f.write(randomize_data)
    generate_mcaddon(source_directory, delay, is_void_gen, output_file, customized)

    shutil.copyfile(backup_randompick_path, 'Packs/LOstDev404/RandomItemSkyblock/functions/randompick.mcfunction')
    shutil.copyfile(backup_randomize_path, 'Packs/LOstDev404/RandomItemSkyblock/functions/randomize.mcfunction')
    os.remove(backup_randompick_path)
    os.remove(backup_randomize_path)

def generate_mcaddon(source_directory, delay, is_void_gen, output_file, customized):
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
        if customized:
            modified_manifest_data = manifest_data.replace(
            'packname', f'Random Item Skyblock ({delay} Seconds) | No Void Gen Beta 0.3 | Customized'
            ).replace(
            'packdescription', '§l§dNo Void Gen Customized §f| §l§bInstructions: §r§fPut this on a §l§6new world §r§fduring world creation. §f| §l§bPack created by: §r§aLOde404 / Grexzn'
            )
        else:   
            modified_manifest_data = manifest_data.replace(
                'packname', f'Random Item Skyblock ({delay} Seconds) | No Void Gen Beta 0.3'
            ).replace(
            'packdescription', '§l§dNo Void Gen §f| §l§bInstructions: §r§fPut this on a §l§6new world §r§fduring world creation. §f| §l§bPack created by: §r§aLOde404 / Grexzn'
        )
        start_replacement = 'randomstartnvg'
    else:
        if customized:
            modified_manifest_data = manifest_data.replace(
            'packname', f'Random Item Skyblock ({delay} Seconds) | 1.2 | Customized'
            ).replace(
                    'packdescription', '§l§cDO NOT PUT ON PRE-EXISTING WORLDS! §f| §l§dCustomized §f| §l§bInstructions: §r§fPut this on a §l§6new world §r§fduring world creation. §f| §l§bPack created by: §r§aLOde404 / Grexzn'
        )
        else:
            modified_manifest_data = manifest_data.replace(
            'packname', f'Random Item Skyblock ({delay} Seconds) | 1.2'
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

st.title('MCADDON Custom Value Manager `Version: 0.14`')
st.write('Contact `LOstDev404` on Discord for any bugs, questions, or suggestions.')

main_option = st.selectbox('Choose a pack / option:', ['Random Item Skyblock', '-Changelogs-'])

if main_option == 'Random Item Skyblock':
    delay = st.number_input('How many seconds delay do you want?:', min_value=1, step=1)
    ris_option = st.selectbox('Choose a version:', ['Normal', 'No Void Gen (Beta)'])
    if ris_option:
        customized = st.checkbox('Customize further')
        if customized:
            st.warning("Don't Change these values if you don't know what you're doing!")
            mob_eggs = st.number_input('How much `mob egg` receive chance do you want?:', min_value=1, step=1, value=40)
            copper = st.number_input('How much `copper` receive chance do you want?:', min_value=1, step=1, value=16)
            potions = st.number_input('How much `potion` receive chance do you want?:', min_value=1, step=1, value=6)
            arrows = st.number_input('How much `tipped arrow` receive chance do you want?:', min_value=1, step=1, value=4)
            enchantment_books = st.number_input('How much `enchantment book` receive chance do you want?:', min_value=1, step=1, value=2)
            
        if st.button('Get download link'):
            source_directory = 'Packs/LOstDev404/RandomItemSkyblock'
            if ris_option == 'Normal':
                output_file = f'Random Item Skyblock {delay} Seconds.mcaddon'
                is_void_gen = False
            elif ris_option == 'No Void Gen (Beta)':
                output_file = f'Random Item Skyblock {delay} Seconds | No Void Gen Beta 0.2.mcaddon'
                is_void_gen = True
            if not customized:
                mob_eggs = 40
                copper = 16
                potions = 6
                arrows = 4
                enchantment_books = 2

            make_mcaddon(mob_eggs, copper, potions, arrows, enchantment_books, source_directory, delay, is_void_gen, output_file, customized)
            
if main_option == '-Changelogs-':
    
    st.markdown("## **`Addon Manager | 0.14`:**")
    st.markdown("- Patched a bug causing no 'variants' to be added if the user didn't check the 'Customized futher' checkmark.\n - Date: *10/24/2024*")
    st.write("---")
    st.markdown("## **`Addon Manager | 0.13`:**")
    st.markdown("- Added bundles and colored bundles as receivable items on Random Item Skyblock.\n - Added the option for users to modify the chance of receiving certain items on Random Item Skyblock.\n  - Date: *10/23/2024*")
    st.write("---")
    st.markdown("## **`Addon Manager | 0.12`:**")
    st.markdown("- Fixed a formatting issue in Random Item Skybock's 'manifest.json' (in the pack description) that was causing the pack to not work on realms.\n - Renamed 'RIS' to 'RandomItemSkyblock' and moved it to 'Packs/LOstDev404/RandomItemSkyblock'.\n - Made the web icon have MCAddon logo, and MCAddon Manager text.\n - Date: *10/20/2024*")
    st.write("---")
    st.markdown("## **`Addon Manager | 0.11`:**")
    st.markdown("- Added changelogs.\n - Date: *10/19/2024*")
