from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.course import Course
from flask_app.models.user import User
import requests


@app.route('/dashboard')
def get_all():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": session['user_id']
    }

    courses = Course.merges()
    return render_template('dashboard.html', user=User.get_by_id(data), courses=courses)


@app.route('/course/new')
def new_show():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('new.html', user=User.get_by_id(data))


@app.route('/new', methods=['POST'])
def create_course():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Course.validate_course(request.form):
        return redirect('/course/new')
    data = {
        "course": request.form["course"],
        "hole": request.form["hole"],
        "tee": request.form["tee"],
        "date": request.form["date"],
        "user_id": session["user_id"]
    }
    Course.save(data)
    return redirect('/dashboard')


@app.route('/edit/<int:id>')
def edit_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template("edit.html", edit=Course.get_one(data), user=User.get_by_id(user_data))


@app.route('/update/course', methods=['POST'])
def update_course():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Course.validate_course(request.form):
        return redirect('/new')
    data = {
        "course": request.form["course"],
        "hole": request.form["hole"],
        "tee": request.form["tee"],
        "date": request.form["date"],
        "id": request.form["id"]
    }
    Course.update(data)
    return redirect('/dashboard')


@app.route('/show/<int:id>')
def show_course(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }

    return render_template("show.html", course=Course.merge(data), user=User.get_by_id(user_data))


@app.route('/destroy/course/<int:id>')
def destroy_course(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Course.destroy(data)
    return redirect('/dashboard')


@app.route('/course')
def course():
    return render_template("location.html")


@app.route('/course/data', methods=['GET', 'POST'])
def get_data():
#     data = {
#         "latitude": request.form['latitude'],
#         "longitude": request.form['longitude'],
#         "radius": request.form['radius']
#     }
#     please_work = Course.save2(data)

    radius = request.form["radius"]
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]

    url = "https://golf-course-finder.p.rapidapi.com/courses"
    params = {"radius": radius, "lat": latitude, "lng": longitude}
    headers = {
        "X-RapidAPI-Key": "ab1d09bf4amsh840dd08b280b8bep193c9fjsn83507321505a",
        "X-RapidAPI-Host": "golf-course-finder.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=params).json()
    print(response)
    return render_template("results.html", course_data=response["courses"])
