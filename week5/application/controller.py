from flask import request, render_template, Blueprint
from .models import Student, Course, Enrollment
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    students = Student.query.all()
    return render_template('home.html', students=students)

@main_bp.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        roll_number = request.form['roll_number']

        student = Student(first_name=first_name, last_name=last_name, roll_number=roll_number)
        
        course_ids = request.form.getlist('courses')
        
        for course_id in course_ids:
            course = Course.query.get(course_id)
            if course:
                enrollment = Enrollment(student=student, course=course)
                db.session.add(enrollment)
        
        db.session.add(student)
        db.session.commit()
        
        return 'Student created successfully'
    
    courses = Course.query.all()
    return render_template('create.html', courses=courses)
