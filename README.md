# GIT LEAKS

## Project Description  

Extracting possible leaks from a GitHub repository, finding keywords and emails with regex in raw commits.  
The script will ask you whether to save the leaks as csv or json, and then save them in the /out folder. If running docker, you need to mount a volume to the /out folder as shown below in order to see the output files.

---

## Running docker:
    > docker build -t <image_name> .
    > docker run -it -v <host_out_folder_absolute_path>:/output --name <container-name> <image_name>
    > docker start -i <container-name> (if container is already created)

## Running python:
    > pip install -r requirements.txt
    > python git_leaks.py