#!/usr/bin/python3
import json
import sys
import zlib
import os
import base64
import platform
import traceback
import psutil
from datetime import datetime

class Project:
    
    def create_blank_package():
        if os.path.exists('./package.json'):
            choice = None
            while not choice == 'y':
                choice = input('"package.json" already exists, remove and create new? (y/n): ')
                if choice == 'n':
                    os._exit(1)
                elif choice == 'y':
                    os.remove('package.json')

        blink_package_data = {
            "name": "Blink package",
            "description": "Blink project package.",
            "os": platform.system(),
            "version": "1.0",
            "addfiles": ["example.txt", "example2.txt"],
            "installpath": "/example/path/"
        }
        with open("package.json", 'w') as jpak:
            jpak.write(json.dumps(blink_package_data, indent='\t'))
        print('Created package.json')
    
    def build_package():
        try:
            print('Reading "package.json"')
            package_info = json.loads(open('./package.json', 'r').read())
        except:
            print('Unable to found "package.json" in current directory or "package.json" corrupted.'); os._exit(1)
        print('Package name: ' + package_info['name'])
        print('Description: ' + package_info['description'])
        print('Target OS: ' + package_info['os'])
        print('Version: ' + package_info['version'])
        print('Files count: ' + str(len(package_info['addfiles'])))
        print('Path to install: ' + package_info['installpath'])
        atc = None
        while not atc == 'y': 
            atc = input('All right? (y/n): ')
            if atc == 'n':
                os._exit(1)
        print('Building...')
        file_err = 0
        for file in package_info['addfiles']:
            if not os.path.exists('./'+file):
                print(f'ERR - File {file} does not exist')
                file_err = 1
        total_files_size = 0
        for file in package_info['addfiles']:
            total_files_size += os.path.getsize('./'+file)
        print('Total files size: '+str(total_files_size)+' bytes')
        if psutil.virtual_memory().available / 1.8 <= total_files_size:
            acc = None
            while not acc == 'y':
                acc = input('Most likely the program will fail to build the package due to lack of system resources.\nContinue? (y/n): ')
                if acc == 'n':
                    os._exit(1)
        if file_err == 1:
            print('Some files does not exist in current directory, fix and try again'); os._exit(1)
        print('Writing basic information...')
        open('package.acpe', 'a').write('pkgname:::' + package_info['name'] + '\n')
        open('package.acpe', 'a').write('description:::' + package_info['description'] + '\n')
        open('package.acpe', 'a').write('os:::' + package_info['os'] + '\n')
        open('package.acpe', 'a').write('version:::' + package_info['version'] + '\n')
        open('package.acpe', 'a').write('path:::' + package_info['installpath'] + '\n')
        print('Writing files...')
        for file in package_info['addfiles']:
            print(f'Reading {file}...')
            with open(f'./{file}', 'rb') as ufile:
                rdata = ufile.read()
            print(f'Encoding {file}...')
            bdata = base64.b64encode(rdata).decode()
            print(f'Writing {file}...')
            with open('package.acpe', 'a') as ufile:
                ufile.write(f'file:::{file}:::{bdata}\n')
        print('Compressing...')
        with open('package.acpe', 'rb') as ufile:
            data = ufile.read()
        os.remove('package.acpe')
        altnamebb = package_info['name']
        with open(f'{altnamebb}-{platform.system()}.acpe', 'wb') as endfile:
            endfile.write(zlib.compress(data))
        print(f'All done. Saved as {altnamebb}-{platform.system()}.acpe')

    def index_all_files():
        if not os.path.exists('package.json'):
            print('Create blink project firstly.')
            os._exit(1)
        print('Adding to "addfiles"...')
        file_index = []
        directory = '.'
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.relpath(os.path.join(root, file), directory)
                file_index.append(file_path)
        CZA = []
        for fpath in file_index:
            if not fpath.endswith(('acp.py', 'package.json')):
                CZA.append(fpath.replace('\\', '/'))
        data = json.loads(open('package.json', 'r').read())
        data['addfiles'] = CZA
        open('package.json', 'w').write(json.dumps(data, indent='\t'))
        print('Done, check "package.json".')
        


class Installer:
    def install_package(filename: str):
        if not os.path.exists(f'./{filename}'):
            print(f'File "{filename}" does not exist in this folder.'); os._exit(1)
        with open(f'./{filename}', 'rb') as ufile:
            cdata = ufile.read()
        print('Decompressing...')
        cdata = zlib.decompress(cdata).decode()
        print('Unpacking...')
        cdata = cdata.replace('\r', '')
        cdata = cdata.split('\n')
        pkgdata = {}
        files = {}
        for item in cdata:
            if item.startswith('pkgname:::'):
                pkgdata['name'] = item.replace('pkgname:::', '')
            elif item.startswith('description:::'):
                pkgdata['description'] = item.replace('description:::', '')
            elif item.startswith('os:::'):
                pkgdata['os'] = item.replace('os:::', '')
            elif item.startswith('version:::'):
                pkgdata['version'] = item.replace('version:::', '')
            elif item.startswith('path:::'):
                pkgdata['path'] = item.replace('path:::', '')
            elif item.startswith('file:::'):
                _, filename, bdata = item.split(':::')
                files[filename] = bdata
        ispkgnormal = True
        for key in ['os', 'name', 'description', 'version', 'path']:
            if not key in pkgdata.keys():
                print('FATAL - Corrupted package.'); os._exit(1)
        if len(files.keys()) <= 0:
            print('FATAL - Corrupted package, there are no files inside.'); os._exit(1)
        print('Package:')
        print(f"""-------
Name: {pkgdata['name']}
Description: {pkgdata['description']}
OS: {pkgdata['os']}
Version: {pkgdata['version']}
Path to extract: {pkgdata['path']}
Files count: {str(len(files.keys()))}
-------""")
        ion = None
        while not ion == 'y':
            ion = input('Install this package? (y/n): ')
            if ion == 'n':
                print('Aborting.')
                os._exit(1)
        print('Installing...')
        if os.path.exists(pkgdata['path']):
            pathchoice = None
            while not pathchoice == 'y':
                altnamepath = pkgdata['path']
                pathchoice = input(f'Seems that "{altnamepath}" already exists.\nContinue? (y/n): ')
                if pathchoice == 'n':
                    print('Aborting.')
                    os._exit(1)
        if not os.path.exists(pkgdata['path']):
            print('Making basic path dirs...')
            os.makedirs(pkgdata['path'])
        print('Constructing files...')
        for filename in files.keys():
            if '/' in filename:
                ca_d = filename.split('/')
                ofname = ca_d[-1]
                ca_d.pop(-1)
                crpath = pkgdata['path']
                for i in ca_d:
                    crpath = os.path.join(crpath, i)
                print('Creating additional path...')
                try:
                    os.makedirs(crpath)
                except FileExistsError:
                    pass
                crpath = os.path.join(crpath, ofname)
                print(f'Writing {ofname}...')
                with open(crpath, 'wb') as mwfile:
                    mwfile.write(base64.b64decode(files[filename].encode()))
            elif '\\' in filename:
                ca_d = filename.split('\\')
                ofname = ca_d[-1]
                ca_d.pop(-1)
                crpath = pkgdata['path']
                for i in ca_d:
                    crpath = os.path.join(crpath, i)
                print('Creating additional path...')
                try:
                    os.makedirs(crpath)
                except FileExistsError:
                    pass
                crpath = os.path.join(crpath, ofname)
                print(f'Writing {ofname}...')
                with open(crpath, 'wb') as mwfile:
                    mwfile.write(base64.b64decode(files[filename].encode()))
            else:
                crpath = os.path.join(pkgdata['path'], filename)
                print(f'Writing {filename}...')
                with open(crpath, 'wb') as mwfile:
                    mwfile.write(base64.b64decode(files[filename].encode()))
        print('Installed successfully.')
                
                

class Info:
    def show_help_message():
        helpmsg = """
ACP Packager
-b-y----o-h-m-i-u-
Usage:
    acp blank - Create an empty package project in this directory
    acp build - Build the package in the current directory
    acp install <package.acpe> - Install the package from the file
    acp all - Add all files in all folders in the "." directory to package.json
"""
        print(helpmsg)

if __name__ == "__main__":
    try:
        arg = sys.argv[1]
        if arg == 'blank':
            Project.create_blank_package()
        elif arg == 'build':
            Project.build_package()
        elif arg == 'install':
            pkgname = sys.argv[2]
            Installer.install_package(pkgname)
        elif 'all':
            Project.index_all_files()
        else:
            Info.show_help_message()
    except Exception as UnknownError:
        if isinstance(UnknownError, IndexError):
            Info.show_help_message()
        else:
            tback = traceback.format_exc()
            with open('./error.log', 'a') as ufile:
                ufile.write(f'{str(datetime.now())} - {tback}\n')
            print('[CRITICAL] - Unknown Error - saved in error.log')
