import os, json

# path to OpenPipeline files
class OpenPipeline():

    filepath = os.path.expanduser("~").replace("\\", "/") + "/AppData/Local/OpenPipeline/"
    projects = filepath + "projects.json"


# just backend
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