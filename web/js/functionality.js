
// file explorer
function file_explorer(mode, redirect, id) {

    if (mode == "Open Directory") {
        eel.explore(document.getElementById(id).innerText);
    } else if (mode == "Add Directory") {
        eel.explore(document.getElementById(id).innerText);
        link(redirect);
    }

}