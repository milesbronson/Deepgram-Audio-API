from crypt import methods
import pathlib
import sqlite3
import uuid
import flask
import wave
 
DEEPGRAM_AUDIO_ROOT = pathlib.Path(__file__).resolve().parent
UPLOAD_FOLDER = DEEPGRAM_AUDIO_ROOT/'database'/'uploads'
DATABASE_FILENAME = DEEPGRAM_AUDIO_ROOT/'database'/'deepgramAudio.db'

audio = flask.Flask(__name__)



def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def get_db():
    db_filename = DATABASE_FILENAME
    flask.g.conn = sqlite3.connect(str(db_filename))
    flask.g.conn.row_factory = dict_factory
    flask.g.conn.execute("PRAGMA foreign_keys = ON")
    return flask.g.conn


@audio.route("/post", methods=['POST'])
def post_file():
    """Post Raw Audio File"""
    file = flask.request.files['file']
    filename = file.filename
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix
    uuid_basename = f"{stem}{suffix}"
    path = UPLOAD_FOLDER/uuid_basename
    file.save(path)
    duration_seconds = 0
    with wave.open(filename, mode='rb') as file_wav:
        duration_seconds = file_wav.getnframes() // file_wav.getframerate()
    print(duration_seconds)
    print(uuid_basename)
    print(filename)
    connection = get_db()
    connection.execute(
        "INSERT INTO audio(filename, filepath, duration) "
        "VALUES (?, ?, ?)",
        (filename, uuid_basename, duration_seconds)
    )
    connection.commit()
    connection.close()
    return flask.jsonify(), 201


@audio.route("/download")
def get_filename():
    connection = get_db()
    filename = flask.request.args.get('name')
    db_output = connection.execute(
        "SELECT * "
        "FROM audio "
        "WHERE filename = ?",
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
    connection.close()

    return context


@audio.route("/list")
def get_list():   
    connection = get_db()
    maxduration = flask.request.args.get('maxduration')
    db_output = connection.execute(
        "SELECT * "
        "FROM audio "
        "WHERE duration <= ? ",
        (maxduration, )
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
    connection.close()

    return context

@audio.route("/info")
def get_metadata():
    connection = get_db()
    filename = flask.request.args.get('name')
    db_output = connection.execute(
        "SELECT * "
        "FROM audio "
        "WHERE filename = ? "
        "ORDER BY duration",
        (filename, )
    )
    files = db_output.fetchall()
    return_data = []
    for file in files:
        file_data = {
            "filename": file["filename"],
            "duration": file["duration"],
            "created": file["created"]
        }
        return_data.append(file_data)
    context = {
        "files": return_data
    }
    connection.close()

    return context

