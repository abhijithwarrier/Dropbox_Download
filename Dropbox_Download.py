# Programmer - python_scripts (Abhijith Warrier)

# A PYTHON SCRIPT TO DOWNLOAD FILES FROM DROPBOX USING dropbox MODULE

# dropbox Module is Python SDK for integrating with Dropbox API v2. Compatible with
# Python 2.7 & 3.4+
# The module can be installed using the command - pip install dropbox

# To use Dropbox API, a new app has to be registered in Dropbox App Console. Follow the below steps
# 1 - Login to the following link - https://www.dropbox.com/developers/apps
# 2 - After signing in click on Create App.
# 3 - In the next page make the following selections
#   1. Choose an API
#       Select Dropbox API
#   2. Choose the type of access you need
#       Select Full Dropbox – Access to all files and folders in a user's Dropbox.
#   3. Name your app
#       Give a name to your APP
# 4 - Click on Create App
# 5 - In the next page, click on Generate, to generate ACCESS TOKEN

# Importing the necessary packages
import os
import dropbox

# In order to make calls to the API, an instance of the Dropbox object has to be created.
# Accessing the Dropbox account with the access token
client = dropbox.Dropbox('YOUR ACCESS TOKEN')
# Setting the download path in the your system, into which the files are to be downloaded
# SET YOUR DOWNLOAD PATH
download_path = 'YOUR DOWNLOAD PATH IN YOUR SYSTEM'
# Declaring an empty variable named selection_name
selection_name = ''

# Defining Dropbox_Folder() with f_f_list (FILES,FOLDER LIST) and s_number(USER-SELECTION_NO) as
# arguments to expand the folder items
def Dropbox_Folder(f_f_list, s_number):
    # Calling the selection_name variable as global
    global selection_name
    # Concating the f_f_list entries name from user selection number and / with the selection_name
    selection_name += f_f_list.entries[s_number-1].name + '/'
    # Fetching the contents of the folder, using the files_list_folder() which takes the path as
    # the argument set to '/' + selection_name
    folder_contents = client.files_list_folder(path='/' + selection_name)
    # Displaying the files present in the folder
    print("\nFILES AND PRESENT IN " + f_f_list.entries[s_number - 1].name + " FOLDER")
    for f in range(len(folder_contents.entries)):
        # Folder contents are displayed from folder_contents
        print(str(f + 1) + " - " + folder_contents.entries[f].name)
    # Prompting the user to enter the selection and storing it in the folder_content_number
    folder_content_number = int(input("\nENTER THE FOLDER OR FILE NUMBER : "))
    # Concating the selection_name with the folder name of the user_input number and setting it to
    # new_selection_type
    new_selection_name = selection_name + folder_contents.entries[folder_content_number - 1].name
    # Getting the type of new_selection_name (folder or file) using files_get_metadata() which takes
    # the path as the argument set to '/'+new_selection_name and storing it in folder_content_type
    folder_content_type = client.files_get_metadata(path='/'+new_selection_name)
    # Checking if the folder_content_type is Folder using the isinstance() which takes the
    # folder_content_type and dropbox.files.FolderMetadata as the arguments
    if isinstance(folder_content_type, dropbox.files.FolderMetadata):
        # If the selection is a folder then call the Dropbox_Folder()
        Dropbox_Folder(folder_contents, folder_content_number)
    # Checking if the folder_content_type is File using the isinstance() which takes the
    # folder_content_type and dropbox.files.FileMetadata as the arguments
    elif isinstance(folder_content_type, dropbox.files.FileMetadata):
        # If the selection is a folder then call the Dropbox_File()
        Dropbox_File(folder_contents, folder_content_number)

# Defining Dropbox_File() with f_f_list and s_number as the arguments
def Dropbox_File(f_f_list, s_number):
    # Calling the selection_name variable as global
    global selection_name
    # Concating the f_f_list entries name from user selection_number with the selection_name
    selection_name += f_f_list.entries[s_number - 1].name
    # Storing only the file name from the path(selection_name) using the os.path.basename
    save_file_name = os.path.basename(selection_name)
    # Downloading the file
    print("\nDOWNLOADING " + save_file_name)
    # Checking if the download_path folder already exists
    if os.path.exists(download_path):
        # Downloading the file using files_download() which takes path set to the selection_name
        # as the argument
        metadata, file = client.files_download(path='/' + selection_name)
        # Opening the new file in the write-binary mode with dwld_file as the object
        with open(download_path + "/" + save_file_name, 'wb') as dwld_file:
            # Write contents of selected file (file.content) to the dwld_file using the write()
            dwld_file.write(file.content)
            # Close the dwld_file
            dwld_file.close()
    # If the download folder does not already exists, then make the folder
    else:
        os.mkdir(download_path)
        # Downloading the file using files_download() which takes path as the argument
        metadata, file = client.files_download(path='/' + selection_name)
        # Opening the new file in the write-binary mode with dwld_file as the object
        with open(download_path + "/" + os.path.basename(selection_name), 'wb') as dwld_file:
            # Write contents of selected file (file.content) to the dwld_file using the write()
            dwld_file.write(file.content)
            # Close the dwld_file
            dwld_file.close()
    print("\n" + os.path.basename(selection_name) + " SAVED SUCCESSFULLY TO " + os.path.basename(download_path))

# Defining the Dropbox_Download()
def Dropbox_Download():
    # Fetching the files and folders present in Dropbox (root folder) using files_list_folder()
    # Setting the files_list_folder() to empty string ('') indicates root folder
    files_folders_list = client.files_list_folder(path='')
    # Displaying the files and folder present in the dropbox
    print("\nFILES AND FOLDERS PRESENT IN THE DROPBOX")
    for f in range(len(files_folders_list.entries)):
        print(str(f+1)+" - "+ files_folders_list.entries[f].name)
    # Prompting the user to enter the selection number and storing it in root_selection_number
    root_selection_number = int(input("\nENTER THE FOLDER OR FILE NUMBER : "))
    # Getting the name of the user's selection and storing it in root_selection_name
    root_selection_name = files_folders_list.entries[root_selection_number-1].name
    # Getting the type of root_selection_name (folder or file) using files_get_metadata() with
    # the path argument set to '/'+root_selection_name and storing it in selection_type
    selection_type = client.files_get_metadata(path='/'+root_selection_name)
    # Checking if the selection_type is Folder using the isinstance() which takes the
    # selection_type and dropbox.files.FolderMetadata as the arguments
    if isinstance(selection_type, dropbox.files.FolderMetadata):
        # If the selection is a folder then call the Dropbox_Folder()
        Dropbox_Folder(files_folders_list, root_selection_number)
    # Checking if the selection_type is File using the isinstance() which takes the
    # selection_type and dropbox.files.FileMetadata as the arguments
    elif isinstance(selection_type, dropbox.files.FileMetadata):
        # If the selection is a folder then call the Dropbox_File()
        Dropbox_File(files_folders_list, root_selection_number)

# Driver Code
if __name__ == '__main__':
    # Calling the Dropbox_Download()
    Dropbox_Download()
