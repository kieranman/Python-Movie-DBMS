from flask import Flask , redirect , url_for , render_template,request,flash
import Movie
import sqlite3 as sql
import os

app = Flask(__name__)

def getConnection():
    return sql.connect(os.path.join(os.path.dirname(__file__), 'filmflix.db'))

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/addMovie",methods=["GET","POST"])
def addMovie():
    if(request.method == "POST"):
        title = request.form["title"]
        yearReleased =int( request.form["yearReleased"])
        rating = request.form["rating"]
        duration =int( request.form["duration"])
        genre = request.form["genre"]

        print(title,yearReleased,rating,duration,genre)
        dbCon = getConnection()
        dbCursor = dbCon.cursor()
        dbCursor.execute("INSERT INTO tblFilms (title, yearReleased, rating, duration, genre) VALUES (?, ?, ?, ?, ?)",
                      (title, yearReleased, rating, duration, genre))
        dbCon.commit()
        dbCon.close()
        return render_template("add.html")
    return render_template("add.html")


def getMovieByField(field,data):
        dbCon = getConnection()
        dbCursor = dbCon.cursor()
        dbCursor.execute(f"SELECT * FROM tblFilms WHERE {field} = ?" ,(data,))
        allMovies = dbCursor.fetchall()
        movieList = []
        for row in allMovies:
            movie = Movie.Movie(row[0],row[1],row[2],row[3],row[4],row[5])
            movieList.append(movie)
        return movieList
        

def displayAllMovies():
        dbCon = getConnection()
        dbCursor = dbCon.cursor()
        dbCursor.execute("SELECT * FROM tblFilms")
        allMovies = dbCursor.fetchall()

        movieList = []

        for row in allMovies:
            movie = Movie.Movie(row[0],row[1],row[2],row[3],row[4],row[5])
            movieList.append(movie)
        return movieList


@app.route("/readMovie",methods=["GET","POST"])
def readMovie():
    if(request.method=="GET"):
        movieList = displayAllMovies()
        return render_template("read.html",data=movieList)
    elif(request.method =="POST"):
        field = request.form["field"]
        data = request.form["data"]
        movieList = getMovieByField(field,data)
        return render_template("read.html",data=movieList)


@app.route("/deleteByMovieId/<int:movieId>", methods=["POST"])
def deleteByMovieId(movieId):
    dbCon = getConnection()
    dbCursor = dbCon.cursor()
    dbCursor.execute(f"DELETE FROM tblFilms WHERE filmID = {movieId}")
    dbCon.commit()
    return deleteMovie()


@app.route("/deleteMovie", methods=["GET","POST"])
def deleteMovie():
    movieList = displayAllMovies()
    return render_template("delete.html",data=movieList)

@app.route("/ammendMovieById/<int:movieId>", methods=["GET", "POST"])
def ammendById(movieId):
    if request.method == "GET":
        dbCon = getConnection()
        dbCursor = dbCon.cursor()
        dbCursor.execute(f"SELECT * FROM tblFilms WHERE filmId = {movieId}")
        movie = dbCursor.fetchone()  # Fetch the movie data
        # Don't forget to close the database connection
        dbCon.close()
        return render_template("ammendMovieById.html", data=movie)
    if(request.method == "POST"):
        title = request.form["title"]
        yearReleased =int( request.form["yearReleased"])
        rating = request.form["rating"]
        duration =int( request.form["duration"])
        genre = request.form["genre"]

        dbCon = getConnection()
        dbCursor = dbCon.cursor()
        dbCursor.execute(
            "UPDATE tblFilms SET title = ?, yearReleased = ?, rating = ?, duration = ?, genre = ? WHERE filmID = ?",
            (title, yearReleased, rating, duration, genre, movieId)
            )
        dbCon.commit()
        dbCon.close()
        return render_template("index.html")


@app.route("/ammendMovie", methods=["GET", "POST"])
def ammendMovie():
    if request.method == "GET":
        movieList = displayAllMovies()
        return render_template("ammend.html", data=movieList)

if __name__ == '__main__':
    app.config['SECRET_KEY'] = os.urandom(24)
    app.run(debug=True)