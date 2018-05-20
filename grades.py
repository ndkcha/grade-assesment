import compute

file_choices = {
    "A1": "a1.txt",
    "A2": "a2.txt",
    "PR": "project.txt",
    "T1": "test1.txt",
    "T2": "test2.txt",
}

sort_choices = ["ID", "LN", "LT", "FN", "A1", "A2", "PR", "T1", "T2", "GR", "FL"]


def open_component_file():
    print("Which component do you want to see?")
    component = input("Enter one of these A1|A2|PR|T1|T2: ").upper()
    while component not in file_choices:
        print("Please enter amongst these options: A1|A2|PR|T1|T2")
        component = input("Which component do you want to see?: ").upper()
    filename = file_choices[component]
    file = open(filename, "r+")
    data = file.read().splitlines()
    file.close()
    return data, component


def open_all_files():
    file_a1 = open(file_choices["A1"])
    file_a2 = open(file_choices["A2"])
    file_pr = open(file_choices["PR"])
    file_t1 = open(file_choices["T1"])
    file_t2 = open(file_choices["T2"])

    data_a1 = file_a1.read().splitlines()
    data_a2 = file_a2.read().splitlines()
    data_pr = file_pr.read().splitlines()
    data_t1 = file_t1.read().splitlines()
    data_t2 = file_t2.read().splitlines()

    file_a1.close()
    file_a2.close()
    file_pr.close()
    file_t1.close()
    file_t2.close()

    return data_a1, data_a2, data_pr, data_t1, data_t2


def display_individual_component():
    data, component = open_component_file()
    compute.individual(component, data)


def display_average_component():
    data, component = open_component_file()
    compute.average(component, data)


def display_report():
    compute.generate_report(open_all_files())


def sort_report():
    print("What column do you want to sort?")
    sort_order = input("Enter one of these ID|LN|LT|FN|A1|A2|PR|T1|T2|GR|FL: ").upper()
    while sort_order not in sort_choices:
        print("Please enter amongst these options: ID|LN|LT|FN|A1|A2|PR|T1|T2|GR|FL")
        sort_order = input("Which component do you want to see?: ").upper()
    compute.generate_report(open_all_files(), sort_order=sort_order)


def change_pass_fail():
    pass_fail_point = input("What is the pass/fail point?: ")
    compute.generate_report(open_all_files(), pass_fail=int(pass_fail_point))


def say_bye():
    print("Good Bye")
    exit()


def execute_action(choice):
    return {
        "1": display_individual_component,
        "2": display_average_component,
        "3": display_report,
        "4": sort_report,
        "5": change_pass_fail,
        "6": say_bye
    }[choice]()


def display_menu():
    compute.index_class()
    while True:
        print("1. Display individual component\n2. Display component average\n3. Display standard report")
        print("4. Sort by alternate column\n5. Change Pass/Fail point\n6. Exit")
        choice = input("What do you want to go for? (Enter the number): ")
        if int(choice) not in range(1, 7):
            print("\nPlease enter the valid choice\n")
            continue
        execute_action(choice)


if __name__ == "__main__":
    display_menu()