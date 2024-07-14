from datetime import datetime
import faker
from random import randint, choice
import sqlite3
from models import groups, students, subjects, marks, teachers

NUMBER_STUDENTS = 30
NUMBER_GROUPS = 3
NUMBER_SUBJECTS = 5
NUMBER_TEACHERS = 5
NUMBER_MARKS = 20

def generate_fake_data(number_students, number_teachers) -> tuple():
    fake_students = []  
    fake_teachers = [] 
    
    fake_data = faker.Faker()

    for _ in range(number_students):
        fake_students.append(fake_data.name())

    for _ in range(number_teachers):
        fake_teachers.append(fake_data.name())

    return fake_students, fake_teachers


def prepare_data(students, teachers) -> tuple():
    for_groups = [('GR-1',), ('GR-2',), ('GR-3',)]
    
    for_students = []    
    for student in students:
        for_students.append((student, randint(1, NUMBER_GROUPS)))

    for_teachers = []
    for teacher in teachers:
        for_teachers.append((teacher, ))

    for_subjects = []    
    for_subjects.append(('Math', randint(1, NUMBER_TEACHERS)))    
    for_subjects.append(('Physics', randint(1, NUMBER_TEACHERS))) 
    for_subjects.append(('Chemistry', randint(1, NUMBER_TEACHERS))) 
    for_subjects.append(('Biology', randint(1, NUMBER_TEACHERS))) 
    for_subjects.append(('English', randint(1, NUMBER_TEACHERS))) 

    for_marks = []
    for _ in range(NUMBER_STUDENTS):
        for _ in range(NUMBER_SUBJECTS):
            for _ in range(NUMBER_MARKS):
                mark_date = datetime(2024, randint(1, 5), randint(1, 28)).date() 
                for_marks.append((randint(1, NUMBER_STUDENTS), randint(1, NUMBER_SUBJECTS), randint(1, 5), mark_date))

    return for_groups, for_students, for_teachers, for_subjects, for_marks


#def insert_data_to_db(groups, students, teachers, subjects, marks) -> None:


#def insert_data_to_db(groups, students, teachers, subjects, marks) -> None:
#    with sqlite3.connect('University.sqlite') as con:
#
#        cur = con.cursor()
#        try:
#            cur.execute("DELETE FROM Groups")       
#            cur.execute("DELETE FROM sqlite_sequence WHERE name='Groups'")
#
#            cur.execute("DELETE FROM Students")        
#            cur.execute("DELETE FROM sqlite_sequence WHERE name='Students'")
#
#            cur.execute("DELETE FROM Teachers")        
#            cur.execute("DELETE FROM sqlite_sequence WHERE name='Teachers'")
#
#            cur.execute("DELETE FROM Subjects")        
#            cur.execute("DELETE FROM sqlite_sequence WHERE name='Subjects'")
#
#            cur.execute("DELETE FROM Marks")
#            cur.execute("DELETE FROM sqlite_sequence WHERE name='Marks'")
#
#           con.commit()
#        
#
#           sql_to_groups = """INSERT INTO Groups(GroupName)
#                            VALUES (?)"""
#            cur.executemany(sql_to_groups, groups)
#            
#            sql_to_students = """INSERT INTO Students(StudentName, GroupID)
#                                VALUES (?, ?)"""
#            cur.executemany(sql_to_students, students)
#            
#            sql_to_teachers = """INSERT INTO Teachers(TeacherName)
#                                VALUES (?)"""
#            cur.executemany(sql_to_teachers, teachers)
#            
#            sql_to_subjects = """INSERT INTO Subjects(SubjectName, TeacherID)
#                                VALUES (?, ?)"""
#            cur.executemany(sql_to_subjects, subjects)        
#            
#            sql_to_marks = """INSERT INTO Marks(StudentID, SubjectID, MarkValue, MarkDate)
#                            VALUES (?, ?, ?, ?)"""
#            cur.executemany(sql_to_marks, marks)        
#            
#            con.commit()
#        
#        except:
#            pass
#        finally:
#            cur.close()


if __name__ == "__main__":
    groups, students, teachers, subjects, marks = prepare_data(*generate_fake_data(NUMBER_STUDENTS, NUMBER_TEACHERS))
    insert_data_to_db(groups, students, teachers, subjects, marks)