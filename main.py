import eel, os, subprocess
from json_backend import *
from project_backend import *

# variables

projects = { # [directory, description, team[[name, email] ] ]
    "Project_01" : ["C:/Users/User/Documents/Projects/Project_01/", "This is a project", [["John Doe", "john.doe@email.com", "director"], ["Mary Smith", "mary.smith@email.com", "artist"]] ],
    "Project_02" : ["D:/Documents/Projects/Importan/t", "What am I supposed to say here??", [["Sir McEmail", "email@email.com", "coder"]] ],
    "Another Project" : ["D:/Documents/Games/Card Game", "A card based puzzle game, where you place cards into tiles following a specific set of rules. Beat your way to the evil prince, and take the throne to yourself!", [["John Doe", "john.doe@email.com", "producer"], ["Mary Smith", "mary.smith@email.com", "modeler"], ["Jeremy Smithers", "jeremy@email.com", "coder"]] ]
}

class Current():

    # currently open stuff
    open_project = ""
    open_member = ""

    open_projectfile = {}

    open_scene = ""

# constants

FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')

# functions

# management tools

@eel.expose
def set_open_project(project):

    # set currently open project
    Current.open_project = project

@eel.expose
def set_open_member(member):

    # set currently open member
    Current.open_member = member.split(" | ")

@eel.expose
def set_open_scene(scene):

    # set currently open member
    Current.open_scene = scene

@eel.expose
def create_project_files():

    project_file = projects[Current.open_project][0]
    # add / to end
    if project_file[-1] != "/": project_file += "/"
    project_file += "project.json"

    # create project
    save_json(project_file, ProjectFiles.project_template)

    # load thing
    load_project_overview()

@eel.expose
def create_project(name, directory, description):

    if len(name) > 0 and name not in projects:

        # create empty project entry
        project = ["", "", []]

        # assign values
        project[0] = directory
        project[1] = description

        # add project to projects dictionary
        projects[name] = project

        # set project as current project
        Current.open_project = name

        print("Project Created Sucessfully")

        # open project overview
        eel.link("project_overview.html")
        
        # save projects to json
        save_projects(projects)

@eel.expose
def edit_project(name, directory, description):
    
    if len(name) > 0:

        # open old project entry
        project = projects[Current.open_project]

        # assign values
        project[0] = directory
        project[1] = description

        # add project to projects dictionary
        projects[name] = project

        # if project name changed
        if Current.open_project != name:

            # remove old entry
            projects.pop(Current.open_project)

            # set project as current project
            Current.open_project = name

        print("Project Edited Sucessfully")

        # open project overview
        eel.link("project_overview.html")

        # save projects to json
        save_projects(projects)

@eel.expose
def remove_project():

    # remove currently active project
    projects.pop(Current.open_project)

    # refresh the UI
    load_side_bar()

    # reset variables
    Current.open_project = ""
    
    # save projects to json
    save_projects(projects)


# scenes
@eel.expose
def add_scene(scene, root):

    # load current project file to project variable
    project = Current.open_projectfile

    # does scene already exist
    if scene not in project["scenes"] and len(scene) > 0:

        project_file = projects[Current.open_project][0]
        # add / to end
        if project_file[-1] != "/": project_file += "/"
        project_file += "project.json"

        # assign new scene key to scenes with root
        project["scenes"][scene] = {"root" : root}

        # set current projectfile
        Current.open_projectfile = project

        # save project file
        save_json(project_file, project)

@eel.expose
def remove_scene(scene):

    # load current project file to project variable
    project = Current.open_projectfile

    # project file path
    project_file = projects[Current.open_project][0]
    # add / to end
    if project_file[-1] != "/": project_file += "/"
    project_file += "project.json"

    # assign new scene key to scenes with root
    project["scenes"].pop(scene)

    # set current projectfile
    Current.open_projectfile = project

    # save project file
    save_json(project_file, project)



# members
@eel.expose
def add_member(name, email, role):

    if len(name) > 0:

        # create empty project entry
        member = ["", "", ""]

        # assign values
        member[0] = name
        member[1] = email
        member[2] = role

        # add member to current project
        projects[Current.open_project][2].append(member)

        print("Member Created Sucessfully")

        # open project overview
        eel.link("project_overview.html")

        # save projects to json
        save_projects(projects)

@eel.expose
def remove_member():

    # remove currently active member
    projects[Current.open_project][2].remove(Current.open_member)

    # reset variables
    Current.open_member = ""
    
    # save projects to json
    save_projects(projects)


# usability
@eel.expose
def explore(path):
    # explorer would choke on forward slashes
    path = os.path.normpath(path)

    # make dir or open dir
    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    else:
        os.mkdir(path)

# loading ui
@eel.expose
def load_side_bar():

    # generate inner html for side bar
    innerHTML = "<label id='side_bar_label' onclick='close_side_bar()'>v Projects</label>"
    innerHTML += "<img src='img/plus.svg' id='side_icon' onclick='link(urls.project_creation)'>"

    # create div container for projects
    innerHTML += "<div id='side_container'>"
    # get all existing projects
    for project in projects:

        # create entry for project name
        innerHTML += f"<div class='side_bar_item' onclick='link(urls.project_overview), eel.set_open_project(this.innerText)'>{project}</div>"
    
    # close project container
    innerHTML += "</div>"

    # return innerHTML
    eel.side_bar(innerHTML)

@eel.expose
def load_project_overview():

    # load project attributes into project var
    project = projects[Current.open_project]

    # set attributes
    name = Current.open_project

    directory = project[0]
    description = project[1]


    # team container innerHTML
    team = "<h4 style='padding:6px;''>Team:</h4>"
    team += "<img src='img/plus.svg' class='container_icon' onclick='link(urls.member_creation)' style='position:relative; float:right; top:-43px;'>"

    # add members to team
    for member in project[2]:
        team += f"<div class='team_member' title='{member[0]} | {member[1]} | {member[2]}' onclick='link(urls.member_editor), eel.set_open_member(this.title)'>"
        team += f"<img src='img/person.svg' class='container_button_icon'>{member[0]} ({member[1]}) ({member[2]})</div>"
    

    # check if directory exists

    # path variable to return to html (1 = path exists, 0 = path doesn't exist but is possible, -1 path error)
    path = directory
    # check if dir length is greater than 0 and it links to a drive
    if len(path) > 0 and path[1:3] == ":/":
        # add / to end of path
        if path[-1] != "/": path += "/"
    else:
        directory = "no path"
        path = -1

    # does path exist
    if path != -1:
        if os.path.exists(path):
            path = 1
        else:
            path = 0


    # project file variable to return to html, if project file exists
    project_file = directory
    project_exists = False
    # if path exists
    if path == 1:
        # add / to end of path
        if project_file[-1] != "/": project_file += "/"
        # add project.json to end
        project_file += "project.json"

        # does file exist
        project_exists = os.path.isfile(project_file)
    
    # load projectfile
    if project_exists == True: Current.open_projectfile = load_json(project_file)


    # update ui
    eel.project_overview(name, directory, description, team, path, project_exists)
    
    print("Project Overview loaded")


@eel.expose
def load_project_editor():

    # load project attributes into project var
    project = projects[Current.open_project]

    # set attributes
    name = Current.open_project

    directory = project[0]
    description = project[1]

    # update ui
    eel.project_editor(name, directory, description)
    
    print("Project Editor loaded")

@eel.expose
def load_member_editor():

    # get current member
    member = Current.open_member

    # set attributes
    name = member[0]
    email = member[1]
    role = member[2]

    # update ui
    eel.member_editor(name, email, role)
    
    print("Member Editor loaded")


# scene editor
@eel.expose
def load_scene_overview():

    project = Current.open_projectfile

    # set attributes
    directory = project["scene_directory"]

    # team container innerHTML
    scenes = "<h4 style='padding:6px;'>Scenes:</h4>"
    # plus button
    scenes += "<img src='img/plus.svg' class='container_icon' onclick='open_scene_creator()' title='Add New Scene' style='position:relative; float:right; top:-46px;''>"

    # add members to team
    for scene in project["scenes"]:

        # root path
        root = project['scenes'][scene]['root']
        # add scene item
        scenes += f"<div class='container_item' title='{scene}' onclick='link(urls.scene_editor), eel.set_open_scene(this.title)'>"
        scenes += f"<img src='img/scene.svg' class='container_button_icon'>Scene: ({scene}) -- Dir: ({root}/{scene})</div>"
    

    # check if directory exists

    # path variable to return to html
    path = projects[Current.open_project][0]

    # make directory the full path
    directory = os.path.join(path, directory).replace("\\", "/")

    # does path exist
    if os.path.exists(directory):
        path = 1
    else:
        path = 0

    # update ui
    eel.scene_overview(directory, path, scenes)
    
    print("Scene Overview loaded")

@eel.expose
def load_scene_editor():

    scene = Current.open_projectfile["scenes"][Current.open_scene]

    # set attributes
    root = scene["root"]

    # node container innerHTML
    nodes = "<div class='node' style='background-color:rgba(0,0,0,0);'>"
    # plus button
    nodes += "<img src='img/plus.svg' class='container_icon' style='float:right;' onclick='open_node_creator()'><h3 class='node_title'>Nodes:</h3></div>"

    # add members to team
    for node in scene:

        # ignore root node
        if node != "root":

            # buttons !!! ADD REMOVE AND NODE EDIT FUNCTIONALITY HERE !!!
            nodes += "<img src='img/error.svg' class='container_icon' style='float:right;'><img src='img/edit.svg' class='container_icon' style='float:right;'>"
            # check if directory exists
            # node path
            node_path = os.path.join(projects[Current.open_project][0], root, scene["root"], scene[node][1], node).replace("\\", "/")

            # does path exist
            if os.path.isdir(node_path):
                nodes += f"<img src='img/folder.svg' title='{node_path}' onclick='eel.explore(this.title)' class='container_icon' style='float:right;'>"
            else:
                nodes += f"<img src='img/add_folder.svg' title='{node_path}' onclick='eel.explore(this.title)' class='container_icon' style='float:right;'>"
            
            # node name
            nodes += f"<h3 class='node_title'>{node}</h3>"

            # node data
            nodes += f"<h3>Node Dir: {scene[node][0]}</h3>"
            nodes += f"<h3>Node Type: {scene[node][1]}</h3>"

            # programs
            if scene[node][2] != "": nodes += f"<h3>Programs: {scene[node][2]}</h3>"

            # ports
            nodes += f"<label>{str(scene[node][3])}</label></div>"

    # check if directory exists

    # path variable to return to html
    path = projects[Current.open_project][0]

    # make directory the full path
    directory = os.path.join(path, root, scene["root"]).replace("\\", "/")

    # does path exist
    if os.path.exists(directory):
        path = 1
    else:
        path = 0

    # update ui
    eel.scene_editor(Current.open_scene, directory, path, nodes)
    
    print("Scene Editor loaded")


# run eel if main
if __name__ == "__main__":

    # load json
    projects = load_projects()

    # init eel at directory "web"
    eel.init("web")
    # start eel
    eel.start("main.html")