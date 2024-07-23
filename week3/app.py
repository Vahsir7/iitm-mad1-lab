import sys
import csv
import os
import webbrowser
from jinja2 import Template
import matplotlib.pyplot as plt

def load_csv_data(file_path):
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        sys.exit(1)

def render_template(template_path, output_path, **kwargs):
    try:
        with open(template_path, 'r') as file:
            template_content = file.read()
        template = Template(template_content)
        output = template.render(**kwargs)
        with open(output_path, 'w') as output_file:
            output_file.write(output)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def open_in_browser(file_path):
    webbrowser.open('file://' + os.path.abspath(file_path))

def generate_student_report(data, student_id, output_path):
    student_list = [entry for entry in data if entry[0] == student_id]
    if not student_list:
        raise Exception("No student found")

    total_marks = sum(int(entry[2]) for entry in student_list)
    render_template('student-details.html', output_path, student=student_list, total=total_marks)
    open_in_browser(output_path)
    print("Student report created successfully")

def generate_course_report(data, course_id, output_path):
    marks = [int(entry[2]) for entry in data if entry[1][1:] == course_id]
    if not marks:
        raise Exception("No course found")

    total_marks = sum(marks)
    average_marks = total_marks / len(marks)
    maximum_marks = max(marks)

    plt.figure()
    plt.xlabel('Marks')
    plt.ylabel('Frequency')
    plt.hist(marks, bins=range(min(marks), max(marks) + 1))
    img_path = 'plot.png'
    plt.savefig(img_path)
    plt.close()

    render_template('course-details.html', output_path, Average_marks=average_marks, Maximum_marks=maximum_marks, image=os.path.abspath(img_path))
    open_in_browser(output_path)
    print("Course report created successfully")

def main():
    try:
        args = sys.argv[1:]
        if len(args) < 2:
            print("Usage: script.py [-s|-c] <ID>")
            sys.exit(1)
        
        command, id = args[0], args[1]
        data = load_csv_data('data.csv')
        output_path = 'output.html'

        if command == '-s':
            generate_student_report(data, id, output_path)
        elif command == '-c':
            generate_course_report(data, id, output_path)
        else:
            raise Exception("Invalid command")
    
    except Exception as e:
        print(f"Error: {e}")
        open_in_browser('error.html')
        sys.exit(1)

if __name__ == "__main__":
    main()
