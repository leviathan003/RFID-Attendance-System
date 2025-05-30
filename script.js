function scanAttendance() {
  document.getElementById('attendanceModal').classList.remove('hidden');
  document.getElementById('status').innerText = 'Waiting for RFID scan to record attendance...';
}

function submitDate() {
  const date = document.getElementById('attendanceDate').value;
  if (!date) {
    alert("Please select a date.");
  } else {
    alert("Attendance recorded for: " + date);
    closeModal();
    document.getElementById('status').innerText = `Attendance submitted for ${date}`;
  }
}

function closeModal() {
  document.getElementById('attendanceModal').classList.add('hidden');
}

function scanNewEntry() {
  document.getElementById('status').innerText = 'Waiting for RFID scan to register new entry...';
  setTimeout(() => {
    document.getElementById('status').innerText = 'New entry registered successfully!';
  }, 2000);
}






