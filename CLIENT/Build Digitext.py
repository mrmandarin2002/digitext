import PyInstaller.__main__
import os, glob
from shutil import copyfile

current_directory = os.getcwd()
windows_directory = current_directory.split('\\')
windows_directory.remove('CLIENT')
windows_directory.append("Releases\\Windows")
windows_directory = '\\'.join(windows_directory)
mac_directory = current_directory.split('\\')
mac_directory.remove('CLIENT')
mac_directory.append("Releases\\MacOS")
mac_directory = '\\'.join(mac_directory)

print(windows_directory)
print(mac_directory)

for file in glob.glob(windows_directory + '\\*'):
    os.remove(file)

for file in glob.glob(mac_directory + '\\*'):
    os.remove(file)

PyInstaller.__main__.run([
    '--name=%s' % "DigiText",
    '--onefile',
    '--icon=%s' % 'sphs_icon.ico',
    "main.py",
])

copyfile(current_directory + "\\Delete_Textbook_Warning.mp3", windows_directory + "\\Delete_Textbook_Warning.mp3")
copyfile(current_directory + "\\Textbook_Scan_in_Sound.mp3", windows_directory + "\\Textbook_Scan_in_Sound.mp3")
copyfile(current_directory + "\\settings.json", windows_directory + "\\settings.json")
copyfile(current_directory + "\\dist\\DigiText.exe", windows_directory + "\\DigiText.exe")



