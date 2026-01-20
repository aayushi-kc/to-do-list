from flask import Flask, request, redirect
import json
import os

app = Flask(__name__)

# File to store tasks
TASKS_FILE = 'tasks.json'

def load_tasks():
    """Load tasks from file"""
    try:
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return []

def save_tasks(tasks):
    """Save tasks to file"""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)

def render_tasks(tasks):
    """Render tasks as HTML"""
    if not tasks:
        return '''
        <div class="empty-state">
            <div>📭</div>
            <h3>No tasks yet!</h3>
            <p>Add your first task above.</p>
        </div>
        '''

    html_parts = []
    for i, task in enumerate(tasks):
        task_id = i
        task_text = task.get('task', '')
        is_done = task.get('done', False)

        task_html = f'''
        <div class="task-item {'done' if is_done else ''}">
            <span style="font-size: 1.2em;">{"✅" if is_done else "◻️"}</span>
            <span class="task-text {'done-text' if is_done else ''}">{task_text}</span>
            <div class="task-actions">
        '''

        if not is_done:
            task_html += f'''
                <button onclick="location.href='/toggle/{task_id}'" class="action-btn done-btn">
                    Done
                </button>
            '''

        task_html += f'''
                <button onclick="confirmDelete({task_id})" class="action-btn delete-btn">
                    Delete
                </button>
            </div>
        </div>
        '''

        html_parts.append(task_html)

    return ''.join(html_parts)

@app.route('/')
def index():
    """Home page - shows the todo list"""
    tasks = load_tasks()
    done_count = sum(1 for t in tasks if t.get('done'))
    pending_count = sum(1 for t in tasks if not t.get('done'))

    # Using double quotes for outer string to avoid f-string quote conflict
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>📝 To-Do List | Replit</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}

            body {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}

            .container {{
                background: white;
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.2);
                width: 100%;
                max-width: 500px;
            }}

            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}

            h1 {{
                color: #333;
                font-size: 2.5em;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 15px;
            }}

            .task-form {{
                display: flex;
                gap: 10px;
                margin-bottom: 25px;
            }}

            .task-input {{
                flex: 1;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 1em;
            }}

            .task-input:focus {{
                outline: none;
                border-color: #667eea;
            }}

            .add-btn {{
                background: #667eea;
                color: white;
                border: none;
                padding: 15px 25px;
                border-radius: 10px;
                cursor: pointer;
                font-weight: bold;
                transition: background 0.3s;
            }}

            .add-btn:hover {{
                background: #764ba2;
            }}

            .tasks-list {{
                margin-top: 20px;
            }}

            .task-item {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 10px;
                margin-bottom: 10px;
                border-left: 5px solid #667eea;
            }}

            .task-item.done {{
                opacity: 0.7;
                border-left-color: #6bcf7f;
            }}

            .task-text {{
                flex: 1;
                margin-left: 15px;
                font-size: 1.1em;
            }}

            .task-text.done-text {{
                text-decoration: line-through;
                color: #666;
            }}

            .task-actions {{
                display: flex;
                gap: 10px;
            }}

            .action-btn {{
                padding: 8px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                transition: transform 0.2s;
            }}

            .action-btn:hover {{
                transform: scale(1.05);
            }}

            .done-btn {{
                background: #6bcf7f;
                color: white;
            }}

            .delete-btn {{
                background: #ff6b6b;
                color: white;
            }}

            .empty-state {{
                text-align: center;
                padding: 40px;
                color: #666;
            }}

            .stats {{
                text-align: center;
                margin-top: 20px;
                color: #666;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 10px;
            }}

            .action-buttons {{
                display: flex;
                gap: 10px;
                margin-top: 20px;
                justify-content: center;
            }}

            .clear-btn {{
                background: #ffd93d;
                color: #333;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>
                    <span>📝</span>
                    To-Do List
                    <span>📝</span>
                </h1>
                <p style="color: #666;">Add, complete, and manage your tasks</p>
            </div>

            <form method="POST" action="/add" class="task-form">
                <input type="text" name="task" class="task-input" placeholder="Enter a new task..." required>
                <button type="submit" class="add-btn">Add Task</button>
            </form>

            <div class="tasks-list">
                {render_tasks(tasks)}
            </div>

            <div class="stats">
                <strong>📊 Stats:</strong> 
                {len(tasks)} total tasks | 
                {done_count} completed | 
                {pending_count} pending
            </div>

            <div class="action-buttons">
                <button onclick="location.href='/clear_done'" class="clear-btn">
                    🗑️ Clear Completed
                </button>
                <button onclick="if(confirm('Delete all tasks?')) location.href='/clear'" class="clear-btn" style="background: #ff6b6b; color: white;">
                    🗑️ Clear All
                </button>
            </div>
        </div>

        <script>
            function confirmDelete(taskId) {{
                if (confirm('Are you sure you want to delete this task?')) {{
                    window.location.href = '/delete/' + taskId;
                }}
            }}

            // Auto-focus the input field
            document.addEventListener('DOMContentLoaded', function() {{
                document.querySelector('.task-input').focus();
            }});
        </script>
    </body>
    </html>
    """

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task"""
    task_text = request.form.get('task', '').strip()
    if task_text:
        tasks = load_tasks()
        tasks.append({"task": task_text, "done": False})
        save_tasks(tasks)
    return redirect('/')

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    """Toggle task completion status"""
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id]['done']
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Delete a task"""
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect('/')

@app.route('/clear')
def clear_tasks():
    """Clear all tasks"""
    save_tasks([])
    return redirect('/')

@app.route('/clear_done')
def clear_done_tasks():
    """Clear completed tasks"""
    tasks = load_tasks()
    tasks = [t for t in tasks if not t.get('done')]
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)