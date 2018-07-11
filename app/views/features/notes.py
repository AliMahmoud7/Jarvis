import sqlite3
from datetime import datetime

# from app.views.features.respond.tts import tts


def show_all_notes(database_path):
    conn = sqlite3.connect(database_path)
    saved_notes = '''Your notes are as follows:
    '''

    cursor = conn.execute("SELECT notes FROM notes")

    for row in cursor:
        saved_notes += '{} \n'.format(row[0])
        # tts(row[0])

    conn.close()
    return saved_notes


def note_something(database_path, speech_text):
    conn = sqlite3.connect(database_path)
    words_of_message = speech_text.split()
    words_of_message.remove('note')
    cleaned_message = ' '.join(words_of_message)

    conn.execute("INSERT INTO notes (notes, notes_date) VALUES (?, ?)",
                 (cleaned_message, datetime.strftime(datetime.now(), '%d-%m-%Y')))
    conn.commit()
    conn.close()

    return 'Your note has been saved.'
