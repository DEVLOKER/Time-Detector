
import json, uuid
import os, time
from flask import Flask, flash, jsonify, request, redirect, abort, url_for, render_template, send_file
from waitress import serve
from TimeDetector import TimeDetector


PORT = 5000
app = Flask(__name__, static_folder='static', static_url_path='/')

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), TimeDetector.INPUT_PATH)
PROCESSED_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), TimeDetector.OUTPUT_PATH)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['SECRET_KEY'] = 'Sick Rat'


@app.route('/')
def index():
    __cleanDirectory(UPLOAD_FOLDER)
    __cleanDirectory(PROCESSED_FOLDER)
    
    # uploaded_files = __get_files(UPLOAD_FOLDER)
    # processed_files = __get_files(PROCESSED_FOLDER)

    return render_template('index.html')#, uploaded_files=uploaded_files, processed_files=processed_files)




@app.route('/get/<name>', methods=['GET'])
def get(name):
    files = __get_files(UPLOAD_FOLDER)
    for file in files:
        if file["name"] == name:
            path = os.path.join(UPLOAD_FOLDER, name)
            if os.path.exists(path):
                return send_file(path)
    abort(404)


@app.route('/download/<name>', methods=['GET'])
def download(name):
    files = __get_files(PROCESSED_FOLDER)
    for file in files:
        if file["name"] == name:
            path = os.path.join(PROCESSED_FOLDER, name)
            if os.path.exists(path):
                return send_file(path)
    abort(404)



@app.route("/upload" , methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    #file = request.files['file']
    app.logger.info(request.files)
    upload_files = request.files.getlist('file')
    app.logger.info(upload_files)
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if not upload_files:
        flash('No selected file')
        return redirect(request.url)
    for file in upload_files:
        original_filename = file.filename
        extension = original_filename.rsplit('.', 1)[1].lower()
        filename = str(uuid.uuid1()) + '.' + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


    results = []
    files = __get_files(os.path.join(TimeDetector.INPUT_PATH))
    for file in files:
        name, size, path = file.values()
        clockImage = os.path.join(path, name)
        result = TimeDetector.detectTime(clockImage)
        if(result!=None):
            results.append(result) # json.dumps(result, indent=4)   result["time"]

    return jsonify(results)
    # flash('Upload succeeded')
    # return redirect(url_for('index'))



def __get_files(dir):
    files = []
    name_list = os.listdir(dir)
    full_list = [os.path.join(dir,i) for i in name_list]
    time_sorted_list = sorted(full_list, key=os.path.getmtime)
    sorted_filename_list = [ os.path.basename(i) for i in time_sorted_list]
    sorted_filename_list.reverse()
    
    for filename in sorted_filename_list:
        sz = os.path.getsize(os.path.join(dir, filename))
        files.append({"name":filename, "size": sz, "path": os.path.join(dir) })
	
    return files


def __cleanDirectory(dir):
    now = time.time()
    timer = 0# 730 * 86400 # 60 minutes : 60 * 60      30 days : 30 * 86400
    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        if os.path.getmtime(path) < now - timer:
            if os.path.isfile(path):
                os.remove(path)




if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
    # serve(app, host="0.0.0.0", port=PORT)