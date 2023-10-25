from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connection_string = 'mongodb://sumagunawan:sugunjenk10@ac-pig4g6g-shard-00-00.lm8jmgi.mongodb.net:27017,ac-pig4g6g-shard-00-01.lm8jmgi.mongodb.net:27017,ac-pig4g6g-shard-00-02.lm8jmgi.mongodb.net:27017/?ssl=true&replicaSet=atlas-w3dsec-shard-0&authSource=admin&retryWrites=true&w=majority&appName=AtlasApp'
client = MongoClient(connection_string)
db = client.dbsumagunawan

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))

    return jsonify({'articles': articles})


@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    # Cek apakah gambar telah diunggah
    if 'file_give' in request.files:
        file = request.files['file_give']
        extension = file.filename.split('.')[-1]
        filename = f'static/post-{mytime}.{extension}'
        file.save(filename)
    else:
        # Gunakan gambar default jika tidak ada gambar yang diunggah
        filename = 'static/default.jpg'

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{mytime}.{extension}'
    profile.save(profilename)

    time = today.strftime('%Y.%m.%d')

    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive,
        'time': time,
    }
    db.diary.insert_one(doc)
    return jsonify({'msg': 'data was saved'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)