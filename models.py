"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Playlist(db.Model):
    """Playlist."""
    __tablename__="playlists"

    # ADD THE NECESSARY CODE HERE
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable= False , unique=True)
    description= db.Column(db.Text, nullable= False)

    # The secondary argument specifies the name of the association table,
    # By using the secondary parameter, SQLAlchemy automatically creates a SQL statement to join the Playlist and Song tables through the playlist_song table
    songs = db.relationship('Song', secondary= 'playlist_song', backref = 'playlists')


class Song(db.Model):
    """Song."""
    __tablename__="songs"

    # ADD THE NECESSARY CODE HERE
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.Text, nullable= False)
    artist= db.Column(db.Text, nullable= False)
    playlist_song= db.relationship('PlaylistSong', backref = 'songs')


class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""

    # ADD THE NECESSARY CODE HERE
    __tablename__="playlist_song"
    
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey(
        'playlists.id'),  nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey(
        'songs.id'), nullable=False)
    


# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

    # Create tables
    with app.app_context():        
        db.create_all()