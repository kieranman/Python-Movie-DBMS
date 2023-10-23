from flask import Flask , redirect , url_for , render_template,request
import Movie
import sqlite3 as sql

app = Flask(__name__)

def getConnection():
    return sql.connect('python-projects/FilmFlix/filmflix.db')

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
        return "Movie added Successfully"

    return render_template("add.html")


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


@app.route("/readMovie",methods=["GET"])
def readMovie():
    if(request.method=="GET"):
        movieList = displayAllMovies()
        return render_template("read.html",data=movieList)

@app.route("/deleteByMovieId", methods=["POST"])
def deleteByMovieId():
    dbCon = getConnection()
    dbCursor = dbCon.cursor()
    dbCursor.execute(f"DELETE FROM tblFilms WHERE filmID = {movieId}")
    dbCon.commit()


@app.route("/deleteMovie", methods=["GET","POST"])
def deleteMovie():
    if(request.method=="GET"):
       movieList = displayAllMovies()
       return render_template("delete.html",data=movieList)
    elif(request.method=="POST"):
        return render_template("delete.html",data=movieList)

if __name__ == '__main__':
    app.run(debug=True)