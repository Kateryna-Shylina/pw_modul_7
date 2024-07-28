from datetime import datetime
import faker
from random import randint, choice
import sqlite3
from models import Group, Student, Subject, Mark, Teacher
from sqlalchemy import create_engine, Integer, String, ForeignKey, select, Text, and_, desc, func
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column, relationship
import connect_db 

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


def insert_data_to_db(groups, students, teachers, subjects, marks) -> None:
    session = connect_db.session

    session.query(Group).delete()
    session.commit()
    session.query(Student).delete()
    session.commit()
    session.query(Teacher).delete()
    session.commit()
    session.query(Subject).delete()
    session.commit()
    session.query(Mark).delete()
    session.commit()

    for group_list in groups:
        group_name = group_list[0]
        group = Group(name = group_name)
        session.add(group)
    session.commit()

    for student_list in students:
        student_name = student_list[0]
        group_id = student_list[1]
        student = Student(name = student_name, group_id = group_id)
        session.add(student)
    session.commit()

    for teacher_list in teachers:
        teacher_name = teacher_list[0]
        teacher = Teacher(name = teacher_name)
        session.add(teacher)
    session.commit()

    for subject_list in subjects:
        subject_name = subject_list[0]
        teacher_id = subject_list[1]
        subject = Subject(name = subject_name, teacher_id = teacher_id)
        session.add(subject)
    session.commit()

    for mark_list in marks:
        student_id = mark_list[0]
        subject_id = mark_list[1]
        mark_value = mark_list[2]
        mark_date = mark_list[3]
        mark = Mark(student_id = student_id,
                    subject_id = subject_id,
                    mark_value = mark_value,
                    mark_date = mark_date)
        session.add(mark)
    session.commit()


if __name__ == "__main__":
    groups, students, teachers, subjects, marks = prepare_data(*generate_fake_data(NUMBER_STUDENTS, NUMBER_TEACHERS))
    insert_data_to_db(groups, students, teachers, subjects, marks)