import sqlite3

db = 'studentGrades.sqlite'

def execute(comm):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(comm)
    conn.commit()

def getBackData(comm):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(comm)

    return cur.fetchall()

def cleanSlate():
    tables = ['Student', 'Teacher', 'Grade', 'Building', 'Room', 'Classroom', 'Subject', 'Semester', 'Record']
    for i in tables:
        execute('''DROP TABLE IF EXISTS ''' + i)

def predetVals():
    for i in range(6):
        val = chr(65 + i)
        if i < 3:
            addOneVar('Grade', val)
            val += '+'
        if i == 4:
            continue
        addOneVar('Grade', val)

def initialize():
    comms = ['''CREATE TABLE IF NOT EXISTS Student (
               id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
               l_name    STRING NOT NULL,
               f_name    STRING NOT NULL)''',
             '''CREATE TABLE IF NOT EXISTS Teacher (
               id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
               l_name    STRING NOT NULL,
               f_name    STRING NOT NULL)''',
             '''CREATE TABLE IF NOT EXISTS Grade (
               id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
               grade     VARCHAR(2) NOT NULL)''',
             '''CREATE TABLE IF NOT EXISTS Building (
               id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
               bldg_name VARCHAR(15) NOT NULL)''',
             '''CREATE TABLE IF NOT EXISTS Room (
               id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
               room_num  INTEGER)''',
             '''CREATE TABLE IF NOT EXISTS Classroom (
               id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
               bldg_id   INTEGER,
               room_id   INTEGER,
               FOREIGN KEY (bldg_id) REFERENCES Building(id),
               FOREIGN KEY (room_id) REFERENCES Room(id))''',
             '''CREATE TABLE IF NOT EXISTS Subject (
               id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
               subj_name    STRING NOT NULL,
               section      VARCHAR(2) NOT NULL)''',
             '''CREATE TABLE IF NOT EXISTS Semester(
               id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
               sy         INTEGER NOT NULL,
               sem        VARCHAR(3))''',
             '''CREATE TABLE IF NOT EXISTS Record (
               id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
               student_id   INTEGER,
               sem_id       INTEGER,
               subject_id   INTEGER,
               teacher_id   INTEGER,
               classroom_id INTEGER,
               grade_id     INTEGER,
               FOREIGN KEY (student_id) REFERENCES Student(id),
               FOREIGN KEY (sem_id) REFERENCES Semester(id),
               FOREIGN KEY (subject_id) REFERENCES Subject(id),
               FOREIGN KEY (teacher_id) REFERENCES Teacher(id),
               FOREIGN KEY (classroom_id) REFERENCES Classroom(id),
               FOREIGN KEY (grade_id) REFERENCES Grade(id))'''
                ]

    for i in comms:
        execute(i)

    predetVals()

def addTwoVars(table, one, two):
    comm = ''
    if table == 'Student' or table == 'Teacher':
        comm = '''INSERT OR IGNORE INTO {0} (l_name, f_name) VALUES ('{1}', '{2}')'''.format(table, one, two)
    elif table == 'Subject':
        comm = '''INSERT OR IGNORE INTO Subject (subj_name, section) VALUES ('{0}', '{1}')'''.format(one, two)
    elif table == 'Semester':
        comm = '''INSERT OR IGNORE INTO Semester (sy, sem) VALUES ({0}, '{1}')'''.format(one, two)
    else:
        return
    execute(comm)

def addOneVar(table, one):
    comm = ''
    if table == 'Building':
        comm = '''INSERT OR IGNORE INTO Building (bldg_name) VALUES ('{0}')'''.format(one)
    elif table == 'Room':
        comm = '''INSERT OR IGNORE INTO Room (room_num) VALUES ({0})'''.format(one)
    elif table == 'Grade':
        comm = '''INSERT OR IGNORE INTO Grade (grade) VALUES ('{0}')'''.format(one)
    else:
        return
    execute(comm)

def addClassroomListing(bldg, rn):
    addOneVar('Building', bldg)
    print(bldg, rn)
    addOneVar('Room', rn)
    b_id = findOneVar('Building', 'bldg_name', bldg)[0][0]
    r_id = findOneVar('Room', 'room_num', rn)[0][0]

    comm = '''INSERT OR IGNORE INTO Classroom (bldg_id, room_id) VALUES ({0}, {1})'''.format(b_id, r_id)
    execute(comm)

def addStudentRecord(sln, sfn, sy, sem, subj, sect, tln, tfn, bldg, room_num, grade):
    student_id = findTwoVar('Student', sln, sfn)
    sem_id = findTwoVar('Semester', sy, sem)
    subj_id = findTwoVar('Subject', subj, sect)
    teacher_id = findTwoVar('Teacher', tln, tfn)
    classroom_id = findTwoVar('Classroom', bldg, room_num)
    grade = findOneVar('Grade', 'grade', grade)

    if student_id and sem_id and subj_id and teacher_id and classroom_id and grade:
        comm = '''INSERT OR IGNORE INTO Record (student_id, sem_id, subj_id, teacher_id, classroom_id, grade) 
                  VALUES (student_id, sem_id, subj_id, teacher_id, classroom_id, grade)'''.format(student_id, sem_id, subj_id, teacher_id, classroom_id, grade)
        execute(comm)

def findOneVar(table, col, var):
    if table == 'Building' or table == 'Grade' or table == 'Subject':
        comm = '''SELECT id FROM {0} WHERE {1} = '{2}' '''.format(table, col, var)
    elif table == 'Room':
        comm = '''SELECT id FROM Room WHERE room_num = {0} '''.format(var)
    else:
        return
    return getBackData(comm)

def findTwoVar(table, varOne, varTwo):
    if table == 'Student' or table == 'Teacher':
        comm = '''SELECT id FROM {0} WHERE l_name = '{1}' AND f_name = '{2}' '''.format(table, varOne, varTwo)
    elif table == 'Subject':
        comm = '''SELECT id FROM Subject WHERE subj_name = '{0}' AND section = '{1}' '''.format(varOne, varTwo)
    elif table == 'Semester':
        comm = '''SELECT id FROM Semester WHERE sy = {0} AND sem = '{1}' '''.format(varOne, varTwo)
    elif table == 'Classroom':
        varOne = findOneVar('Building', 'bldg_name', varOne)[0][0]
        varTwo = findOneVar('Room', 'room_num', varTwo)[0][0]
        comm = '''SELECT id FROM Classroom WHERE bldg_id = '{0}' AND room_id = {1} '''.format(varOne, varTwo)
    else:
        return
    return getBackData(comm)

def pullDataTwo(table, searchKey, sortOne, sortTwo):
    comm = ''
    sortBy = 'ORDER BY '
    if sortOne != 'None':
        sortBy += 'Semester.sy {0}, Semester.sem {1} '.format(sortOne, sortOne)
        if sortTwo != 'None':
            if table == 'Records':
                sortBy += ', Grade.grade {0} '.format(sortTwo)
            else:
                sortBy += ', Teacher.ln {0},  Teacher.fn {1} '.format(sortTwo, sortTwo)
    else:
        if sortTwo != 'None':
            if table == 'Records':
                sortBy += 'Grade.grade {0} '.format(sortTwo)
            else:
                sortBy += 'Teacher.ln {0},  Teacher.fn {1} '.format(sortTwo, sortTwo)
        else:
            sortBy = ''

    if table == 'Records':
        name = searchKey.split(',')
        id = findTwoVar('Student', name[0].trim(), name[1].trim())[0][0]
        comm = '''SELECT Student.ln, Student.fn, Semester.sy, Semester.sem, Subject.subj_name, Grade.grade
                  FROM Record 
                  JOIN Student ON Student.id = Record.student_id
                  JOIN Semester ON Semester.id = Record.sem_id
                  JOIN Subject ON Subject.id = Record.subject_id
                  JOIN Grade ON Grade.id = Record.grade_id
                  WHERE Record.student_id = {0} {1} '''.format(id, sortBy)
    elif table == 'Subjects':
        id = findOneVar('Subject', 'subj_name', searchKey)[0][0]
        comm = '''SELECT Subject.subj_name, Subject.section, Semester.sy, Semester.sem, Teacher.ln, Teacher.fn, Student.ln, Student.fn
                  FROM Record
                  JOIN Subject ON Subject.id = Record.subject_id
                  JOIN Semester ON Semester.id = Record.sem_id
                  JOIN Teacher ON Teacher.id = Record.teacher_id
                  JOIN Student ON Student.id = Record.student.id
                  WHERE Record.subject_id = {0} {1} '''.format(id, sortBy)
    print(getBackData(comm))

def pullSubjInSem(sy, sem):
    id = findTwoVar('Semester', sy, sem)[0][0]
    comm = '''SELECT DISTINCT Semester.sy, Semester.sem, Subject.subj_name
              FROM Record
              JOIN Semester ON Semester.id = Record.sem_id
              JOIN Subject ON Subject.id = Record.subject_id
              WHERE Record.sem_id = {0} 
              ORDER BY Semester.sy ASC, Semester.sem ASC '''.format(id)
    print (getBackData(comm))

def updateEntry(updateType, sy, sem, subj, sect, varOne, varTwo, varThree):
    sem_id = findTwoVar('Semester', sy, sem)[0][0]
    subj_id = findTwoVar('Subject', subj, sect)[0][0]

    params = 'sem_id = {0} '.format(sem_id)
    subjParam = 'AND subject_id = {0} '.format(subj_id)
    condition = ''
    newVals = ''
    confirm = ''

    if updateType == 'classroom':
        new_room_id = findTwoVar('Classroom', varOne, varTwo)[0][0]
        newVals = 'classroom_id = {0}'.format(new_room_id)
        confirm = params + subjParam + 'AND ' + newVals
    elif updateType == 'teacher':
        new_teacher_id = findTwoVar('Teacher', varOne, varTwo)[0][0]
        newVals = 'teacher_id = {0}'.format(new_teacher_id)
        confirm = params + subjParam + 'AND ' + newVals
    elif updateType == 'grade':
        student_id = findTwoVar('Student', varOne, varTwo)[0][0]
        new_grade_id = findOneVar('Grade', 'grade', varThree)[0][0]
        condition = 'AND student_id = {0} '.format(student_id)
        newVals = 'grade_id = {0} '.format(new_grade_id)
        confirm = params + subjParam + condition + 'AND ' + newVals
    elif updateType == 'section':
        teacher_id = findTwoVar('Teacher', varOne, varTwo)[0][0]
        new_sect_id = findTwoVar('Subject', subj, varThree)[0][0]
        condition = 'AND teacher_id = {0} '.format(teacher_id)
        newVals = 'subject_id = {0} '.format(new_sect_id)
        confirm = params + 'AND' + newVals + condition

    else:
        return

    params += 'subject_id = {0} {1}'.format(subj_id, condition)
    comm = '''IF EXISTS (SELECT DISTINCT * FROM Record WHERE {0})
              UPDATE Record SET ({1})
              WHERE {2}'''.format(params, newVals, params)
    execute(comm)

    confirmComm = '''SELECT * FROM Record WHERE {0} '''.format(confirm)
    print(len(getBackData(confirmComm)))

def delQuery(recordType, sy, sem, varOne, varTwo, varThree):

