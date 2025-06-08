from flask import Flask, render_template, request, jsonify
from db import retrieve_daily_attendance

DATE_DATA=""
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('landing_page.html')

@app.route('/attendance')
def goToAttendancePage():
    return render_template('attendance_page.html')

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
