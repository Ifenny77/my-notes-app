from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# This tells Python where to save your database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

# This defines what a "Note" looks like in our database
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

# Create the database file automatically
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Pull all notes from the database to show them
    all_notes = Note.query.all()
    return render_template('index.html', notes=all_notes)

@app.route('/add', methods=['POST'])
def add_note():
    # Get the text from the input box
    note_text = request.form.get('content')
    if note_text:
        new_note = Note(content=note_text)
        db.session.add(new_note)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_note(id):
    note_to_delete = Note.query.get_or_404(id)
    db.session.delete(note_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
