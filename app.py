from flask import Flask, render_template, request, jsonify
from db import retrieve_daily_attendance, get_all_valid_tags, register_newTagID
from rfid_utils import read_rfid, sendMessageToArduino, grant_access, deny_access
import time

DATE_DATA=""
app = Flask(__name__)

LED_G = 7
LED_R = 6
BUZZER = 5

@app.route('/')
def home():
    return render_template('landing_page.html')

@app.route('/attendance')
def goToAttendancePage():
    return render_template('attendance_page.html')

@app.route('/get_rfid')
def get_rfid():
    tag = read_rfid()
    if tag:
        if tag not in get_all_valid_tags():
            sendMessageToArduino(LED_G, "HIGH", BUZZER, "ON", "New Tag ID", "Detected")
            time.sleep(2)
            sendMessageToArduino(LED_G, "LOW", BUZZER, "OFF", "TAG YOUR", "ID CARD")
            return jsonify({'rfid': tag})
        else:
            return jsonify({'rfid':'Tag ID already Registered'})
    return jsonify({'rfid': None})

@app.route('/register_new_tag', methods=['POST'])
def register_new_tag():
    data = request.get_json()
    tag = data.get('tagId')
    roll = data.get('roll')
    name = data.get('name')
    register_newTagID(tag,roll,name)
    return jsonify({'status': 'success', 'message': 'Tag registered'})

@app.route('/register_attendance', methods=['POST'])
def registerAttendance():
    data = request.get_json()
    date = data.get('date')
    tag = read_rfid()
    if tag in get_all_valid_tags():
        grant_access(tag, date)
        return jsonify({'status': 'success', 'message': 'Access granted'})
    if tag==None:
        return jsonify({'status': 'denied', 'message': 'Access denied'})
    else:
        deny_access()
        return jsonify({'status': 'denied', 'message': 'Access denied'})

@app.route('/new_entry')
def goToNewEntryPage():
    return render_template('new_entry_page.html')

@app.route('/load_table', methods=['POST'])
def load_table():
    DATE_DATA = request.get_json()
    db_value = DATE_DATA.get('db')
    attendance = retrieve_daily_attendance(db_value)
    return jsonify({"data": {"rows": attendance}})

if __name__ == '__main__':
    app.run(debug=True)
