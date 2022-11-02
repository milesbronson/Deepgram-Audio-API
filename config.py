"""CONFIGURATION"""
import pathlib

DEEPGRAM_AUDIO_ROOT = pathlib.Path(__file__).resolve()
UPLOAD_FOLDER = DEEPGRAM_AUDIO_ROOT/'database'/'uploads'
DATABASE_FILENAME = DEEPGRAM_AUDIO_ROOT/'var'/'deepgramAudio.sqlite3'