from tqdm import tqdm
import requests
import os

# GUI Library Import
try:
    import wx
    guiProvider = 'wx'
except:
    try:
        from tkinter import filedialog
        from tkinter import Tk
        guiProvider = 'tk'
    except:
        guiProvider = 'cli'


# Define globals
version = 'v1.0.0'
debug = False

def printHeader():
    print("==================================================")
    print("=           Project Earth Setup Utility          =")
    print("========================================= " + version + " =")
    print("\n\n")

def printDisclaimer():
    disclaimer = [
        "Bluebotlabz nor Project Genoa are affiliated with Mojang, Microsoft, Minecraft or Minecraft: Earth",
        "Bluebotlabz nor Project Genoa are affiliated with Project Earth",
        "Project Earth is not affiliated with Mojang, Microsoft, Minecraft or Minecraft: Earth",
        "Bluebotlabz, Project Genoa, nor Project Earth take any responsibility for any thing which may occur as a result of using this software",
        "",
        "Microsoft/Mojang reserve the right to terminate the usage of Project Earth/Minecraft Earth at any time",
        "",
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,",
        "INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.",
        "IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,",
        "WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE",
        "OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.",
    ]
    printCenteredText(disclaimer)
    print("")
    print("By using this software, you agree to the above disclaimer")
    input("Press enter to continue...")
    print("\n\n")

def pause():
    input("Press enter to continue...")

def printCenteredText(textList, lineWidth=150, horizontalChar='=', verticalChar='='):
    print(horizontalChar*lineWidth)
    for line in textList:
        renderedLine = line

        padRight = False
        while len(renderedLine) <  lineWidth-4:
            if (padRight):
                renderedLine += ' '
            else:
                renderedLine = ' ' + renderedLine
            padRight = not padRight

        renderedLine = verticalChar + ' ' + renderedLine + ' ' + verticalChar
        print(renderedLine)
    print(horizontalChar*lineWidth)

def selectFolder():
    # Selects a folder using the available native OS GUI and outputs its path
    if (guiProvider == 'wx'):
        print("Please select a folder to install to")
        wxRoot = wx.App()
        selectionDialog = wx.DirDialog(None, "Please select an installation location", style= wx.DD_DEFAULT_STYLE | wx.STAY_ON_TOP )
        if (selectionDialog.ShowModal() == wx.ID_OK ):
            del wxRoot
            print("Installing to [" + selectionDialog.GetPath() + ']\n\n')
            return selectionDialog.GetPath()
        else:
            del wxRoot
            print("Error selecting folder: User canceled the operation")
            print("\n\n")
            exit(1)
    elif (guiProvider == 'tk'):
        print("Please select a folder to install to")
        tkRoot = Tk()
        tkRoot.focus()
        tkRoot.withdraw()
        tkRoot.attributes("-topmost", 1)
        selectedFolder = filedialog.askdirectory()
        if (selectedFolder):
            print("Installing to [" + selectedFolder + ']\n\n')
            return selectedFolder
        else:
            print("Error selecting folder: User canceled the operation")
            print("\n\n")
            exit()
    else:
        selectedFolder = None
        while not selectedFolder:
            selectedFolder = input("Please enter the destination folder for the installation: ")
            if (os.path.isdir(selectedFolder)):
                print("Installing to [" + os.path.join(selectedFolder) + ']\n\n')
                return os.path.join(selectedFolder)
            else:
                selectedFolder = None
                input("The folder you have selected is invalid, please try again...")
                print("\n\n")

def selectFile():
    # Selects a folder using the available native OS GUI and outputs its path
    if (guiProvider == 'wx'):
        print("Please select a file")
        wxRoot = wx.App()
        selectionDialog = wx.FileDialog(None, "Please select a file", style= wx.FD_DEFAULT_STYLE | wx.STAY_ON_TOP )
        if (selectionDialog.ShowModal() == wx.ID_OK ):
            del wxRoot
            print("Using file [" + selectionDialog.GetPath() + ']\n\n')
            return selectionDialog.GetPath()
        else:
            del wxRoot
            print("Error selecting file: User canceled the operation")
            print("\n\n")
            exit(1)
    elif (guiProvider == 'tk'):
        print("Please select a file")
        tkRoot = Tk()
        tkRoot.focus()
        tkRoot.withdraw()
        tkRoot.attributes("-topmost", 1)
        selectedFolder = filedialog.askopenfilename()
        if (selectedFolder):
            print("Using file [" + selectedFolder + ']\n\n')
            return selectedFolder
        else:
            print("Error selecting file: User canceled the operation")
            print("\n\n")
            exit()
    else:
        selectedFolder = None
        while not selectedFolder:
            selectedFolder = input("Please enter the artifact file path: ")
            if (os.path.isdir(selectedFolder)):
                print("Using file [" + os.path.join(selectedFolder) + ']\n\n')
                return os.path.join(selectedFolder)
            else:
                selectedFolder = None
                input("The file you have selected is invalid, please try again...")
                print("\n\n")

def listSelect(selectionList, numberSeperator = '.', selectionPrompt='Please choose which version to install by typing the number on the list: ', confirmationPrompt='You have selected version [SELECTIONTEXT], are you sure you want to download it? [Y/n]', confirm=True):
    # Displays a list of options from the provided list
    # Asks user to make a selection from number and returns the index in the list chosen by the user
    # List must contain tupple in format:
    # ( "DisplayText", "DescriptionText" )
    # Tupple can have additional elements, but they are ignored by the function
    # Note: DescriptionText == '--' results in HEADER being printed, not selection

    userSelection = None
    while not userSelection:
        displayIndex = 0 # Index displayed to user
        realIndex = 0 # The actual index of the selection in the list
        indexMap = {} # Maps display indexes to real indexes

        for selection in selectionList:
            if (selection[1] != '--'):

                # Pad number so they are all indented the same (noticable with lists of 10 or more)
                renderedNumber = str(displayIndex)
                while len(renderedNumber) < len(str(len(selectionList))):
                    renderedNumber = ' ' + renderedNumber

                print(renderedNumber + numberSeperator + ' ' + selection[0] + '\t' + selection[1])
                indexMap[displayIndex] = realIndex
                displayIndex += 1
            else:
                renderedLine = '='
                while len(renderedLine) < len(str(len(selectionList))):
                    renderedLine = ' ' + renderedLine

                print(renderedLine + "= " + selection[0] + " =" + renderedLine)
                
            realIndex += 1

        try:
            userSelection = int(input(selectionPrompt))
        except ValueError:
            userSelection = None
            input("You have made an invalid selection, please try again...")
            print("\n\n")
            continue
        
        if (userSelection >= 0 and userSelection < displayIndex):
            if (confirm):
                if (input(confirmationPrompt.replace('[SELECTIONTEXT]', selectionList[indexMap[userSelection]][0])).lower() != 'n'):
                    print("\n\n")
                    return indexMap[userSelection]
                else:
                    userSelection = None
                    print("\n\n")
        else:
            userSelection = None
            input("You have made an invalid selection, please try again...")
            print("\n\n")

def downloadFile(fileURL, saveLocation, descriptionSuffix=''):
    # Downloads a file given its URL and download location
    # Displays a terminal progress bar via TQDM

    # Create the folder if needed
    try:
        os.makedirs(os.path.dirname(saveLocation), exist_ok=True)
    except Exception as error:
        print(error)
        print("Error creating folder... Please try again and select another download location")
        exit(1)

    # Get the file
    downloadedFile = requests.get(fileURL, stream=True)

    try:
        fileSize = int(downloadedFile.headers["content-length"])
    except:
        fileSize = 0

    # Actually download the file
    with open(saveLocation, 'wb') as file:
        with tqdm(desc='Downloading [' + os.path.basename(saveLocation) + ']' + descriptionSuffix, total=fileSize, unit_scale=True, unit='B', unit_divisor=1000, leave=False, bar_format='{l_bar}{bar}| {n_fmt}B/{total_fmt}B [{elapsed}<{remaining}, {rate_fmt}{postfix}]') as progressBar: # TQDM for progress bar
            for chunk in downloadedFile.iter_content(chunk_size=1024): # Download file
                file.write(chunk) # Write filedata
                progressBar.update(len(chunk)) # Update progressbar with amount down