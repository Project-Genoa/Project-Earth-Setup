import libprojectearthsetup
import shutil
import json
import os

# Thanks to
# https://www.c-sharpcorner.com/blogs/how-to-find-ip-address-in-python
import socket
hostname=socket.gethostname()
localIP=socket.gethostbyname(hostname)

libprojectearthsetup.printDisclaimer()
libprojectearthsetup.printHeader()
print("\n\n")

print("\n")
print("Select installation location")
libprojectearthsetup.pause()
installationLocation = libprojectearthsetup.selectFolder()

print("\n")
print("Please select artifact file")
libprojectearthsetup.pause()
artifactFile = libprojectearthsetup.selectFile()

print("Copying API Files...")
os.makedirs(os.path.join(installationLocation, 'api'), exist_ok=True)
shutil.unpack_archive(artifactFile, os.path.join(installationLocation, 'api'))
try:
    shutil.rmtree(os.path.join(installationLocation, 'api/data'))
except:
    pass

print("\n\n")
print("Setting up Cloudbust...")
os.makedirs(os.path.join(installationLocation, 'cloudburst/plugins'), exist_ok=True)
libprojectearthsetup.downloadFile("https://ci.rtm516.co.uk/job/ProjectEarth/job/Server/job/earth-inventory/10/artifact/target/Cloudburst.jar", os.path.join(installationLocation, 'cloudburst/Cloudburst.jar'))
shutil.copy("./cloudburst.yml", os.path.join(installationLocation, 'cloudburst/cloudburst.yml'))

print("Downloading plugins...")
libprojectearthsetup.downloadFile("https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbm15cEZpRjVlRkt5UkJYdW82ZDh4WHotbjVQZ3xBQ3Jtc0tuQmNNT2VRZjgydVQwMEpPQ3NCX25ORVdtaDNSUWsxbThfbWdWUjl3X2J5Z3lRQmNIWE1MMVNDLWxqR1RoS1VKZGluUG1sUllkanIwTDhxQkVQaUVrTWppNUlQM3RCckJ4bG1HUlBXeTJrcnB2RFRDWQ&q=https%3A%2F%2Fcdn.discordapp.com%2Fattachments%2F768873632767410196%2F965590044540825711%2FZGenoaAllocatorPlugin.jar&v=I1DMbp8V1Fs", os.path.join(installationLocation, 'cloudburst/plugins/ZGenoaAllocatorPlugin.jar'))
libprojectearthsetup.downloadFile("https://ci.rtm516.co.uk/job/ProjectEarth/job/GenoaPlugin/job/master/32/artifact/target/GenoaPlugin.jar", os.path.join(installationLocation, 'cloudburst/plugins/GenoaPlugin.jar'))

print("Configuring Plugins...")
os.makedirs(os.path.join(installationLocation, 'cloudburst/plugins/GenoaAllocatorPlugin'), exist_ok=True)
os.makedirs(os.path.join(installationLocation, 'cloudburst/plugins/GenoaPlugin'), exist_ok=True)

with open(os.path.join(installationLocation, 'cloudburst/plugins/GenoaAllocatorPlugin/key.txt'), 'w') as file:
    file.write("/g1xCS33QYGC+F2s016WXaQWT8ICnzJvdqcVltNtWljrkCyjd5Ut4tvy2d/IgNga0uniZxv/t0hELdZmvx+cdA==")

with open(os.path.join(installationLocation, 'cloudburst/plugins/GenoaAllocatorPlugin/ip.txt'), 'w') as file:
    file.write(localIP)


print("\n\n")
print("Configuring API...")

print("\n\n")
print("Downloading API data")
libprojectearthsetup.downloadFile("https://github.com/jackcaver/ApiData/archive/refs/heads/master.zip", "./apiData.zip")
shutil.unpack_archive('./apiData.zip', os.path.join(installationLocation, 'api/'))
shutil.move(os.path.join(installationLocation, 'api/ApiData-master'), os.path.join(installationLocation, 'api/data'))

print("\n\n")
print("Downloading resource pack")
os.makedirs(os.path.join(installationLocation, 'api/data/resourcepacks'), exist_ok=True)
libprojectearthsetup.downloadFile("https://web.archive.org/web/20210624200250if_/https://cdn.mceserv.net/availableresourcepack/resourcepacks/dba38e59-091a-4826-b76a-a08d7de5a9e2-1301b0c257a311678123b9e7325d0d6c61db3c35", os.path.join(installationLocation, 'api/data/resourcepacks/vanilla.zip'))
#shutil.move(os.path.join(installationLocation, 'api/data/resourcepacks/dba38e59-091a-4826-b76a-a08d7de5a9e2-1301b0c257a311678123b9e7325d0d6c61db3c35'), os.path.join(installationLocation, 'api/data/resourcepacks/vanilla.zip'))

configData = None
with open(os.path.join(installationLocation, 'api/data/config/apiconfig.json'), 'r') as jsonConfig:
    configData = json.loads(jsonConfig.read())
    configData["baseServerIP"] = 'http://' + str(localIP)
    configData["multiplayerAuthKeys"] = {}
    configData["multiplayerAuthKeys"][localIP] = "/g1xCS33QYGC+F2s016WXaQWT8ICnzJvdqcVltNtWljrkCyjd5Ut4tvy2d/IgNga0uniZxv/t0hELdZmvx+cdA=="

with open(os.path.join(installationLocation, 'api/data/config/apiconfig.json'), 'w') as jsonConfig:
    jsonConfig.write(json.dumps(configData, indent=4))


print("\n\n")
print("Creating .bat files")
with open(os.path.join(installationLocation, 'api/start.bat'), 'w') as file:
    file.write('.\\ProjectEarthServerAPI.exe\npause')
with open(os.path.join(installationLocation, 'cloudburst/start.bat'), 'w') as file:
    file.write('"C:\\Program Files (x86)\\Java\\jdk1.8.0_191\\bin\\java.exe" -jar .\\Cloudburst.jar\npause')


print("\n\n")
print("Installation complete!")
print("\n\n")
print("YOU NEED JAVA 8 AND .NET5.0 INSTALLED TO RUN THE API/CLOUDBURST")
print("Please run the start.bat file in the api folder and then the start.bat file in the cloudburst folder")
print("!! IT HAS TO BE IN THAT ORDER !!")
print("")
print("Patch url: [" + "http://" + str(localIP) + "]")