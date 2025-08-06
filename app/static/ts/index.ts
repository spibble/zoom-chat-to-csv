console.log("Hello world")



// Shows/hides relevant options for checkboxes in the "Options" panel.
function toggleOptions(category: string): void {
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

// Takes uploaded .txt file and sends it to the backend
function processFile(f: File): void {
    console.log(`File received: ${f.name}`);
    console.log(`File type (should be text): ${f.type}`);

    if (f.type != "text/plain") {
        console.error("Uploaded file is not a text file!");
        return;
    }

    sendFile(f);
}

// Helper fn. to send file
function sendFile(f: File) {
    const request = new XMLHttpRequest;
    const formData = new FormData();
    formData.append('file', f);

    console.log("sending file...");
    request.open('POST', '/upload');
    request.send(formData);
}

// Renders a preview of the generated .csv file.
function showPreview(): void {}

// Shows/hides the download button when a .csv file is rendered/unrendered.
function toggleDownload(): void {}

document.getElementById('upload-file').addEventListener('change', function(e) {
    const target = e.target as HTMLInputElement;
    const file = target.files[0];

    if (!file) {
        console.error("File upload failed!");
        return;
    }

    processFile(file);
});

/* copied from reddit, study later */
let downloadBtn = document.getElementById('download-button')
downloadBtn.addEventListener('click', downloadFile)

function downloadFile() {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.status === 200 && xhttp.readyState === 4) {
        let blob = new Blob([xhttp.response], { type: "text/csv" });
        let url = window.URL.createObjectURL(blob);
        let link = document.createElement("a");
        link.href = url;
        link.download = "processed_chat.csv";
        link.style.display = "none";
        document.body.appendChild(link);
        link.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
        }
    };
    xhttp.open("POST", "/download", true);
    xhttp.responseType = "blob";
    xhttp.send();
}

/*
document.getElementById('options-apply').addEventListener('click', function(e) {
    const form = document.getElementById('delimiters-form')

    // copied from stackoverflow
    var rates = document.getElementsByName('rate');
    var rate_value;
    for(var i = 0; i < rates.length; i++){
        if(rates[i].checked){
            rate_value = rates[i].value;
        }
    }
})

document.getElementById('participation-apply').addEventListener('click', function(e) {

})
*/