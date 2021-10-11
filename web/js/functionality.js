
// file explorer
function file_explorer(mode) {

    if (mode == "Open Directory") {
        eel.explore(document.getElementById("project_directory").innerText);
    } else if (mode == "Add Directory") {
        eel.explore(document.getElementById("project_directory").innerText);
        link(urls.project_overview);
    }

}