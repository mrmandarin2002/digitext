import PyInstaller.__main__
import os, glob
from sys import platform
from shutil import copy


current_directory = os.getcwd()
split_char = '\\'
plat = "Windows"
option = '--console'
file_type = ".exe"
if(platform == "darwin"):
    option = '--windowed'
    split_char = '/'
    plat = "MacOS"
    file_type = ".app"
out_directory = current_directory.split(split_char)
out_directory.remove('CLIENT')
out_directory.append("Releases" + split_char + plat)
out_directory = split_char.join(out_directory)

print("CURRENT DIRECTORY: " + current_directory)
print("OUTPUT DIRECTORY: " + out_directory)

for file in glob.glob(out_directory + split_char + '*'):
    os.remove(file)


PyInstaller.__main__.run([
    option,
    '--name=%s' % "DigiText",
    '--onefile',
    '--icon=%s' % 'sphs_icon.ico',
    "main.py",
])

copy(current_directory + split_char + "Delete_Textbook_Warning.mp3", out_directory )
copy(current_directory + split_char +"Textbook_Scan_in_Sound.mp3", out_directory )
copy(current_directory + split_char +"settings.json", out_directory)
copy(current_directory + split_char +"dist"+ split_char +"DigiText" + file_type, out_directory)



