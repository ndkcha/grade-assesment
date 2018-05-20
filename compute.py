class_details = open("class.txt", "r").read().splitlines()
grade_letters = ["A+", "A", "A-", "B+", "B", "B-", "C"]
marking_components = ["A1", "A2", "PR", "T1", "T2"]
students = dict()


def index_class():
    global students
    for student in class_details:
        s = student.split("|")
        students[s[0]] = s[2] + "," + s[1]


def individual(component_name, in_score):
    max_score = in_score.pop(0)

    print("\n" + component_name + " grades (" + max_score + ")")

    student_ids = []
    names = []
    grades = []
    in_score.sort()

    for score in in_score:
        s = score.split("|")
        id = s[0]
        student_ids.append(id)
        names.append(students[id])
        grades.append(s[1] if len(s) == 2 else "")

    data = list(zip(student_ids, names, grades))

    for i, d in enumerate(data):
        line = ''.join(str(x).ljust(20) for x in d)
        print(line)

    print("\n")


def average(component_name, in_score):
    max_score = in_score.pop(0)
    total = 0.0

    for score in in_score:
        s = score.split("|")
        total += float(s[1]) if len(s) == 2 and len(s[1]) > 0 else 0

    avg = total / len(in_score)
    avg = round(avg, 2)

    print("\n" + component_name + " average: " + str(avg) + "/" + str(max_score) + "\n")


def generate_report(data, pass_fail=50, sort_order="ID"):
    print("\nPass/Fail point: " + str(pass_fail))
    norm_data = normalize_data(data)
    grade_distribution_range = 100 - pass_fail
    grade_range = grade_distribution_range / 7
    grade_range = round(grade_range, 2)

    grades = range(7)
    grades = [100 - (x * grade_range) for x in grades]

    student_ids = []
    student_last_name = []
    student_first_name = []
    student_a1 = []
    student_a2 = []
    student_pr = []
    student_t1 = []
    student_t2 = []
    student_total = []
    student_grade = []

    payload = norm_data if sort_order in marking_components + ["GR", "FL"] else None
    final_order = sort_students(sort_order, payload)

    for student_id in final_order:
        student_name = students[student_id].split(",")
        total, match_a1, match_a2, match_pr, match_t1, match_t2 = calculate_final_total(norm_data, student_id)

        student_ids.append(student_id)
        student_last_name.append(student_name[0])
        student_first_name.append(student_name[1] if len(student_name) > 1 else "")
        student_a1.append(match_a1[0].split("|")[2] if len(match_a1) > 0 else "")
        student_a2.append(match_a2[0].split("|")[2] if len(match_a2) > 0 else "")
        student_pr.append(match_pr[0].split("|")[2] if len(match_pr) > 0 else "")
        student_t1.append(match_t1[0].split("|")[2] if len(match_t1) > 0 else "")
        student_t2.append(match_t2[0].split("|")[2] if len(match_t2) > 0 else "")
        student_total.append(str(total))
        if total < pass_fail:
            student_grade.append("F")
        else:
            grade_index = [g for g in grades if g > total]
            student_grade.append(grade_letters[len(grade_index) - 1])

    titles = ['ID', 'LN', 'FN', 'A1', 'A2', 'PR', 'T1', 'T2', 'GR', 'FL']
    data = [titles] + list(zip(student_ids, student_last_name, student_first_name, student_a1, student_a2, student_pr,
                    student_t1, student_t2, student_total, student_grade))

    for i, d in enumerate(data):
        line = ''.join(str(x).ljust(15) for x in d)
        print(line)

    print("\n")


def calculate_final_total(norm_data, student_id, only_total=False):
    norm_a1, norm_a2, norm_pr, norm_t1, norm_t2 = norm_data
    match_a1 = [s for s in norm_a1 if student_id in s]
    match_a2 = [s for s in norm_a2 if student_id in s]
    match_pr = [s for s in norm_pr if student_id in s]
    match_t1 = [s for s in norm_t1 if student_id in s]
    match_t2 = [s for s in norm_t2 if student_id in s]

    total = 0
    total += float(match_a1[0].split("|")[2]) if len(match_a1) > 0 else 0
    total += float(match_a2[0].split("|")[2]) if len(match_a2) > 0 else 0
    total += float(match_pr[0].split("|")[2]) if len(match_pr) > 0 else 0
    total += float(match_t1[0].split("|")[2]) if len(match_t1) > 0 else 0
    total += float(match_t2[0].split("|")[2]) if len(match_t2) > 0 else 0
    total = round(total, 2)
    if only_total:
        return total
    else:
        return total, match_a1, match_a2, match_pr, match_t1, match_t2


def sort_students(sort_order="ID", sort_column=None):
    if sort_order in marking_components:
        norm_a1, norm_a2, norm_pr, norm_t1, norm_t2 = sort_column
        payload = {
            "A1": norm_a1,
            "A2": norm_a2,
            "PR": norm_pr,
            "T1": norm_t1,
            "T2": norm_t2
        }[sort_order]
    else:
        payload = sort_column
    return {
        "ID": sort_students_by_id,
        "FN": sort_students_by_first_name,
        "LT": sort_students_by_last_name,
        "LN": sort_students_by_last_name,
        "A1": sort_students_by_marking_component,
        "A2": sort_students_by_marking_component,
        "PR": sort_students_by_marking_component,
        "T1": sort_students_by_marking_component,
        "T2": sort_students_by_marking_component,
        "GR": sort_students_by_total,
        "FL": sort_students_by_total
    }[sort_order](payload)


def sort_students_by_id(sort_column):
    student_ids = list(students.keys())
    student_ids = [int(student_id) for student_id in student_ids]
    student_ids.sort()
    student_ids = [str(student_id) for student_id in student_ids]
    final_students = dict()
    for student_id in student_ids:
        final_students[student_id] = students[student_id]
    return final_students


def sort_students_by_first_name(sort_column):
    first_names = list(students.values())
    first_names = [name.split(",")[1] if len(name.split(",")) > 0 else "" for name in first_names]
    first_names.sort()
    final_students = dict()
    for first_name in first_names:
        student_id = [id for id, name in students.items() if name.endswith(first_name)]
        student_id.sort()
        student_id = student_id.pop()
        final_students[student_id] = students[student_id]
    return final_students


def sort_students_by_last_name(sort_column):
    last_names = list(students.values())
    last_names = [name.split(",")[0] for name in last_names if len(name.split(",")) > 0]
    last_names.sort()
    final_students = dict()
    for last_name in last_names:
        student_id = [id for id, name in students.items() if name.startswith(last_name)]
        student_id.sort()
        student_id = student_id.pop()
        final_students[student_id] = students[student_id]
    return final_students


def sort_students_by_marking_component(column_marking_component):
    column_marking_component.pop(0)
    component_grades = [float(component_grade.split("|")[2]) for component_grade in column_marking_component]
    component_grades.sort(reverse=True)
    component_grades = [str(component_grade) for component_grade in component_grades]
    final_students = dict()
    for component_grade in component_grades:
        student_ids = [grade.split("|")[0] for grade in column_marking_component if grade.endswith(component_grade)]
        for student_id in student_ids:
            student_ids.sort()
            final_students[student_id] = students[student_id]
    included_student_ids = list(final_students.keys())
    total_student_ids = list(students.keys())
    remaining_student_ids = [student_id for student_id in total_student_ids if student_id not in included_student_ids]
    for student_id in remaining_student_ids:
        final_students[student_id] = students[student_id]
    return final_students


def sort_students_by_total(norm_data):
    total = []
    for student_id in students:
        total.append(student_id + "|" + str(calculate_final_total(norm_data, student_id, True)))
    total_marks = [total_mark.split("|")[1] for total_mark in total]
    total_marks.sort(reverse=True)
    final_students = dict()
    for total_mark in total_marks:
        student_ids = [t.split("|")[0] for t in total if t.endswith(total_mark)]
        student_ids.sort()
        for student_id in student_ids:
            final_students[student_id] = students[student_id]
    included_student_ids = list(final_students.keys())
    total_student_ids = list(students.keys())
    remaining_student_ids = [student_id for student_id in total_student_ids if student_id not in included_student_ids]
    for student_id in remaining_student_ids:
        final_students[student_id] = students[student_id]
    return final_students


def get_marks(grades):
    g = grades.split("|")
    return float(g[2])


def normalize_data(data):
    data_a1, data_a2, data_pr, data_t1, data_t2 = data
    calc_a1 = calculate_total(data_a1)
    calc_a2 = calculate_total(data_a2)
    calc_pr = calculate_total(data_pr)
    calc_t1 = calculate_total(data_t1)
    calc_t2 = calculate_total(data_t2)

    norm_a1 = evaluate_item(calc_a1, 0.075)
    norm_a2 = evaluate_item(calc_a2, 0.075)
    norm_pr = evaluate_item(calc_pr, 0.25)
    norm_t1 = evaluate_item(calc_t1, 0.3)
    norm_t2 = evaluate_item(calc_t2, 0.3)

    return norm_a1, norm_a2, norm_pr, norm_t1, norm_t2


def evaluate_item(item, multiplier):
    processed_item = []
    max_score = item.pop(0)
    processed_item.append(max_score)
    for grades in item:
        g = grades.split("|")
        if len(g) < 3:
            continue
        normalized = float(g[2]) * multiplier
        normalized = round(normalized, 2)
        c = g[0] + "|" + g[1] + "|" + str(normalized)
        processed_item.append(c)
    return processed_item


def calculate_total(item):
    processed_item = []
    max_score = item.pop(0)
    processed_item.append(max_score)
    for grades in item:
        g = grades.split("|")
        if len(g) < 2 or len(g[1]) == 0:
            continue
        normalized = 100 * float(g[1]) / float(max_score)
        normalized = round(normalized, 2)
        c = grades + "|" + str(normalized)
        processed_item.append(c)
    return processed_item




