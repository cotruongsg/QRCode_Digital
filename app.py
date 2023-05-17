from flask import Flask, redirect, render_template , flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm
# from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tvbqnjbu:cEw8E-hckG1UyjcOgK2jxQajiMWY6Vfk@mahmud.db.elephantsql.com/tvbqnjbu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

connect_db(app)

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)

# @app.route("/playlists/add", methods=["GET", "POST"])
# def add_playlist():
#     """Handle add-playlist form:

#     - if form not filled out or invalid: show form
#     - if valid: add playlist to SQLA and redirect to list-of-playlists
#     """
#      # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
#     form = PlaylistForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         description = form.description.data
#         new_playlist= Playlist(name=name, description=description)
#         db.session.add(new_playlist)
#         try:
#             db.session.commit()
#         except IntegrityError:
#             form.name.errors.append('Name taken.  Please pick another')
#             return render_template('new_playlist.html', form=form)
#         flash('Successfully Created New Playlist')
#         return redirect('/playlists')

#     return render_template('new_playlist.html', form=form)  


# @app.route("/playlists/<int:playlist_id>")
# def show_playlist(playlist_id):
#     """Show detail on specific playlist."""

#     # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
#     playlist = Playlist.query.get_or_404(playlist_id)
   
#     # PlaylistSong.query.filter_by(playlist_id=playlist_id) this will return object which have 
#     # all information about id want to search : <flask_sqlalchemy.query.Query object at 0x000001E693D70A90>
#     # for s in ... will print <PlaylistSong 1> <PlaylistSong 5> then find s.song_id and append to array
#     songs_id=[s.song_id for s in PlaylistSong.query.filter_by(playlist_id=playlist_id)]
#     # songs will print [<Song 1>, <Song 2>]
#     songs = [Song.query.get(id) for id in songs_id]    
#     return render_template('playlist.html', playlist=playlist, songs=songs)


# ##############################################################################
# # Song routes


# @app.route("/songs")
# def show_all_songs():
#     """Show list of songs."""

#     songs = Song.query.all()
#     return render_template("songs.html", songs=songs)


# @app.route("/songs/<int:song_id>")
# def show_song(song_id):
#     """return a specific song"""

#     # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
#     song = Song.query.get_or_404(song_id)
    
#     # Find the list of all playlist_id that have the specific song_id, which we are looking for. We need to do this stuff
#     # because we need to show all the playlist of this song_id in html file.
#     playlists_id = [p.playlist_id for p in PlaylistSong.query.filter_by(song_id=song_id)]

#     # List all the playlist id and playlist name of all playlists which is in the list above
#     # will return a playlists tuple 
#     # Ex : [(1, 'Dance'), (2, 'Nhac Viet Nam'), (3, 'Cha Cha Cha')]
#     playlists = db.session.query(Playlist.id, Playlist.name).filter(Playlist.id.in_(playlists_id)).all()
    
#     return render_template('song.html', song=song, playlists=playlists)   


# @app.route("/songs/add", methods=["GET", "POST"])
# def add_song():
#     """Handle add-song form:

#     - if form not filled out or invalid: show form
#     - if valid: add playlist to SQLA and redirect to list-of-songs
#     """

#     # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
#     form = SongForm()
#     if form.validate_on_submit():
#         title = form.title.data
#         artist = form.title.data
#         new_song = Song(title=title, artist=artist)
#         db.session.add(new_song)
#         try:
#             db.session.commit()
#         except IntegrityError:
#             form.title.errors.append('Title taken.  Please pick another')
#             return render_template("new_song.html", form=form)
#         flash('Successfully Created New Song')
#         return redirect('/songs')
#     return render_template("new_song.html", form=form)


# @app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
# def add_song_to_playlist(playlist_id):
#     """Add a playlist and redirect to list."""

#     # BONUS - ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

#     # THE SOLUTION TO THIS IS IN A HINT IN THE ASSESSMENT INSTRUCTIONS

#     playlist = Playlist.query.get_or_404(playlist_id)
#     form = NewSongForPlaylistForm()


#     # Restrict form to songs not already on this playlist

#     songs_id = [s.song_id for s in PlaylistSong.query.filter_by(playlist_id=playlist_id)]
#     songs = db.session.query(Song.id, Song.title).filter(Song.id.notin_(songs_id)).all()
    
#     # Each tuple in the list contains two values: the first value is the string representation of the id of a song, and the second value is the title of the song.
#     # The str() function is used to convert the id integer value to a string because SelectField expects the choices to be strings. 
#     # The song[0] and song[1] are used to access the first and second values respectively of each song tuple in the songs list.
#     form.song.choices = [(str(song[0]), song[1]) for song in songs]

#     if form.validate_on_submit():

#           # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
#           playlist_song = PlaylistSong(song_id=form.song.data,
#                                   playlist_id=playlist_id)
#           db.session.add(playlist_song)
#           db.session.commit()
#           return redirect(f"/playlists/{playlist_id}")

#     return render_template("add_song_to_playlist.html",
#                              playlist=playlist,
#                              form=form)