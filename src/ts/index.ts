console.log("Hello world")

/*
    Things to impl:
    - in "Options", once a user uploads a file, add the name of the file after "File:" for clarity
*/

function toggleOptions(category: string) {
    let checkbox = null;

    switch(category) {
        case "usernames":
            checkbox = <HTMLInputElement>document.getElementById("extract-usernames");
            break;
        case "participation":
            checkbox = <HTMLInputElement>document.getElementById("track-participation");
            break;
        default:
            console.error(`Checkbox for category "${category}" not found.`);
            return;
    }

    let optionsDivId = `${category}-options`;
    let optionsDiv = <HTMLElement>document.getElementById(optionsDivId);

    if (checkbox.checked == true) {
        optionsDiv.style.display = "block";
    } else {
        optionsDiv.style.display = "none";
    }
}