#!/usr/bin/python3

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# Les King (Lesking72) wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.
# ----------------------------------------------------------------------------

# There is no error handling, so this won't fail gracefully.
# It accesses version_history.json so if you don't run it in the server
# folder or haven't run the server before to get version_history.json it won't work.

# The author accepts no liability for anything at all, ever. God help you.

import json
import urllib.request

#This is the version of Minecraft we're targeting
target_mc = "1.16.3"

request = urllib.request.urlopen("https://papermc.io/api/v1/paper/" + target_mc) #Request the available Paper builds for the targeted MC version
body = request.read() #Read the response, store it in body
api_resp = json.loads(body) #The response is in JSON, so we can parse it into a Python dictionary

release_id = api_resp["builds"]["latest"] #The API tells us the latest build, under the builds>latest subdictionary.

print ("Latest Build for Minecraft " + target_mc + ": Paper-"+ release_id) #tell the user the latest build

vh_file = open("version_history.json","r") #This is Paper's version history file, we can use it to find the current version
#This isn't foolproof. The file is updated by the server, so if the server hasn't been run yet, the updater will still believe there is an update available.

vh_content =  vh_file.read() #Read version_history.json

vh_dict = json.loads(vh_content) #Parse version_history.json into a dictionary

current_version = vh_dict["currentVersion"] #Makes the next two lines less of a clusterfuck

installed_build = current_version[10:current_version.find("MC: ") - 2] #Get a substring of the Paper build ID
#There's no set length for build IDs, so we get what's between "git-Paper-" (10) and " (MC", which is 2 places before "MC: ".

installed_mc = current_version[current_version.find("MC: ") + 4:len(current_version) - 1] #Specifically separate out the MC version string
#MC Version strings also have no set length, so we get what's between "MC: " and the ")" at the end of the string.

print ("Installed Version: Paper-" + installed_build + " for Minecraft " + installed_mc) #Tell the user their currently installed version

if target_mc > installed_mc: #Didn't realize until after running this that those are strings. apparently it works with strings.
	print("You appear to be upgrading to a newer Minecraft version! Make sure you have backups!")
elif target_mc < installed_mc:
	print("The targeted MC version is less than the currently installed version! This tool does not support downgrading!")
	exit()
elif installed_build == release_id:
	print("You are already using the latest version.")
	exit()
elif installed_build > release_id: #this is typically overruled by the first statement, but I'm keeping it just in case
	print("The installed version appears to be newer than the available version.")
	print("If you're updating between Minecraft versions, this is normal.")

print ("Make sure the server is stopped, because I won't!")
if input("Download Paper-" + release_id + " for Minecraft " + target_mc + "? (y/n) ") == "y":
	pass
	#it's done this way to always exit unless the user explicitly enters "y"
	#probably could have done != "y"... too late.
else:
	print("Operation canceled by user")
	exit()

dl_link = "https://papermc.io/api/v1/paper/" + target_mc + "/" + release_id + "/download" #This is our download link

print ("Downloading Paper-" + release_id + " from " + dl_link) #Tell the user what we're downloading

urllib.request.urlretrieve(dl_link, "paperclip.jar") #Download it, save it as paperclip.jar

print ("Saved paper-" + release_id +  ".jar as paperclip.jar") #Tell the user where we saved it

