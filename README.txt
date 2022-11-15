GIT LEAKS

if running docker:
    > docker build -t <image_name> .
    > docker run -it -v <host_target_folder_absolute_path>:/output <image_name>

if running locally:
    > pip install -r requirements.txt
    > python git-leaks.py

The script will ask you wether to save the leaks as csv or json, and then save them in the /output folder.