from flask import Flask, request, render_template
import os
import json
import datetime
import subprocess

app = Flask(__name__)
received_values = []

@app.route('/')
def hello_world():
    return "Hello, World!"


@app.route('/receive-data', methods=['POST'])
def receive_data():
    data = request.form.get('temperature')

    
    if data is not None:
        received_values.append(f'temperature: {data}')
        if len(received_values) == 24:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            file_name = f'data_{timestamp}.txt'

            with open(file_name, 'w') as file:
                for value in received_values:
                    file.write(value + '\n')

            received_values.clear()
            PROCESS=subprocess.Popen("ots stamp "+str(file_name), stdout= subprocess.PIPE, shell=True)
            value=PROCESS.communicate()[0].split()
            print(value)
            return f"24 values received and file {file_name} created."

    return "Received data..."
    
@app.route('/verify-data/<metrics_name>', methods=['GET'])
def verify_data(metrics_name):
    PROCESS=subprocess.Popen("ots verify "+str(metrics_name), stdout= subprocess.PIPE, shell=True)
    return '200.OK'

@app.route('/data-info/<metrics_name>', methods=['GET'])
def data_info(metrics_name):
    PROCESS=subprocess.Popen("ots info "+str(metrics_name), stdout= subprocess.PIPE, shell=True)
    return '200.OK'

if __name__ == '__main__':
    app.run(host='192.168.1.72', port=5000)