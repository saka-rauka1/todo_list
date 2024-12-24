import os
from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


# Create Form
class TaskForm(FlaskForm):
    task = StringField("New Task", validators=[DataRequired(), Length(max=250)])
    submit = SubmitField("Add Task")


# Initialize app
app = Flask(__name__)
app.secret_key = os.environ.get("secret_key")
bootstrap = Bootstrap5(app)

# todo Store tasks in sql database
# Create task list
tasks = ["Example Task 1", "Example Task2"]


# Create routes
@app.route("/", methods=["GET", "POST"])
def index():
    form = TaskForm()
    # Handle form submission
    if form.validate_on_submit():
        # Add task to task list
        tasks.append(form.task.data)

    return render_template("index.html", form=form, tasks=tasks)


@app.route("/delete", methods=["POST"])
def delete():
    deleted_tasks = request.form.getlist("task-check")

    # Create a list of indices to remove from task list
    indices_to_remove = []
    for task in deleted_tasks:
        indices_to_remove.append(int(task))

    # Remove tasks from task list by indices
    global tasks
    tasks = [item for i, item in enumerate(tasks) if i not in set(indices_to_remove)]

    return redirect("/")


# todo Change to an ordered list and allow drag and drop to change order
# todo Decouple checking tasks and deleting them
# todo Increase character limit
# todo Can implement the delete tasks form as a flask-wtform

if __name__ == '__main__':
    app.run(debug=True)
