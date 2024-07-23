from jinja2 import Template
import csv
import sys
import webbrowser
import os

def main():
    try:
        arg = sys.argv[1:]
        if len(arg) < 2:
            print("Usage: python app.py -s <student_id>")
            return

        flag = arg[0]
        student_id = arg[1]

        if flag != '-s':
            print("Invalid flag. Use '-s' to search for student.")
            return

        # Read data from CSV file
        with open('data.csv', 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        # Collect student data
        student_list = []
        total_marks = 0
        for entry in data:
            if entry[0] == student_id:
                student_list.append(entry)
                total_marks += int(entry[2])

        if len(student_list) > 0:
            # Read template from file
            with open('student_details.html', 'r') as student_details_file:
                student_details = student_details_file.read()

            # Render template
            template = Template(student_details)
            output = template.render(student=student_list, total=total_marks)

            # Write output to HTML file
            output_file_path = '/home/rishav/Desktop/iitm-mad1/week3/output.html'
            with open(output_file_path, 'w') as output_file:
                output_file.write(output)

            # Open the HTML file in the default web browser
            webbrowser.open('file://' + os.path.abspath(output_file_path))
            print("Web page opened successfully.")

        else:
            print(f"No records found for student ID {student_id}")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except IndexError as e:
        print(f"Index error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
