let scannedTagId = "";
const label = document.getElementsByClassName('popup-label')[0];
const loader = document.getElementById('loader');
const tagId = document.getElementById('tagId');

window.onload = () => {
    showPopup();
    //code to run arduino on backend
    scannedTagId="00 00 00 00"
}

function showError(msg){
    label.innerText = msg;
    loader.classList.remove('loader');
    loader.src = '../static/assets/red-cross.png';
    showPopup()
    setTimeout(() => {
        closePopup(); 
    }, 2000);
}

function showPopup(){
    document.getElementById('popup').style.display = 'flex';
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
}

// function updateTagId(scannedTagId){
//     loader.classList.remove('loader');
//     loader.src = '../assets/green-tick.svg';
//     label.innerText = "Tag ID Detected";
//     setTimeout(() => {
//         closePopup(); 
//     }, 2000);
//     tagId.value=scannedTagId;
// }

document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        loader.classList.remove('loader');
        loader.src = '../static/assets/green-tick.svg';
        label.innerText = "Tag ID Detected";
        setTimeout(() => {
            closePopup(); 
        }, 2000);
        tagId.value=scannedTagId;
    }
});

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
        console.log(formData);
        //Code for backend here
        loader.classList.remove('loader');
        loader.src = '../static/assets/green-tick.svg';
        label.innerText = "New Entry Added Successfully";
        showPopup();
        setTimeout(() => {
            closePopup(); 
        }, 2000);
    }
});