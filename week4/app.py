import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Template
from flask import Flask , render_template , request

app=Flask(__name__)

def clean(data):
    data=data.rename(columns={' Course id':'Course id',' Marks':'Marks'})
    return data

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == "POST" :
        print("*********************")
        print("got post")
        data = pd.read_csv('data.csv')
        data = clean(data)
        try:
            type = request.form.get("ID")
            id=int(request.form.get('id_value'))
            id_value=int(request.form.get('id_value'))
            print("id requested",id)
            print("type is",type)
            if type == 'Student ID' and id in data['Student id'].tolist():
                selected_students = data[data['Student id']==id_value]
                print(selected_students)
                total=selected_students['Marks'].sum()
                selected_students=selected_students.values.tolist()
                return render_template('student-details.html',students=selected_students,total=total)
            
            else:
                marks = data[data['Course id']==id_value]['Marks'].values
                plt.figure(figsize=(4, 4))
                plt.xlabel('Marks')
                plt.ylabel('Frequency')
                plt.hist((marks))
                img_path = './static/images/plot.png'
                plt.savefig(img_path)
                plt.close()
                Average_marks=sum(marks)/len(marks)
                Maximum_marks=max(marks)
                return render_template('course-details.html',Average_marks=Average_marks,Maximum_marks=Maximum_marks,image=img_path)

        except Exception as e:
            return render_template('error.html',error=e)
        
    else:
        return render_template('index.html')
if __name__=="__main__":
    app.run()


                 