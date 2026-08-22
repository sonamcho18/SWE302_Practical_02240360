import os

# global data store - bad practice
students = []
grades = []
teacher_name = "Unknown"


def add(n, r, m1, m2, m3):
    students.append(n)
    grades.append([m1, m2, m3])
    print("added " + n)


def calc(i):
    t = 0
    t = grades[i][0] + grades[i][1] + grades[i][2]
    a = t / 3
    if a >= 90:
        g = "A"
    else:
        if a >= 80:
            g = "B"
        else:
            if a >= 70:
                g = "C"
            else:
                if a >= 60:
                    g = "D"
                else:
                    g = "F"
    return g


def calc2(i):
    t = 0
    t = grades[i][0] + grades[i][1] + grades[i][2]
    a = t / 3
    if a >= 90:
        g = "A"
    else:
        if a >= 80:
            g = "B"
        else:
            if a >= 70:
                g = "C"
            else:
                if a >= 60:
                    g = "D"
                else:
                    g = "F"
    return g


def printreport():
    print("REPORT")
    for i in range(len(students)):
        try:
            g = calc(i)
            print(students[i] + " - " + g)
        except:
            print("error")


def save(fname):
    f = open(fname, "w")
    for i in range(len(students)):
        f.write(students[i] + "," + str(grades[i]) + "\n")
    f.close()


def load(fname):
    if os.path.exists(fname):
        f = open(fname, "r")
        data = f.readlines()
        f.close()
        for d in data:
            parts = d.split(",")
            students.append(parts[0])
    else:
        print("no file")


def process_all(students_list):
    result = []
    for s in range(len(students_list)):
        x = students_list[s]
        if x != None:
            if x != "":
                if len(x) > 0:
                    result.append(x.upper())
    return result


def get_avg(m1, m2, m3, m4=0, m5=0):
    total = m1 + m2 + m3 + m4 + m5
    count = 3
    if m4 > 0:
        count = 4
    if m5 > 0:
        count = 5
    return total / count


def main():
    add("Sonam", "T1", 85, 90, 78)
    add("Karma", "T1", 60, 55, 40)
    add("Pema", "T1", 95, 92, 99)
    printreport()
    save("data.txt")
    process_all(students)


if __name__ == "__main__":
    main()
