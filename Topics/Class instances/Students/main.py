class Student:
    def __init__(self, name, last_name, birth_year):
        self.name = name
        self.last_name = last_name
        self.birth_year = birth_year
        self.student_id = self.name[0] + self.last_name + self.birth_year


s_name = input()
l_name = input()
b_year = input()
student = Student(s_name, l_name, b_year)
print(student.student_id)
