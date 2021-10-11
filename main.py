import eel, os, subprocess, json
from json_backend import *

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

    # team innerHTML
    team = "<h4 style='padding:6px;''>Team:</h4>"
    team += "<img src='img/plus.svg' class='container_icon' onclick='link(urls.member_creation)' style='position:relative; float:right; top:-43px;'>"

    # add members to team
    for member in project[2]:
        team += f"<div class='team_member' title='{member[0]} | {member[1]} | {member[2]}' onclick='link(urls.member_editor), eel.set_open_member(this.title)'>{member[0]} ({member[1]}) ({member[2]})</div>"
    
    # check if directory exists
    path = directory
    # add / to end of path
    if len(path) > 0:
        if path[-1] != "/": path += "/"
    else:
        directory = "no path"

    # does path exist
    if os.path.exists(path):
        path = True
    else:
        path = False


    # update ui
    eel.project_overview(name, directory, description, team, path)
    
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


# run eel if main
if __name__ == "__main__":

    # load json
    projects = load_projects()

    # init eel at directory "web"
    eel.init("web")
    # start eel
    eel.start("main.html")