let scannedTagId = "";
const label = document.getElementsByClassName('popup-label')[0];
const loader = document.getElementById('loader');
const tagId = document.getElementById('tagId');

window.onload = () => {
    showPopup();
    scannedTagId="00 00 00 00";
    fetchRFID();
}

function showError(msg){
    label.innerText = msg;
    loader.classList.remove('loader');
    loader.src = '../static/assets/red-cross.png';
    showPopup();
    setTimeout(()=>{
        loader.classList.add('loader');
        loader.src = '../static/assets/loading-logo.svg'; 
        label.innerText = 'SCANNING TAG ID FOR NEW ENTRY';
    }, 2000);
}

function showPopup(){
    document.getElementById('popup').style.display = 'flex';
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
}

function fetchRFID() {
    fetch('/get_rfid')
    .then(response => response.json())
    .then(data => {
        if(data.rfid==='Tag ID already Registered'){
            showError(data.rfid);
            setTimeout(() => {
                showPopup();       // Show popup again after delay
                fetchRFID();       // Continue polling
            }, 1000);
        } 
        else if (data.rfid) {
            loader.classList.remove('loader');
            loader.src = '../static/assets/green-tick.svg';
            label.innerText = "Tag ID Detected";
            setTimeout(() => {
                closePopup(); 
            }, 2000);
            tagId.value=data.rfid;
        } 
        else {
            // Keep polling until a valid tag is received
            setTimeout(fetchRFID, 1000); // 1 second delay
        }
    })
    .catch(error => {
        console.error('Error fetching RFID:', error);
        setTimeout(fetchRFID, 2000); // Retry after 2 seconds on error
    });
}

document.getElementById('inputForm').addEventListener('submit', function(e) {
    e.preventDefault(); 
    const tagIdValue = document.getElementById('tagId').value;
    const rollValue = document.getElementById('rollNo').value;
    const nameValue = document.getElementById('name').value;
    const isRollValid = /^[0-9lt]+$/.test(rollValue);       
    const isNameValid = /^[A-Za-z\s ]+$/.test(nameValue);
    if(tagIdValue=="" || rollValue=="" || nameValue==""){
        showError("One or more values are Empty");
    }
    else if (!isRollValid) {
        showError("Roll Number is Invalid");
    }
    else if (!isNameValid) {
        showError("Name is Invalid")
    }
    if (isRollValid && isNameValid) {
        const formData = {
            tagId: tagIdValue,
            roll: rollValue,
            name: nameValue
        };
        fetch('/register_new_tag', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            console.log(data);
            loader.classList.remove('loader');
            loader.src = '../static/assets/green-tick.svg';
            label.innerText = "New Entry Added Successfully";
            showPopup();
            setTimeout(() => {
                closePopup(); 
            }, 2000);
        })
        .catch(error => {
            console.error('Error submitting form:', error);
            showError("Submission failed. Try again.");
        });
    }
});