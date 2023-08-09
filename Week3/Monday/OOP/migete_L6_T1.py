class SchoolMember:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Teacher(SchoolMember):
    def __init__(self, name, age, salary):
        super().__init__(name, age)
        self.salary = salary
        self.coursesList = {}

    def getSalary(self):
        return self.salary

    def addCourse(self, signature, name):
        self.coursesList[signature] = name

    def getCourses(self):
        for key, value in self.coursesList.items():
            print(f'{key} {value}') #?????


class Student(SchoolMember):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.courses = {}

    def attendCourse(self, signature, year):
        self.courses[signature] = {'grades' : [], 'year' : year}

    def addGrade(self, signature, grade):
        if signature in self.courses.keys():
            self.courses[signature]['grades'].append(grade)

    def getCourses(self):
        for key, value in self.courses.items():
            print(f'{key} {value}')

    def getAvgGrade(self, signature):
        sum = 0
        for grade in self.courses[signature]['grades']:
            sum     += grade

        return  sum / len(self.courses[signature]['grades'])