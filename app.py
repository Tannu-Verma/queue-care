from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'queuecure2026'
socketio = SocketIO(app, cors_allowed_origins="*")

queue = []
current_patient = None
avg_time = 5

@app.route('/')
def receptionist():
    return render_template('receptionist.html')

@app.route('/waiting')
def waiting():
    return render_template('waiting.html')

@socketio.on('add_patient')
def add_patient(data):
    global queue
    queue.append(data['name'])
    send_update()

@socketio.on('call_next')
def call_next():
    global current_patient, queue
    if queue:
        current_patient = queue.pop(0)
    send_update()

@socketio.on('set_time')
def set_time(data):
    global avg_time
    avg_time = max(1, int(data['time']))
    send_update()

@socketio.on('remove_patient')
def remove_patient(data):
    global queue
    idx = int(data['index'])
    if 0 <= idx < len(queue):
        queue.pop(idx)
    send_update()

def send_update():
    emit('queue_update', {
        'current': current_patient,
        'queue': queue,
        'wait_times': [avg_time * (i + 1) for i in range(len(queue))]
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)