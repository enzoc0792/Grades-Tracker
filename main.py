# Made by:		Jose Lorenzo Castro
# Date made:	10 Aug 2019
#!/usr/bin/env python

import os
import sqlite3
from flask import Flask, request, render_template

import functions as fun

app = Flask(__name__)

#fun.cleanSlate()
fun.initialize()
#test = fun.findTwoVar('Student', 'Castro', 'Jose Lorenzo')
#if (test):
#    print ('Found Record')
#else:
#    print ('Sadness')

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/add')
def addDir():
    return render_template("add/add.html")

@app.route('/add/student', methods = ['POST', 'GET'])
def addStudent():
    if request.method == 'POST':
        ln = request.form['sln']
        fn = request.form['sfn']

        fun.addTwoVars('Student', ln, fn)

    return render_template("add/addStudent.html")

@app.route('/add/teacher', methods = ['POST', 'GET'])
def addTeacher():
    if request.method == 'POST':
        ln = request.form['tln']
        fn = request.form['tfn']

        fun.addTwoVars('Teacher', ln, fn)

    return render_template("add/addTeacher.html")

@app.route('/add/semester', methods = ['POST', 'GET'])
def addSem():
    if request.method == 'POST':
        sy = request.form['sy']
        sem = request.form['sem']

        fun.addTwoVars('Semester', sy, sem)

    return render_template("add/addSemester.html")

@app.route('/add/classroom', methods = ['POST', 'GET'])
def addClassroom():
    if request.method == 'POST':
        bldg = request.form['building']
        room_num = request.form['roomNum']

        fun.addClassroomListing(bldg, room_num)

    return render_template("add/addClassroom.html")

@app.route('/add/subject', methods = ['POST', 'GET'])
def addSubject():
    if request.method == 'POST':
        subj = request.form['subjName']
        sect = request.form['section']

        fun.addTwoVars('Subject', subj, sect)

    return render_template("add/addSubject.html")

@app.route('/add/record', methods = ['POST', 'GET'])
def addRecord():
    if request.method == 'POST':
        sln = request.form['sln']
        sfn = request.form['sfn']
        sy = request.form['sy']
        sem = request.form['sem']
        subj = request.form['subjName']
        sect = request.form['section']
        tln = request.form['tln']
        tfn = request.form['tfn']
        bldg = request.form['building']
        room_num = request.form['roomNum']
        grade = request.form['grade']

        fun.addStudentRecord(sln, sfn, sy, sem, subj, sect, tln, tfn, bldg, room_num, grade)

    return render_template("add/addRecord.html")

@app.route('/view')
def viewDir():
    return render_template("view/view.html")

@app.route('/view/student_records')
def viewRecords():

    studentName = request.form['sy']
    semSort = request.form['semSort']
    gradeSort = request.form['gradeSort']

    fun.pullDataTwo('Records', studentName, semSort, gradeSort)

    return render_template("view/viewRecords.html")

@app.route('/view/subjects')
def viewSubjects():

    subjName = request.form['sy']
    semSort = request.form['semSort']
    teacherSort = request.form['teacherSort']

    fun.pullDataTwo('Subjects', subjName, semSort, teacherSort)

    return render_template("view/viewSubjects.html")

@app.route('/view/semester')
def viewSem():

    sy = request.form['sy']
    sem = request.form['sem']

    fun.pullSubjInSem(sy, sem)

    return render_template("view/viewSemesters.html")



@app.route('/update')
def upDir():
    return render_template("update/update.html")

@app.route('/update/grade', methods = ['POST', 'GET'])
def upGrade():
    if request.method == 'POST':
        sy = request.form['sy']
        sem = request.form['sem']
        subj = request.form['subjName']
        sect = request.form['section']
        sln = request.form['studentLastName']
        sfn = request.form['studentFirstName']
        newGrade = request.form['setGrade']

        fun.updateEntry('grade', sy, sem, subj, sect, sln, sfn, newGrade)

    return render_template("update/updateGrade.html")

@app.route('/update/section', methods = ['POST', 'GET'])
def upSect():
    if request.method == 'POST':
        sy = request.form['sy']
        sem = request.form['sem']
        subj = request.form['subjName']
        sect = request.form['section']
        tln = request.form['teacherLastName']
        tfn = request.form['teacherFirstName']
        newSection = request.form['setNewSection']

        fun.updateEntry('section', sy, sem, subj, sect, tln, tfn, newSection)

    return render_template("update/updateSection.html")

@app.route('/update/teacher', methods = ['POST', 'GET'])
def upTeacher():
    if request.method == 'POST':
        sy = request.form['sy']
        sem = request.form['sem']
        subj = request.form['subjName']
        sect = request.form['section']
        tln = request.form['teacherLastName']
        tfn = request.form['teacherFirstName']

        fun.updateEntry('teacher', sy, sem, subj, sect, tln, tfn, '')

    return render_template("update/updateTeacher.html")

@app.route('/update/classroom', methods = ['POST', 'GET'])
def upClass():
    if request.method == 'POST':
        sy = request.form['sy']
        sem = request.form['sem']
        subj = request.form['subjName']
        sect = request.form['section']
        bldg = request.form['buildingName']
        room = request.form['roomNumber']

        fun.updateEntry('classroom', sy, sem, subj, sect, bldg, room, '')

    return render_template("update/updateClassroom.html")

@app.route('/delete')
def delete():
    return render_template("delete/delete.html")

@app.route('/delete/student')
def delStudent():


    return render_template("delete/deleteStudent.html")

@app.route('/delete/section')
def delSection():


    return render_template("delete/deleteSection.html")

@app.route('/delete/teacher')
def delTeacher():


    return render_template("delete/deleteTeacher.html")

@app.route('/exit')
def shutdown():
    conn = sqlite3.connect(fun.db)
    cur = conn.cursor()
    cur.close()
    return 0

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port, debug = 'False')

