import connect_db
from sqlalchemy import func, desc, and_
from models import Group, Student, Subject, Mark, Teacher

session = connect_db.session

def query_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    return session.query(Student.name, func.round(func.avg(Mark.mark_value), 2).label('AvarageMark'))\
                    .select_from(Mark)\
                    .join(Student)\
                    .group_by(Student.id)\
                    .order_by(desc('AvarageMark'))\
                    .limit(5)\
                    .all()

def query_2(subject_name):
    # Знайти студента із найвищим середнім балом з певного предмета.
    return session.query(Student.name, func.round(func.avg(Mark.mark_value), 2).label('AvarageMark'))\
                    .select_from(Mark)\
                    .join(Student)\
                    .join(Subject)\
                    .filter(Subject.name == subject_name)\
                    .group_by(Student.id)\
                    .order_by(desc('AvarageMark'))\
                    .limit(1)\
                    .all()

def query_3(subject_name):
    # Знайти середній бал у групах з певного предмета.
    return session.query(Group.name, func.round(func.avg(Mark.mark_value), 2).label('AvarageMark'))\
                    .select_from(Mark)\
                    .join(Student)\
                    .join(Subject)\
                    .join(Group)\
                    .filter(Subject.name == subject_name)\
                    .group_by(Group.id)\
                    .order_by(desc('AvarageMark'))\
                    .all()

def query_4():
    # Знайти середній бал на потоці (по всій таблиці оцінок).
    return session.query(func.round(func.avg(Mark.mark_value), 2).label('AvarageMark'))\
                    .select_from(Mark)\
                    .all()

def query_5(teacher_name):
    # Знайти які курси читає певний викладач.
    return session.query(Teacher.name, Subject.name)\
                    .select_from(Subject)\
                    .join(Teacher)\
                    .filter(Teacher.name == teacher_name)\
                    .all()

def query_6(group_name):
    # Знайти список студентів у певній групі.
    return session.query(Group.name, Student.name)\
                    .select_from(Student)\
                    .join(Group)\
                    .filter(Group.name == group_name)\
                    .order_by(Student.name)\
                    .all()

def query_7(subject_name, group_name):
    # Знайти оцінки студентів у окремій групі з певного предмета.
    results = session.query(Group.name.label("GroupName"), 
                            Subject.name.label("SubjectName"), 
                            Student.name.label("StudentName"), 
                            Mark.mark_date.label("MarkDate"), 
                            Mark.mark_value.label("MarkValue"))\
                    .select_from(Mark)\
                    .join(Student)\
                    .join(Subject)\
                    .join(Group)\
                    .filter(and_(Subject.name == subject_name, Group.name == group_name))\
                    .order_by(Student.name)\
                    .all()
    
    formatted_results = []
    for result in results:
        formatted_date = result.MarkDate.strftime('%Y-%m-%d')
        formatted_results.append((
            result.GroupName,
            result.SubjectName,
            result.StudentName,
            formatted_date,
            result.MarkValue
        ))

    return formatted_results

def query_8(teacher_name):
    # Знайти середній бал, який ставить певний викладач зі своїх предметів.
    return session.query(Teacher.name, 
                         Subject.name, 
                         func.round(func.avg(Mark.mark_value), 2).label('AvarageMark'))\
                    .select_from(Mark)\
                    .join(Subject)\
                    .join(Teacher)\
                    .filter(Teacher.name == teacher_name)\
                    .group_by(Teacher.name, Subject.name)\
                    .order_by(desc('AvarageMark'))\
                    .all()

def query_9(student_name):
    # Знайти список курсів, які відвідує певний студент.
    return session.query(Subject.name)\
                    .select_from(Mark)\
                    .join(Student)\
                    .join(Subject)\
                    .filter(Student.name == student_name)\
                    .group_by(Subject.name)\
                    .all()

def query_10(student_name, teacher_name):
    # Список курсів, які певному студенту читає певний викладач.
    return session.query(Subject.name)\
                    .select_from(Mark)\
                    .join(Student)\
                    .join(Subject)\
                    .join(Teacher)\
                    .filter(and_(Student.name == student_name, Teacher.name == teacher_name))\
                    .group_by(Subject.name)\
                    .all()

def query_11(student_name, teacher_name):
    # Середній бал, який певний викладач ставить певному студентові.
    return session.query(func.round(func.avg(Mark.mark_value), 2).label('AvarageMark'))\
                    .select_from(Mark)\
                    .join(Student)\
                    .join(Subject)\
                    .join(Teacher)\
                    .filter(and_(Student.name == student_name, Teacher.name == teacher_name))\
                    .all()

def query_12(group_name, subject_name):
    # Оцінки студентів у певній групі з певного предмета на останньому занятті.
    max_date_subquery = session.query(Mark.student_id, 
                                      Mark.subject_id, 
                                      func.max(Mark.mark_date).label('max_mark_date'))\
                                .group_by(Mark.student_id, Mark.subject_id)\
                                .subquery()
    
    results = session.query(Student.name.label("StudentName"), Mark.mark_date, Mark.mark_value)\
                    .select_from(Mark)\
                    .join(Student)\
                    .join(Subject)\
                    .join(Group)\
                    .join(max_date_subquery, and_(Mark.student_id == max_date_subquery.c.student_id,
                                                  Mark.subject_id == max_date_subquery.c.subject_id,
                                                  Mark.mark_date == max_date_subquery.c.max_mark_date))\
                    .filter(and_(Group.name == group_name, Subject.name == subject_name))\
                    .all()
    
    formatted_results = []
    for result in results:
        formatted_date = result.mark_date.strftime('%Y-%m-%d')
        formatted_results.append((
            result.StudentName,
            formatted_date,
            result.mark_value
        ))

    return formatted_results


if __name__ == "__main__":
    print('1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.')
    print(query_1())

    print('2. Знайти студента із найвищим середнім балом з певного предмета.')
    print(query_2("Math"))

    print('3. Знайти середній бал у групах з певного предмета.')
    print(query_3("Math"))

    print('4. Знайти середній бал на потоці (по всій таблиці оцінок).')
    print(query_4())

    print('5. Знайти які курси читає певний викладач.')
    print(query_5("Leslie Hays"))
    
    print('6. Знайти список студентів у певній групі.')
    print(query_6("GR-2"))

    print('7. Знайти оцінки студентів у окремій групі з певного предмета.')
    print(query_7("Chemistry", "GR-1"))

    print('8. Знайти середній бал, який ставить певний викладач зі своїх предметів.')
    print(query_8("Katherine Gardner"))

    print('9. Знайти список курсів, які відвідує певний студент.')
    print(query_9("Mitchell Martin"))

    print('10. Список курсів, які певному студенту читає певний викладач.')
    print(query_10("Linda Bass", "Leslie Hays"))

    print('11. Середній бал, який певний викладач ставить певному студентові.')
    print(query_11("Barry Proctor", "Katherine Gardner"))

    print('12. Оцінки студентів у певній групі з певного предмета на останньому занятті.')
    print(query_12("GR-3", "Biology"))


