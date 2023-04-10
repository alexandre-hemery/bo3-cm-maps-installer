# Black Ops III - Custom Zombies Maps Installer
Welcome everyone! I have created a small tool entirely coded in Python that allows players who do not have Steam to automatically download and install custom maps that are available on the Steam Workshop!

You can download the latest version here : [Version 1.1](https://github.com/alexandre-hemery/bo3-cm-maps-installer/releases/tag/release-1.1)

This small tool does not work alone, in order to run it properly you will first need to download Python which you can get at this address: [Python](https://www.python.org/downloads/)
And you will also need SteamCMD which you can get at this address (direct download link): [SteamCMD](https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip)

**Note that in order for the tool to function properly, you will need to place it in the same folder as the SteamCMD.exe executable!**

This tool was initially designed to automate the installation of maps for the Zombies mode of the game, it may work with maps for the Multiplayer mode but this has not yet been tested, so please try it out and let me know if it works!

Installing custom maps without using the Steam Workshop integrated into Steam requires manually downloading the Workshop item that interests us, finding a workshop.json file that contains the name of the map so that it is recognized by the game, and then copying all the files into the game directory using this map name. This tool aims to automate this entire process. All you have to do is enter the installation directory of your game, write the ID of the Workshop item you want to install, and click the "Download and Install" button. I have also included a system that allows you to remember the directory of your game so that you do not have to do it every time you start the tool. This system works by creating a text file named "game_directory" in the folder where the script is located.

On the tool, you can find a button to take you directly to the Black Ops III Workshop page in the Zombies category, a button to select the directory of your game, a button to start the download and installation, and of course a button to quit the software (although you could just click the "X" to close it).

![Screenshot of the tool, showing the different buttons.](https://i.imgur.com/VmPqSCM.png)

Feel free to give me your suggestions to potentially improve the tool! And also let me know of any bugs you encounter! Note: if after clicking the "Download and Install" button, the graphical interface stops responding, it is because the script has launched the installation from the Steam Workshop servers. You can follow what is happening from the command interface that launches at the same time as the graphical interface. Once the installation is complete, you will receive a Windows pop-up to notify you of the end of the installation and to ask if you want to access the folder that was created so that you can check if necessary that the script was executed correctly. Once the installation is complete, the graphical interface of the tool will start responding again.
