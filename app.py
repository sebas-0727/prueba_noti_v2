from flask import Flask, jsonify, render_template
import pymysql
from datetime import datetime

app = Flask(__name__)

db_config = {
    'host': 'io0727.mysql.pythonanywhere-services.com',
    'user': 'io0727',
    'password': '^@k4,FB7RQ2?G_z',
    'database': 'io0727$default',
    'port': 3306
}

def get_last_report():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT numero, zona, hora, observaciones FROM reporte ORDER BY numero DESC LIMIT 1")
            result = cursor.fetchone()
        
        if result:
            return {
                'numero': result[0],
                'zona': result[1],
                'hora': result[2].isoformat() if isinstance(result[2], datetime) else result[2],
                'observaciones': result[3],
                'timestamp': datetime.now().isoformat()
            }
        return None
    finally:
        connection.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-last-report')
def check_new_number():
    report = get_last_report()
    return jsonify(report) if report else jsonify({})

if __name__=='__main__':
    app.run(debug=True)