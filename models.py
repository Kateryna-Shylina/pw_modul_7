from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()

groups = Table('groups', Base.metadata,
        Column('GroupID', Integer, primary_key=True),
        Column('GroupName', String),
    )

students = Table('students', Base.metadata,
    Column('StudentID', Integer, primary_key=True),
    Column('StudentName', String),
    Column('GroupID', Integer, ForeignKey('groups.GroupID')),
)

teachers = Table('teachers', Base.metadata,
    Column('TeacherID', Integer, primary_key=True),
    Column('TeacherName', String),
)

subjects = Table('subjects', Base.metadata,
    Column('SubjectID', Integer, primary_key=True),
    Column('SubjectName', String),
    Column('TeacherID', Integer, ForeignKey('teachers.TeacherID')),
)

marks = Table('marks', Base.metadata,
    Column('MarkID', Integer, primary_key=True),
    Column('StudentID', Integer, ForeignKey('students.StudentID')),
    Column('SubjectID', Integer, ForeignKey('subjects.SubjectID')),
    Column('MarkValue', Integer),
    Column('MarkDate', String),
)