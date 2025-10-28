# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_submodules
block_cipher = None

hiddenimports = collect_submodules('controllers') + collect_submodules('utils') + ['tkcalendar','_cffi_backend','jinja2','PIL','utils.autocomplete', 'utils.modal_history', 'controllers.user_controller']

def collect_folder(folder, dest):
    datas = []
    if not os.path.isdir(folder):
        return datas
    for root, _, files in os.walk(folder):
        for f in files:
            src = os.path.join(root, f)
            rel = os.path.relpath(root, folder)
            dest_dir = os.path.join(dest, rel) if rel != '.' else dest
            datas.append((src, dest_dir))
    return datas

datas = []
datas += collect_folder('images', 'images')
datas += collect_folder('views', 'views')
if os.path.exists('empleados.db'):
    datas.append(('empleados.db', '.'))

# incluir Tcl/Tk data si existe (evita error _internal/_tcl_data)
for p in (sys.prefix, getattr(sys,'base_prefix',None), getattr(sys,'real_prefix',None)):
    if p:
        tcl = os.path.join(p, 'tcl')
        if os.path.isdir(tcl):
            for root, _, files in os.walk(tcl):
                for f in files:
                    src = os.path.join(root, f)
                    rel = os.path.relpath(root, tcl)
                    dest = os.path.join('_internal','_tcl_data', rel) if rel != '.' else os.path.join('_internal','_tcl_data')
                    datas.append((src, dest))

a = Analysis([os.path.join(r'C:\Users\SOLMART TM\Documents\proyectos python\app_empleados','main.py')],
             pathex=[r'C:\Users\SOLMART TM\Documents\proyectos python\app_empleados'],
             binaries=[],
             datas=datas,
             hiddenimports=hiddenimports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='main', debug=False, bootloader_ignore_signals=False, strip=False, upx=True, console=True, icon=['icono_sge.ico'] if os.path.exists('icono_sge.ico') else None)
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name='main')