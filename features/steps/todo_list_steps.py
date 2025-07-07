# features/steps/todo_list_steps.py
import sys
from io import StringIO
from behave import given, when, then
from todo_list import ToDoListManager

# === GIVENs ===


@given('the to-do list is empty')
def step_empty(context):
    context.manager = ToDoListManager(storage_file='test_tasks.json')
    context.manager.clear_tasks()


@given('the to-do list contains tasks')
def step_populate(context):
    context.manager = ToDoListManager(storage_file='test_tasks.json')
    context.manager.clear_tasks()
    for row in context.table:
        title = row['Task']
        desc = row.get('Description', '')
        due_date = row.get('Due date', '')
        priority = row.get('Priority', 'Medium')
        task = context.manager.add_task(title, desc, due_date, priority)
        if row.get('Status', '').lower() == 'completed':
            context.manager.mark_completed(task.id)

# === WHENs ===


@when('the user adds a task "{title}"')
def step_add(context, title):
    context.manager.add_task(title, '', '', 'Medium')


@when('the user lists all tasks')
def step_list_all(context):
    context._old_stdout = sys.stdout
    context._captured = StringIO()
    sys.stdout = context._captured
    context.manager.list_tasks()
    sys.stdout = context._old_stdout


@when('the user marks task "{title}" as completed')
def step_mark_complete(context, title):
    tid = next(t.id for t in context.manager.tasks if t.title == title)
    context.manager.mark_completed(tid)


@when('the user clears the to-do list')
def step_clear(context):
    context.manager.clear_tasks()


@when('the user removes task with ID {tid:d}')
def step_remove_by_id(context, tid):
    context.manager.remove_task(tid)


@when('the user changes the due date of task "{title}" to "{new_date}"')
def step_edit_due_date(context, title, new_date):
    tid = next(t.id for t in context.manager.tasks if t.title == title)
    context.manager.edit_task(tid, due_date=new_date)

# === THENs ===


@then('the to-do list should contain "{title}"')
def step_then_contains(context, title):
    titles = [t.title for t in context.manager.tasks]
    assert title in titles, f"'{title}' no está en la lista: {titles}"


@then('the output should contain')
def step_output_contains(context):
    output = context._captured.getvalue()
    for row in context.table:
        assert row['Task'] in output, (
            f"'{row['Task']}' no está en la salida:\n{output}"
            )


@then('the to-do list should show task "{title}" as completed')
def step_then_completed(context, title):
    task = next(t for t in context.manager.tasks if t.title == title)
    assert task.status.lower() == 'completed'


@then('the to-do list should be empty')
def step_then_empty(context):
    assert len(context.manager.tasks) == 0


@then('the to-do list should not contain "{title}"')
def step_not_contain(context, title):
    titles = [t.title for t in context.manager.tasks]
    assert title not in titles


@then('the task "{title}" should have due date "{expected}"')
def step_then_due_date(context, title, expected):
    task = next(t for t in context.manager.tasks if t.title == title)
    assert task.due_date == expected
