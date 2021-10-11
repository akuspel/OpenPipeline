import os, json

# path to OpenPipeline files
class OpenPipeline():

    filepath = os.path.expanduser("~").replace("\\", "/") + "/AppData/Local/OpenPipeline/"
    projects = filepath + "projects.json"
    
    porjectfile = "project.json"



# json load and save
def load_json(path):

    # load json file
    with open(path, "r") as file:

        # load json
        data = json.load(file)
    
    file.close()

    # return loaded variable
    return(data)

def save_json(path, data):

    # open json file
    with open(path, "w") as file:

        # save json data
        json.dump(data, file)
    
    file.close()


# projects dict load and save
def load_projects():

    # does path exist
    if not os.path.isdir(OpenPipeline.filepath):
        
        # create directory
        os.mkdir(OpenPipeline.filepath)
    
    # does save path exist
    if not os.path.isfile(OpenPipeline.projects):

        # create save json file
        with open(OpenPipeline.projects, "w") as file:
            json.dump({}, file)
        
        file.close()
    
    # read json data
    with open(OpenPipeline.projects, "r") as file:

        # load json
        projects = json.load(file)
    
    file.close()

    # return loaded variable
    return(projects)

def save_projects(projects):

    # yes
    with open(OpenPipeline.projects, "w") as file:

        # save json data
        json.dump(projects, file)
    
    file.close()