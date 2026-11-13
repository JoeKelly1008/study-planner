
from drafter import *
from dataclasses import dataclass
from bakery import assert_equal


@dataclass
class Assignment:
    name: str
    course: str
    due_date: str
    estimated_time: float
    priority: str
    notes: str
    completed: bool


@dataclass
class State:
    assignments: list[Assignment]
    selected_course: str
    selected_priority: str
    student_name: str
    show_completed: bool


def assignment_form_page(state, message):
    content = [
        Header("Add a New Assignment")
    ]

    if message != "":
        content.append(message)

    content.extend([
        "Assignment Name:",
        TextBox("name"),
        "Course Name:",
        TextBox("course"),
        "Due Date (YYYY-MM-DD):",
        TextBox("due_date"),
        "Estimated Time (hours):",
        TextBox("estimated_time", "1.0"),
        "Priority:",
        SelectBox(
            "priority",
            ["High", "Medium", "Low"],
            "Medium"
        ),
        "Assignment Notes:",
        TextArea("notes"),
        Button("Save Assignment", "save_assignment"),
        Button("Home", "index"),
        Button("View All Assignments", "view_assignments")
    ])

    return Page(state, content)


@route
def index(state: State) -> Page:
    total = len(state.assignments)
    completed = 0

    for assignment in state.assignments:
        if assignment.completed:
            completed = completed + 1

    unfinished = total - completed

    content = [
        Header("Student Study Planner"),
        "Welcome, " + state.student_name + "!",
        Header("Assignment Overview"),
        "Total Assignments: " + str(total),
        "Completed Assignments: " + str(completed),
        "Unfinished Assignments: " + str(unfinished),
        Header("Update Your Profile"),
        "Student Name:",
        TextBox("new_student_name", state.student_name),
        Button("Update Name", update_profile),
        Header("Quick Actions"),
        Button("Add Assignment", add_assignment),
        Button("View All Assignments", view_assignments),
        Button("View Completed Assignments", completed_assignments),
        Button("Filter Assignments", filter_page)
    ]

    return Page(state, content)


@route
def add_assignment(state: State) -> Page:
    return assignment_form_page(state, "")


@route
def save_assignment(
    state: State,
    name: str,
    course: str,
    due_date: str,
    estimated_time: float,
    priority: str,
    notes: str
) -> Page:

    if name.strip() == "" or course.strip() == "":
        return assignment_form_page(
            state,
            "Please enter an assignment name and course."
        )

    if due_date.strip() == "":
        return assignment_form_page(
            state,
            "Please enter a due date."
        )

    if (len(due_date) != 10 or
            due_date[4] != "-" or
            due_date[7] != "-" or
            not due_date.replace("-", "").isdigit()):

        return assignment_form_page(
            state,
            "Please enter the date in YYYY-MM-DD format."
        )

    if estimated_time <= 0:
        return assignment_form_page(
            state,
            "Estimated time must be greater than zero."
        )

    new_assignment = Assignment(
        name.strip(),
        course.strip(),
        due_date,
        estimated_time,
        priority,
        notes.strip(),
        False
    )

    state.assignments.append(new_assignment)

    return view_assignments(state)


@route
def view_assignments(state: State) -> Page:
    content = [
        Header("All Assignments")
    ]

    if len(state.assignments) == 0:
        content.append("You currently have no assignments.")

    else:
        index = 0

        for assignment in state.assignments:

            content.append(Header(assignment.name))
            content.append("Course: " + assignment.course)
            content.append("Due Date: " + assignment.due_date)
            content.append(
                "Estimated Time: " +
                str(assignment.estimated_time) + " hours"
            )
            content.append("Priority: " + assignment.priority)

            if assignment.completed:
                content.append("Status: Completed")
            else:
                content.append("Status: Not Completed")

            content.append(
                Button(
                    "View Details",
                    "assignment_details",
                    arguments=[
                        Argument("assignment_index", index)
                    ]
                )
            )

            if not assignment.completed:
                content.append(
                    Button(
                        "Mark Complete",
                        "mark_assignment_complete",
                        arguments=[
                            Argument("assignment_index", index)
                        ]
                    )
                )

            content.append(
                Button(
                    "Delete Assignment",
                    "delete_assignment",
                    arguments=[
                        Argument("assignment_index", index)
                    ]
                )
            )

            content.append(HorizontalRule())

            index = index + 1

    content.append(Button("Add Another Assignment", "add_assignment"))
    content.append(Button("Home", "index"))
    content.append(Button("Completed Assignments", "completed_assignments"))
    content.append(Button("Filter Assignments", "filter_page"))

    return Page(state, content)


@route
def assignment_details(
    state: State,
    assignment_index: int
) -> Page:

    content = [
        Header("Assignment Details")
    ]

    if (assignment_index < 0 or
            assignment_index >= len(state.assignments)):

        content.append("Assignment could not be found.")

    else:
        assignment = state.assignments[assignment_index]

        content.extend([
            "Name: " + assignment.name,
            "Course: " + assignment.course,
            "Due Date: " + assignment.due_date,
            "Estimated Time: " +
            str(assignment.estimated_time) + " hours",
            "Priority: " + assignment.priority,
            "Notes: " + assignment.notes
        ])

        if assignment.completed:
            content.append("Status: Completed")

        else:
            content.append("Status: Not Completed")

            content.append(
                Button(
                    "Mark as Completed",
                    "mark_assignment_complete",
                    arguments=[
                        Argument("assignment_index", assignment_index)
                    ]
                )
            )

        content.append(
            Button(
                "Delete Assignment",
                "delete_assignment",
                arguments=[
                    Argument("assignment_index", assignment_index)
                ]
            )
        )

    content.append(Button("Back to All Assignments", "view_assignments"))
    content.append(Button("Home", "index"))

    return Page(state, content)


@route
def mark_assignment_complete(
    state: State,
    assignment_index: int
) -> Page:

    if (assignment_index >= 0 and
            assignment_index < len(state.assignments)):

        state.assignments[assignment_index].completed = True

    return view_assignments(state)


@route
def delete_assignment(
    state: State,
    assignment_index: int
) -> Page:

    if (assignment_index >= 0 and
            assignment_index < len(state.assignments)):

        state.assignments.pop(assignment_index)

    return view_assignments(state)


@route
def completed_assignments(state: State) -> Page:
    content = [
        Header("Completed Assignments")
    ]

    found_assignment = False
    index = 0

    for assignment in state.assignments:

        if assignment.completed:
            found_assignment = True

            content.append(Header(assignment.name))
            content.append("Course: " + assignment.course)
            content.append("Due Date: " + assignment.due_date)
            content.append("Status: Completed")

            content.append(
                Button(
                    "View Details",
                    "assignment_details",
                    arguments=[
                        Argument("assignment_index", index)
                    ]
                )
            )

            content.append(HorizontalRule())

        index = index + 1

    if not found_assignment:
        content.append(
            "You have not completed any assignments yet."
        )

    content.append(Button("Home", "index"))
    content.append(Button("View All Assignments", "view_assignments"))

    return Page(state, content)


@route
def filter_page(state: State) -> Page:

    courses = ["All"]

    for assignment in state.assignments:
        if assignment.course not in courses:
            courses.append(assignment.course)

    if state.selected_course not in courses:
        state.selected_course = "All"

    content = [
        Header("Filter Assignments"),
        "Choose a Course:",
        SelectBox(
            "course_filter",
            courses,
            state.selected_course
        ),
        "Choose a Priority:",
        SelectBox(
            "priority_filter",
            ["All", "High", "Medium", "Low"],
            state.selected_priority
        ),
        "Include Completed Assignments:",
        CheckBox("include_completed", state.show_completed),
        Button("Apply Filters", "filter_assignments"),
        Button("Home", "index"),
        Button("View All Assignments", "view_assignments")
    ]

    return Page(state, content)


@route
def filter_assignments(
    state: State,
    course_filter: str,
    priority_filter: str,
    include_completed: bool
) -> Page:

    state.selected_course = course_filter
    state.selected_priority = priority_filter
    state.show_completed = include_completed

    content = [
        Header("Filtered Assignments")
    ]

    found_assignment = False
    index = 0

    for assignment in state.assignments:

        course_matches = (
            state.selected_course == "All" or
            assignment.course == state.selected_course
        )

        priority_matches = (
            state.selected_priority == "All" or
            assignment.priority == state.selected_priority
        )

        completion_matches = (
            state.show_completed or
            not assignment.completed
        )

        if (course_matches and
                priority_matches and
                completion_matches):

            found_assignment = True

            content.append(Header(assignment.name))
            content.append("Course: " + assignment.course)
            content.append("Due Date: " + assignment.due_date)
            content.append("Priority: " + assignment.priority)

            if assignment.completed:
                content.append("Status: Completed")
            else:
                content.append("Status: Not Completed")

            content.append(
                Button(
                    "View Details",
                    "assignment_details",
                    arguments=[
                        Argument("assignment_index", index)
                    ]
                )
            )

            content.append(HorizontalRule())

        index = index + 1

    if not found_assignment:
        content.append("No assignments match your selected filters.")

    content.append(Button("Change Filters", "filter_page"))
    content.append(Button("Home", "index"))
    content.append(Button("View All Assignments", "view_assignments"))

    return Page(state, content)



@route
def update_profile(state: State, new_student_name: str) -> Page:
    """
    Updates the student's name.
    """
    if new_student_name.strip() != "":
        state.student_name = new_student_name.strip()

    return index(state)


# Test assignment_form_page

test_state = State([], "All", "All", "Student", True)

result = assignment_form_page(test_state, "")
assert_equal(result is not None, True)

result = assignment_form_page(test_state, "Please enter a name.")
assert_equal(result is not None, True)

assert_equal(len(test_state.assignments), 0)


# Test index

result = index(test_state)
assert_equal(result is not None, True)
assert_equal(test_state.student_name, "Student")

test_state.student_name = "Joey"
result = index(test_state)

assert_equal(test_state.student_name, "Joey")
assert_equal(result is not None, True)


# Test add_assignment

result = add_assignment(test_state)
assert_equal(result is not None, True)
assert_equal(len(test_state.assignments), 0)


# Test save_assignment

test_state = State([], "All", "All", "Student", True)

result = save_assignment(
    test_state, "Math Homework", "Math",
    "2026-11-25", 2.0, "High", "Finish worksheet"
)

assert_equal(len(test_state.assignments), 1)
assert_equal(test_state.assignments[0].name, "Math Homework")
assert_equal(test_state.assignments[0].course, "Math")
assert_equal(test_state.assignments[0].completed, False)

result = save_assignment(
    test_state, "Physics Lab", "Physics",
    "2026-11-26", 3.0, "Low", "Complete lab"
)

assert_equal(len(test_state.assignments), 2)
assert_equal(test_state.assignments[1].name, "Physics Lab")
assert_equal(test_state.assignments[1].priority, "Low")

# Invalid assignment name

empty_state = State([], "All", "All", "Student", True)

result = save_assignment(
    empty_state, "", "Math",
    "2026-11-25", 2.0, "High", ""
)

assert_equal(len(empty_state.assignments), 0)

# Invalid course

result = save_assignment(
    empty_state, "Homework", "",
    "2026-11-25", 2.0, "High", ""
)

assert_equal(len(empty_state.assignments), 0)

# Invalid date

result = save_assignment(
    empty_state, "Homework", "Math",
    "November 25", 2.0, "High", ""
)

assert_equal(len(empty_state.assignments), 0)

# Empty date

result = save_assignment(
    empty_state, "Homework", "Math",
    "", 2.0, "High", ""
)

assert_equal(len(empty_state.assignments), 0)

# Invalid estimated time

result = save_assignment(
    empty_state, "Homework", "Math",
    "2026-11-25", 0, "High", ""
)

assert_equal(len(empty_state.assignments), 0)

result = save_assignment(
    empty_state, "Homework", "Math",
    "2026-11-25", -2.0, "High", ""
)

assert_equal(len(empty_state.assignments), 0)


# Test view_assignments

test_state = State(
    [
        Assignment("Chemistry", "Chemistry", "2026-11-20",
                   2.0, "High", "", False),
        Assignment("Math", "Math", "2026-11-22",
                   1.5, "Medium", "", True)
    ],
    "All", "All", "Student", True
)

result = view_assignments(test_state)

assert_equal(result is not None, True)
assert_equal(len(test_state.assignments), 2)

empty_state = State([], "All", "All", "Student", True)

result = view_assignments(empty_state)

assert_equal(result is not None, True)
assert_equal(len(empty_state.assignments), 0)


# Test assignment_details

result = assignment_details(test_state, 0)

assert_equal(result is not None, True)
assert_equal(test_state.assignments[0].name, "Chemistry")

result = assignment_details(test_state, 1)

assert_equal(result is not None, True)
assert_equal(test_state.assignments[1].name, "Math")

result = assignment_details(test_state, 10)

assert_equal(result is not None, True)

result = assignment_details(test_state, -1)

assert_equal(result is not None, True)


# Test mark_assignment_complete

test_state = State(
    [
        Assignment("Chemistry", "Chemistry", "2026-11-20",
                   2.0, "High", "", False),
        Assignment("Physics", "Physics", "2026-11-22",
                   1.5, "Medium", "", False)
    ],
    "All", "All", "Student", True
)

result = mark_assignment_complete(test_state, 0)

assert_equal(test_state.assignments[0].completed, True)
assert_equal(test_state.assignments[1].completed, False)

result = mark_assignment_complete(test_state, 1)

assert_equal(test_state.assignments[1].completed, True)

result = mark_assignment_complete(test_state, 10)

assert_equal(len(test_state.assignments), 2)


# Test delete_assignment

test_state = State(
    [
        Assignment("Chemistry", "Chemistry", "2026-11-20",
                   2.0, "High", "", False),
        Assignment("Math", "Math", "2026-11-22",
                   1.5, "Medium", "", True),
        Assignment("Physics", "Physics", "2026-11-25",
                   3.0, "Low", "", False)
    ],
    "All", "All", "Student", True
)

result = delete_assignment(test_state, 0)

assert_equal(len(test_state.assignments), 2)
assert_equal(test_state.assignments[0].name, "Math")

result = delete_assignment(test_state, 0)

assert_equal(len(test_state.assignments), 1)
assert_equal(test_state.assignments[0].name, "Physics")

result = delete_assignment(test_state, 10)

assert_equal(len(test_state.assignments), 1)

result = delete_assignment(test_state, -1)

assert_equal(len(test_state.assignments), 1)


# Test completed_assignments

result = completed_assignments(test_state)

assert_equal(result is not None, True)

test_state = State(
    [
        Assignment("Chemistry", "Chemistry", "2026-11-20",
                   2.0, "High", "", True)
    ],
    "All", "All", "Student", True
)

result = completed_assignments(test_state)

assert_equal(result is not None, True)
assert_equal(test_state.assignments[0].completed, True)

empty_state = State([], "All", "All", "Student", True)

result = completed_assignments(empty_state)

assert_equal(result is not None, True)


# Test filter_page

test_state = State(
    [
        Assignment("Chemistry", "Chemistry", "2026-11-20",
                   2.0, "High", "", False),
        Assignment("Math", "Math", "2026-11-22",
                   1.5, "Medium", "", True)
    ],
    "All", "All", "Student", True
)

result = filter_page(test_state)

assert_equal(result is not None, True)
assert_equal(test_state.selected_course, "All")

test_state.selected_course = "Chemistry"

result = filter_page(test_state)

assert_equal(result is not None, True)
assert_equal(test_state.selected_course, "Chemistry")

# Test invalid selected course resets to All

test_state.selected_course = "Biology"

result = filter_page(test_state)

assert_equal(test_state.selected_course, "All")


# Test filter_assignments

test_state = State(
    [
        Assignment("Chemistry", "Chemistry", "2026-11-20",
                   2.0, "High", "", False),
        Assignment("Math", "Math", "2026-11-22",
                   1.5, "Medium", "", True),
        Assignment("Physics", "Physics", "2026-11-25",
                   3.0, "Low", "", False)
    ],
    "All", "All", "Student", True
)

result = filter_assignments(
    test_state, "Chemistry", "High", False
)

assert_equal(test_state.selected_course, "Chemistry")
assert_equal(test_state.selected_priority, "High")
assert_equal(test_state.show_completed, False)
assert_equal(result is not None, True)

result = filter_assignments(
    test_state, "Math", "Medium", True
)

assert_equal(test_state.selected_course, "Math")
assert_equal(test_state.selected_priority, "Medium")
assert_equal(test_state.show_completed, True)

result = filter_assignments(
    test_state, "All", "All", False
)

assert_equal(test_state.selected_course, "All")
assert_equal(test_state.selected_priority, "All")
assert_equal(test_state.show_completed, False)


# Test update_profile

test_state = State([], "All", "All", "Student", True)

result = update_profile(test_state, "Joey")

assert_equal(test_state.student_name, "Joey")
assert_equal(result is not None, True)

result = update_profile(test_state, "Alex")

assert_equal(test_state.student_name, "Alex")

# Empty name should not change the profile

result = update_profile(test_state, "")

assert_equal(test_state.student_name, "Alex")

start_server(
    State(
        [],
        "All",
        "All",
        "Student",
        True
    )
)

