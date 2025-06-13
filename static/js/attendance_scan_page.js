const label = document.getElementsByClassName('popup-label')[0];
const loader = document.getElementById('loader');
const dateEntry = document.getElementById('date-entry');
const dateBtn = document.getElementById('date-btn');
const popUpBox = document.getElementById('popup-box');
let currentData = "";

window.onload = () => {
    showPopup();  
}

function showError(msg){
    popUpBox.style.width='15%';
    label.innerText = msg;
    label.style.display = "flex";
    loader.classList.remove('loader');
    loader.style.display = "flex";
    dateEntry.style.display = "none";
    dateBtn.style.display = "none";
    showPopup();
    setTimeout(() => {
        closePopup();
        popUpBox.style.width='30%';
        dateEntry.style.display = "flex";
        dateBtn.style.display = "block";
        label.style.display = "none";
        loader.style.display = "none";
        showPopup();
    }, 2000);
}

function showPopup(){
    document.getElementById('popup').style.display = 'flex';
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
}

function isValidDate(date){
    const regex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
    const match = date.match(regex);
    if (!match) return false;

    const day = parseInt(match[1], 10);
    const month = parseInt(match[2], 10) - 1; 
    const year = parseInt(match[3], 10);

    const d = new Date(year, month, day);

    return (
        d.getFullYear() === year &&
        d.getMonth() === month &&
        d.getDate() === day
    );
}

function getTableDataByDate(){
    const date = document.getElementById('date-entry').value;
    if(date==''){
        showError("Date cant be Empty");
    }
    else if(!isValidDate(date)){
        showError("Invalid Date Entry");
    }
    else{
        popUpBox.style.width='20%';
        label.style.display = "flex";
        loader.classList.remove('loader');
        loader.style.display = "flex";
        dateEntry.style.display = "none";
        dateBtn.style.display = "none";
        loader.classList.remove('loader');
        loader.src = '../static/assets/green-tick.svg';
        label.innerText = "Database Created/Connected";
        loadTable(date.replaceAll('/', '_'));
        setTimeout(() => {
            closePopup(); 
        }, 2000);
    }
}

function loadTable(db){
    fetch('/load_table', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ db: db })
    })
    .then(response => response.json())
    .then(data => {
        const rows = data.data.rows;
        const newData = JSON.stringify(rows);
        if (newData !== currentData) {
            currentData = newData;
            const tbody = document.querySelector('.attendance-table tbody');
            tbody.innerHTML = '';
            rows.forEach(row => {
                const tr = document.createElement('tr');
                row.forEach(cell => {
                    const td = document.createElement('td');
                    td.textContent = cell;
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

setInterval(() => {
    const date = document.getElementById("date-entry").value;
    if (date) {
        loadTable(date.replace(/\//g, "_"));
    }
}, 5000);


let attendanceInterval = null;
dateBtn.addEventListener('click', () => {
    const date = document.getElementById('date-entry').value.trim();
    if (attendanceInterval) clearInterval(attendanceInterval); 
    attendanceInterval = setInterval(() => {
        fetch('/register_attendance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ date: date })
        })
        .then(response => {
            if (!response.ok) throw new Error("Server error");
            return response.json();
        })
        .catch(error => {
        });
    }, 3000);
});
