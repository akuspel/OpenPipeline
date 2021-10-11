// set up project overview
function project_overview(name, directory, description, team, exists) {

    document.getElementById("project_name").innerText = "Name: " + name;
    document.getElementById("project_directory").innerText = directory;
    document.getElementById("project_description").innerText = description;

    document.getElementById("project_team").innerHTML = team;

    if (exists == false) {
        document.getElementById("folder_icon").src = "img/add_folder.svg";
        document.getElementById("folder_icon").title = "Add Directory";
        document.getElementById("project_directory").style = "color:rgb(150,30,30); margin-left:20px;";
    }

    console.log("Project Overview loaded")

}

// set up project editor
function project_editor(name, directory, description) {

    document.getElementById("project_name").value = name;
    document.getElementById("project_directory").value = directory;
    document.getElementById("project_description").textContent = description;

    console.log("Project Editor loaded")

}

// set up member editor
function member_editor(name, email, role) {

    document.getElementById("member_name").value = name;
    document.getElementById("member_email").value = email;
    document.getElementById("member_email").role = role;

    console.log("Member Editor loaded")

}

// edit member
function member_edit(name, email, role) {

    eel.add_member(name, email, role);
    eel.remove_member();

}


// closing side bar
function close_side_bar() {

    console.log("Toggle Side Bar")

    if (document.getElementById("side_container").hidden == false) {

        document.getElementById("side_container").hidden = true;
        document.getElementById("side_bar_label").textContent = "> Projects";

    } else {
        
        document.getElementById("side_container").hidden = false;
        document.getElementById("side_bar_label").textContent = "v Projects";

    }
   
}

// linking through divs
function link(url) {
    
    window.location = url;

}

var urls = {
    main: "main.html",
    help: "help.html",
    license: "license.html",

    project_overview: "project_overview.html",
    project_creation: "project_creation.html",
    project_editor: "project_editor.html",

    member_creation: "member_creation.html",
    member_editor: "member_editor.html"
}

// remove tool
function remove(mode) {

    if (mode != "Remove") {

        var x = confirm("Are you sure you want to " + mode + "?")
    
        if (x == true) {
    
            if (mode == "Remove Project") {
                eel.remove_project()
            } else if (mode == "Remove Member") {
                eel.remove_member()
                // change ui
                link(urls.project_overview)
            } else {
                console.error("Unable to Remove Anything - Is removable object currenly open?")
            }
       
        } else  {
    
            console.log("Removal Canceled")
    
        }
   }  
}

// make top bar work
function top_bar() {
    
    console.log("Top Bar loaded");
    document.getElementById("top_bar").innerHTML="<img src='img/logo.svg' id='logo' onclick='link(urls.main)' title='Home Page'> <div class='top_bar_item'>File</div> <div class='top_bar_item'>Edit</div> <div class='top_bar_item'>Settings</div> <div class='top_bar_item' onclick='link(urls.help)'>Help</div> <div class='top_bar_item' onclick='link(urls.license)'>License</div>  <img src='img/reload.svg' class='top_icon' onclick='top_bar(),eel.load_side_bar()' title='Refresh UI'> <img src='img/trash.svg' id='remove' class='top_icon' onclick='remove(this.title)' title='Remove'>";
    
}


// make side bar work
function side_bar(value) {

    console.log("Side Bar loaded");
    document.getElementById("side_bar").innerHTML=value;
    //document.getElementById("side_bar").innerHTML="<label id='side_bar_label' onclick='close_side_bar()'>v Projects</label> <img src='img/plus.svg' id='side_icon' onclick='open(main.html)'> <div id='side_container'> <div class='side_bar_item' onclick='link(urls.project_overview)'>Project aaa_something_something</div> <div class='side_bar_item'>Project 2</div> </div>";

}