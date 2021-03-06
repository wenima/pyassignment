import re
import random
import sys
import doctest
import copy

list_teachers = []
list_students = []
K12 = ['K', '1', '2', '3', '4', '5', '6', '7', '8','9','10','11', '12']

def calc_avg_gpa(list):
    """takes a list of either student names or teacher names and returns the avg GPA.
    """
    if (list):
        avg_gpa = sum(float(item.gpa) for item in list) / len(list)
        return avg_gpa
    else:
        return 'There are no students!'


def gen_grade_levels():
    """generates a dictionary with grade as key and a list of type student
        in that grade
    """
    #define the keys to be used to initalize the dict
    keys = ['K', '1', '2', '3', '4', '5', '6', '7', '8','9','10','11', '12']
    #initalize dict with grades as keys and an empty list as value
    grade_levels = {}
    grade_levels = {key: None for key in keys} #! look into this again more
    print (grade_levels)

def new_student_testcase_setup():
    t = Teacher()
    fav_teacher = random.choice(list_teachers)
    t.name = fav_teacher
    return t

def new_student_testcase_full_full(av_teachers):
    """tests if a new student can enroll as specified
    """
    print('Enrolling one more student:')
    t = new_student_testcase_setup();
    print t
    check_capacity(av_teachers, t.name)

def check_capacity(d, *fav_teacher):
    """checks dictionary *d* for capacity and gets rid of empty key/value pairs. If *fav_teacher* is provided, it will check capacity for that
    *fav_teacher*.If that *fav_teacher* is at max, enroll will be invoked with the grade of the *fav_teacher*
    """

    d = {k: v for k,v in d.iteritems() if v}  # re-bind to non-empty # see README for credit

    if fav_teacher:
        print fav_teacher
        if (fav_teacher.max):
            if not(fav_teacher.grade_level in d.viewkeys()):
                print('Sorry, no enrollment possible!')
            else:
                Student.enroll(d, fav_teacher.grade_level)
        else:
            Student.enroll(d, fav_teacher)


    return d

def random_teacher(av_teachers, g, *grade):
    """takes a list *g* of key values representing grade-levels with available teachers. Then returns
    a randomized teachers. An optional *grade* can be passed in if available.
    """
    random.seed()
    if grade:
        t = random.choice(av_teachers[grade_level])
    else:
        grade_level = random.choice(g)
        t = random.choice(av_teachers[grade_level])
    return t

def set_student_attributes(s, t):
    """takes objects student *s* and teacher *t* to set values on the student object and returns it
    """
    l = len(list_students)+1 #!helper
    s.gpa = random.randint(1, 100)
    s.grade_level = t.grade_level #!not DRY
    s.name = ('Student'+ str(l+1) + '_G_' + str(s.grade_level)) #come up with a better naming
    s.current_teacher = t
    # print('This is the new Student:', s) #comment
    # print(s.current_teacher.name, len(s.current_teacher.students))
    # print('No of students for ', s.current_teacher.name, ' at ', len(s.current_teacher.students))
    return s

def remove_maxed_teacher(s, av_teachers):
    """attempts to remove a teacher who has hit it's limit
    """
    if (s.current_teacher.max): #remove teacher at capacity so he gets eliminated from being randomly chosen to be assigned to a student and make lookups faster
        # print('student added:', s.name, ' attempting to remove because at cap', s.current_teacher.name) #comment
        try:
            av_teachers[grade].remove(s.current_teacher)
            # print('successfully removed:', s.current_teacher)
        except ValueError:
            print ("An error occured while trying to remove the item")

class School(object):
    def __init__(self):
        self.name = 'My cool school'
        self.teachers = []
        self.students = []

    def gen_grade_teacher_dict(self):
        """ build a dictionary with grades K through 12 as keys and a list of teachers in that grade as value
        """
        dict_grade_teacher = {} #dict for grade level to teacher pairing
        for key in K12:
            avail_t = [] #first build a list of teachers at current grade level
            for teacher in list_teachers:
                if key == teacher.grade_level:
                    avail_t.append(teacher) #fill the list which gets initialized again for next iteration in K12
            dict_grade_teacher[key] = avail_t
        return dict_grade_teacher

    def avg_gpa_by_grades(self):
        """Get Average GPA throughout all students in school broken down by grade level
        """

        g = []
        g = list(av_teachers.keys()) #! make DRYer

        results = {}

        for grade in g:
            sum_gpa = 0
            i = 0
            for s in self.students:
                if grade == s.grade_level:
                    print('Name:', s.name + ',GPA:', s.gpa)
                    sum_gpa += s.gpa
                    i += 1
                    avg_gpa = sum_gpa/i
                    results[grade] = avg_gpa
        return results

    def avg_gpa_by_teachers(self, grade_level):
        """Get Average GPA for all teachers broken down by grade
        """
        results = dict()
        if self.teachers != None:
            if grade_level:
                loc_teachers = [t for t in self.teachers if t.grade_level == grade_level]
                # debug
                print('Teachers for grade: {0}'.format(loc_teachers))
            else:
                loc_teachers = self.teachers
            for teacher in loc_teachers:
                avg_gpa = calc_avg_gpa(teacher.students)
                results[teacher] = avg_gpa
            return results
        return results

    def get_count_students(self, *arg):
        """this method, when called without an optional *arg* will return the current number of students. An optional *arg*
            can be passed in to get the count by grade. This optional *arg* could be extended so this function is more generic
        """
        grade_count = {}

        if (arg):
            if arg[0] == 'grade':
                for key in K12:
                    i = 0
                    for s in self.students:     #! need to find a way to make this generic
                        if key == s.grade_level:
                            i += 1
                    grade_count[key]= i #! not very pythonic
                for key in grade_count:
                    print('Grade: ', key, ' Count: ', grade_count[key])
        else:
            if (self.students):
                print('Number of students in school', len(self.students))
            else:
                print('There are no students!')


    def get_count_teachers(self, *arg):
        """this method, when called without an optional *arg* will return the current number of teachers. An optional *arg*
            can be passed in to get the count by grade. This optional *arg* could be extended so this function is more generic
        """
        grade_count = {}

        if (arg):
            if arg[0] == 'grade':
                for key in K12:
                    i = 0
                    for t in self.teachers:     #! need to find a way to make this generic
                        if key == t.grade_level:
                            i += 1
                    grade_count[key]= i #! not very pythonic
                for key in grade_count:
                    print('Grade: ', key, ' Count: ', grade_count[key])
        else:
            if (self.students):
                print('Number of teachers in school', len(self.teachers))
            else:
                print('There are no teachers!')

    def get_avg_gpa_by_teacher(self):

        for item in self.teachers:
            avg_gpa = calc_avg_gpa(item.students)
            if type(avg_gpa) is str: #! is this canonic?
                print('Teacher: ', item.name, ' Avg GPA: N/A (No students assigned to this teacher))')
            else:
                print('Teacher: ', item.name, ' Avg GPA: {0:.2f}'.format(avg_gpa))



    def get_students_sorted_by_grade(self):
        """Get all students sorted ascending by their grade level
        """
        if self.students != None:
            # sort students by grade with lambda function
            self.students.sort(key=lambda x: x.grade_level, reverse=False)
        return self.students

        # To sort the list in place...
        # ut.sort(key=lambda x: x.count, reverse=True)

        # To return a new list, use the sorted() built-in function...
        # newlist = sorted(ut, key=lambda x: x.count, reverse=True)

class Teacher(object):
    """represents a teacher object
        attributes : name, grade_level, students, max.
    """
    def __init__(self): #does this need parameters to hire properly?
        self.name = ''
        self.grade_level = ''
        self.students = []
        self.max = False
        #possible to add an attribute which is a method to calc average gpas?

    def check_students_max(self):
         if len(self.students) == 10:
             self.max =  True

    def __str__(self):
        """To identify the object when printing it
        """
        return self.name, self.grade_level

    def __repr__(self):                 #?do I need this?
        """To identify the object when printing it
        """
        return self.name

    def __eq__(self, other):        #this is needed to tell Python that 2 objects are the same if the name attribute of 2 objects matches
        return self.name == other.name

    def hire(t, *grade):
        """creates a type teacher and if *grade* is provided, will be assigned to a given *grade*, otherwise
        the teacher will be randomly assigned to an element of K12
        """
        l = len(list_teachers)+1 #!helper
        if not grade:
            t.grade_level = random.choice(K12)
            grade = t.grade_level
        else:
            t.grade_level = grade
        t.name = ('Teacher' + str(l) + '_G_' + str(grade)) #come up with cool teacher names, for now
        #it's just a boring number
        list_teachers.append(t)

class Student(object):
    """represens a student object
        atributes: name, gpa, grade_level, current_teacher.
    """
    def __init__(self):
        self.name = ''
        self.gpa = 0
        self.grade_level = 0
        self.current_teacher = None

    def __str__(self):
        """To identify the object when printing it
        """
        return self.name

    def __repr__(self):
        """To identify the object when printing it
        """
        return self.name

    def enroll(s, av_teachers, *arg):
        """Generates a type of student and passes in a dict *av_teachers* of available teachers.
        When enrolling a single student, an optional parameter can be passed in. This *arg* is assigned by
        another function which checked, if this student could be enrolled with a specific_teacher. If that teacher
        still has capacity, the teacher's name is passed in. If he is at max, a random teacher of
        that *grade* is assigned. If there is no teacher with any capacity at this grade level, the student is denied
        and should receive a message.
        """
        #check for capacity
        # print(av_teachers) #comment
        av_teachers = check_capacity(av_teachers)
        # print(av_teachers) #comment


        if not(check_capacity(av_teachers)):
            if arg:
                print('Sorry kid, no further enrollment possible')
                quit()
            else:
                return

        g = []
        g = list(av_teachers.keys())
        # possibly optimize this with unpacking args correctly if passed in as a tuple (if I knew how...)
        if arg:
            if arg in g:
                s.grade_level = arg #teacher was at max, grade_level of original teacher set
                t = random_teacher(av_teachers, g, arg)
            else:
                t = arg #logic for when student is assigned a specific teacher
        else:
        #randomly assign a teacher
            t = random_teacher(av_teachers, g)
        set_student_attributes(s, t)
        t.students.append(s)
        t.check_students_max()
        return s

class InteractionManager:
    """use to manage the communication with user in console
    """

    def __init__(self, args):
        self.setup_school()
        self.arg_val = None
        self.init_from_args(args)
        self.show_menu()



    def setup_school(self):
        """Setup the school inital
        """

        self.school = School()
        # setting up the initial faculty
        random.seed()
        num_teachers = random.randint(0, 12)
        print('num_teachers:', num_teachers) #comment
            # print('No Teachers'
        for i in range(num_teachers):
            t = Teacher();
            t.hire()
        self.school.teachers = list_teachers

        #if no teachers have arrived, there are no students
        if len(list_teachers) < 1:
            self.school.students = []
        else:
            av_teachers = self.school.gen_grade_teacher_dict()
            student_enrollment_number = random.randint(82, 100)
            print(student_enrollment_number)
            for i in range(student_enrollment_number): #largest HS in USA has 8076 #!more in readme
                s = Student()
                s = s.enroll(av_teachers)
                try:
                    list_students.append(s)
                    remove_maxed_teacher(s, av_teachers)
                except Exception as e:
                    break;
            print('Enrollment completed')
            self.school.students = list_students
            # self.grade_levels = self.gen_grade_levels()
            # new_student_testcase_full_full(av_teachers)
            print('Current size of faculty is: ', len(self.school.teachers))
            print('Hiring new teacher with no grade assigned:....')
            t = Teacher()
            t.hire()
            self.school.teachers.append(t)
            print('Teacher: ', t.name, ', hired for Grade: ', t.grade_level)
            print('New size of faculty is: ', len(self.school.teachers))
            print('Current size of faculty is: ', len(self.school.teachers))
            print('Hiring a new teacher to work in Grade 12:.....')
            grade_level = '12'
            t_for_12= Teacher()
            t_for_12.hire(grade_level)
            print('Teacher: ', t_for_12.name, ', hired for Grade: ', t_for_12.grade_level)
            print('New size of faculty is: ', len(self.school.teachers))
            self.school.teachers.append(t)
        self.output_startup()




    def init_from_args(self, args):
        """Initialize from arguments when running from command line
        """
        if len(args) > 1 and args[1]:
            self.arg_val = args[1]
            try:
                opt = int(self.arg_val)
                self.run_option(opt)
                # im.show_menu()
            except ValueError:
                # not an integer, so it must be roll_call or wrong argument
                if self.arg_val == 'roll_call':
                    self.run_roll_call(True)

    def output_startup(self):
        """Output the key information of the generated school. Handles edge cases where no teachers have been
            generated so no school can start up and handles the case where not enough students are available
            for enrollment
        """
        print('School "{0}" generated'.format(self.school.name))
        print('{0} Teachers and {1} students'.format(len(self.school.teachers), len(self.school.students)))
        #! todo check for type and return based on that
        print('Average GPA throughout the school: {0:.2f}'.format(calc_avg_gpa(self.school.students)))
        print('Students:')
        self.school.get_count_students('grade')
        print('Teachers:')
        self.school.get_count_teachers('grade')
        print('avg gpa by teacher:')
        self.school.get_avg_gpa_by_teacher()


    def new_student_testcase_full_free():
        """tests if a new student can enroll as specified
        """
        print('Trying again, one student dropped out')
        g = []
        g = list(av_teachers.keys()) #! see if it can be put into the function directly
        t = new_student_testcase_setup();
        t_same_grade = random_teacher(av_teachers, g, t.grade_level)
        print(t_same_grade.students)
        t_same_grade.students.remove[0]
        check_capacity(av_teachers, t.grade_level)
        print(t_same_grade.students)

    def run_roll_call(self, comma_list=False):
        """Output all students sorted ascending by their grade level and exit.
        Only called from command line
        The parameter is optional and determines the output format.
        """
        students = self.school.get_students_sorted_by_grade()
        last_grade = 0
        if comma_list == True:
            list_grades = list(set([s.grade_level for s in self.school.students]))
            for grade in list_grades:
                print('Grade {0}:\n{1}'.format(grade, ', '.join([s.name for s in students if s.grade_level == grade])))
        else:
            for stud in students:
                if stud.grade_level != last_grade:
                    last_grade = int(stud.grade_level)
                    print('Grade {0}: '.format(last_grade))
                    print('{0}'.format(stud.name))
        print('goodbye')
        gen_grade_levels()
        sys.exit()

    def run_option(self, opt):
        """Run the selected option from menu
        """
        if int(opt) == 1:
            avg_grades = self.school.avg_gpa_by_grades()
            for grade, avg in avg_grades.items():
                print('Average GPA in Grade {0} is: {1:.2f}'.format(grade, avg))
        elif int(opt) == 2:
            w_grade = self.get_input('Enter grade for report (1-12): ')
            avg_by_teacher = self.school.avg_gpa_by_teachers(int(w_grade))
            if len(avg_by_teacher) == 0:
                print('There are no teachers!')
            else:
                for teacher, avg in avg_by_teacher.items():
                    print('Average GPA for {0}: {1:.2f}'.format(teacher.name, avg))

        elif int(opt) == 3:
            if self.arg_val != None and self.arg_val:
                # for debugging purposes
                # print(self.arg_val)
                print('Valid options via parameter are [1] or [2] or "roll_call"!')
                print('goodbye')
                sys.exit()
            else:
                # use list to identify valid input for cancelling the exit
                list_stay = ['no', 'n']
                answer = self.get_input('Do you really want to exit? (yes/no): ').lower()
                if answer not in list_stay:
                    print('goodbye')
                    sys.exit()
        else:
            print('{0} is no valid menu option!'.format(opt))

    def show_menu(self):
        # reset the args from first run if there were any:
        self.arg_val = None
        print('\tMenu\n[1]\tGPA per grade level\n[2]\tAverage GPA perteacher per grade\n[3]\tExit')
        option = self.get_input('Choose an option: ')
        try:
            chosen_opt = int(option)
            # for debugging purposes
            # print('You chose: {0}'.format(chosen_opt))
            self.run_option(chosen_opt)
        except ValueError:
            print('Valid options are only the numbers [1], [2] or [3]!')

        self.show_menu()

    def get_input(self, caption):
        return input(caption)



# doctest.testmod()
im = InteractionManager(sys.argv)
