from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from .user import User
from pprint import pprint
from datetime import date, datetime, timedelta


class Course:
    db_name = 'courses'

    def __init__(self, db_data):
        if "courses.id" in db_data:
            self.id = db_data['courses.id']
        else:
            self.id = db_data['id']
            self.course = db_data['course']
        self.hole = db_data['hole']
        self.tee = db_data['tee']
        self.date = db_data['date']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user = None


    @classmethod
    def save(cls, data):
        query = "INSERT INTO courses (course, hole, tee, date, user_id) VALUES ( %(course)s, %(hole)s, %(tee)s, %(date)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM courses;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_courses = []
        for row in results:
            all_courses.append(cls(row))
        return all_courses

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM courses WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        pprint(results)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE courses SET course=%(course)s, hole=%(hole)s, tee=%(tee)s, date=%(date)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM courses WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def merge(cls, data):
        query = "SELECT * FROM courses JOIN users ON users.id = courses.user_id WHERE courses.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        pprint(results)
        user = {
            'id': results[0]["users.id"],
            'first_name': results[0]["first_name"],
            'last_name': results[0]["last_name"],
            'email': results[0]["email"],
            'password': results[0]["password"],
            'created_at': results[0]["users.created_at"],
            'updated_at': results[0]["users.updated_at"]
        }
        this_user = User(user)
        course = cls(results[0])
        course.user = this_user
        return course

    @classmethod
    def merges(cls):
        query = "SELECT * FROM users JOIN courses ON users.id = courses.user_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        courses = []
        pprint(results)
        for row in results:
            user = User(row)
            course = cls(row)
            course.user = user
            courses.append(course)
        return courses

    @staticmethod
    def validate_course(courses):
        result = datetime.strptime(courses['date'], '%Y-%m-%d').date()
        today = date.today()
        is_valid = True
        if len(courses['course']) < 3:
            is_valid = False
            flash("Course must be at least 3 characters", "courses")
        if len(courses['hole']) < 1:
            is_valid = False
            flash("Hole must be atleast 1 character", "courses")
        if len(courses['tee']) < 3:
            is_valid = False
            flash("Tees must be atleast 3 characters", "courses")
        if result < today:
            is_valid = False
            flash("Date can not be in the past. Please revise", "courses")
        return is_valid
