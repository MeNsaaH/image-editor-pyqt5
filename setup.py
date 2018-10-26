import sys
from cx_Freeze import setup, Executable 

build_exe_options = {'packages': ['os']}

base = None 
if sys.platform == 'win32':
	base = 'Win32GUI'

target = Executable(
	script = 'ImageEditor.py',
	base = base,
	icon = 'icon.ico',
	shortcutName = 'Image Editor',
	#shortcutDir = "C:\Users\Bethel Madu\Desktop\\", 
	copyright = 'Manasseh Mmadu',
	trademarks = 'Copy Right - mmadu Manasseh'
	)

setup(
	name = 'Image Editor', 
	version = '1.0.0',
	description = 'My First Executable GUI Photo Editor',
	author = 'Manasseh Corps',
	#publisher = 'Mensaah Corps',
	options = {'build_exe': build_exe_options},
	executables = [target]
	)