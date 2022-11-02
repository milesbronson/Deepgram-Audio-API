from crypt import methods
import pathlib
import sqlite3
import uuid
import flask
import wave

audio = flask.Flask(__name__)

def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def get_db():
    db_filename = audio.config['DATABASE_FILENAME']
    conn = sqlite3.connect(str(db_filename))
    conn.row_factory = dict_factory
    return conn


@audio.route("/post", methods=['POST'])
def post_file():
    """Post Raw Audio File"""
    print("test")
    #print(flask.request.files)
    #print(flask.request.form.__dict__)
    print(flask.request.data)
    file = flask.request.form['onlyFile']

    print("test2")
    filename = file.filename
    print("filename:", filename)
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix
    uuid_basename = f"{stem}{suffix}"
    path = audio.config["UPLOAD_FOLDER"]/uuid_basename
    file.save(path)
    duration_seconds = 0
    with wave.open(file) as file_wav:
        duration_seconds = file_wav.getnframes() / file_wav.getframerate()
    connection = get_db()
    connection.execute(
        "INSERT INTO audio"
        "(filename, filepath, duration) "
        "VALUES (?, ?, ?)",
        (filename, path, duration_seconds, )
    )
    return flask.jsonify(), 201


@audio.route("/download")
def get_file():
    connection = get_db()
    filename = flask.request.args.get('name')
    db_output = connection.execute(
        "SELECT filepath "
        "FROM audio "
        "WHERE filename = ?",
        (filename, )
    )
    files = db_output.fetchall()
    files = db_output.fetchall()
    return_data = []
    for file in files:
        file_data = {
            "filename": file["filename"],
            "filepath": file["filepath"]
        }
        return_data.append(file_data)
    context = {
        "files": return_data
    }
    return context


@audio.route("/list")
def get_list():   
    connection = get_db()
    filename = flask.request.args.get('maxduration')
    db_output = connection.execute(
        "SELECT filepath "
        "FROM audio "
        "WHERE size < ? "
        "OR",
        (filename, )
    )
    files = db_output.fetchall()
    return_data = []
    for file in files:
        file_data = {
            "filename": file["filename"],
            "filepath": file["filepath"]
        }
        return_data.append(file_data)
    context = {
        "files": return_data
    }
    return context

@audio.route("/info")
def get_metadata():
    connection = get_db()
    filename = flask.request.args.get('name')
    db_output = connection.execute(
        "SELECT filename, size, created "
        "FROM audio "
        "WHERE filename = ?",
        (filename, )
    )
    files = db_output.fetchall()
    return_data = []
    for file in files:
        file_data = {
            "filename": file["filename"],
            "size": file["size"],
            "created": file["created"]
        }
        return_data.append(file_data)
    context = {
        "files": return_data
    }
    return context

if __name__ == '__main__':
    audio.run(host='0.0.0.0', port=80)