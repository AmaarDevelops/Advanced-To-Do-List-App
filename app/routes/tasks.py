from flask import Blueprint,redirect,url_for,session,render_template,flash,request
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks',__name__)
@tasks_bp.route('/')

#Function for viewing tasks
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    tasks = Task.query.all()
    return render_template('tasks.html',tasks = tasks)


#Function for Addding tasks
@tasks_bp.route("/add",methods=["POST"])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    title = request.form.get('title')
    if title:
        new_task = Task(title = title,status ='Pending')
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully')
    return redirect(url_for('tasks.view_tasks'))

#Changin the status of the task
@tasks_bp.route("/toggle/<int:task_id>",methods=["POST"])
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task:
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Done'  
        else:
            task.status = 'Pending'
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))  

#Clearing all the tasks
@tasks_bp.route("/clear",methods = ["POST"])
def clear_task():
    Task.query.delete()
    db.session.commit()
    flash('All Tasks Cleared!','info')
    return redirect(url_for('tasks.view_tasks'))

#Delete one task at a time
@tasks_bp.route("/delete/<int:task_id>",methods=["POST"])
def delete_task(task_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task was deleted successfully','info')
    else:
        flash('Task not found','error')

    return redirect(url_for('tasks.view_tasks'))
        








