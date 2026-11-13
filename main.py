from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

@dataclass
class Assignment:
    name: str
    course: str
    due_date: str
    estimated_time: float
    priority: str
    completed: bool

@dataclass
class State:
    assignments: list[Assignment]


def priority_rank(priority: str) -> int:
    # Lower number means more urgent
    if priority.lower() == "high":
        return 0
    elif priority.lower() == "medium":
        return 1
    else:
        return 2

def comes_after(first: Assignment, second: Assignment) -> bool:
    # True if first should be placed after second
    if first.due_date != second.due_date:
        return first.due_date > second.due_date
    return priority_rank(first.priority) > priority_rank(second.priority)

def sort_assignments(assignments: list[Assignment]):
    # Sort assignments by due date, then by priority
    for i in range(1, len(assignments)):
        current = assignments[i]
        j = i - 1
        while j >= 0 and comes_after(assignments[j], current):
            assignments[j + 1] = assignments[j]
            j -= 1
        assignments[j + 1] = current

@route
def add_new_assignment(state: State, name: str, course: str,
                       due_date: str, estimated_time: str, priority: str) -> Page:
    # Create a new Assignment
    new_assignment = Assignment(name, course, due_date,
                                float(estimated_time), priority.lower(), False)
    # Add it to the assignments list
    state.assignments.append(new_assignment)
    return index(state)

def complete_assignment(state: State, assignment_number: int):
    # Find the selected assignment
    for i in range(len(state.assignments)):
        if i == assignment_number:
            # Change completed to True
            state.assignments[i].completed = True

def display_assignments(state: State) -> list:
    # Show a message if there are no assignments
    if len(state.assignments) == 0:
        return ["\nYou currently have no assignments."]

    # Sort first so the closest deadlines appear at the top
    sort_assignments(state.assignments)

    display = ["\nYour Assignments:"]
    # Loop through the assignment list
    for i in range(len(state.assignments)):
        assignment = state.assignments[i]
        if assignment.completed:
            status = "Completed"
        else:
            status = "Not completed"
        # Display assignment information
        display.append("\nAssignment " + str(i))
        display.append("\n" + assignment.name + " (" + assignment.course + ")")
        display.append("\nDue: " + assignment.due_date)
        display.append("\nEstimated time: " + str(assignment.estimated_time) + " hours")
        display.append("\nPriority: " + assignment.priority)
        display.append("\nStatus: " + status)
        display.append("\n")
    return display

@route
def index(state: State) -> Page:
    return Page(state, [
        "Student Study Planner",
        "\nWelcome to your study planner!",
    ] + display_assignments(state) + [
        "\nMark an assignment as finished by entering its number:",
        TextBox("assignment_number"),
        Button("Mark Complete", complete_assignment_route),
        "\n",
        Button("Add New Assignment", add_assignment_route)
    ])

@route
def add_assignment_route(state: State) -> Page:
    return Page(state, [
        "Add a New Assignment",
        "\nAssignment name:",
        TextBox("name"),
        "\nCourse name:",
        TextBox("course"),
        "\nDue date (YYYY-MM-DD):",
        TextBox("due_date"),
        "\nEstimated completion time (hours):",
        TextBox("estimated_time"),
        "\nPriority level:",
        SelectBox("priority", ["high", "medium", "low"]),
        "\n",
        Button("Add Assignment", add_new_assignment),
        Button("Back", index)
    ])

@route
def complete_assignment_route(state: State, assignment_number: int) -> Page:
    complete_assignment(state, assignment_number)
    return index(state)


start_server(State([]))
