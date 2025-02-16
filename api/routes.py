from flask import Blueprint, request, jsonify
import asyncio
from services import add_task, get_task_status, get_all_tasks, get_task_by_id, execute_task_by_id, execute_all_tasks, query_tiny_agent

tinyagent_bp = Blueprint('tinyagent', __name__)

@tinyagent_bp.route('/test', methods=['GET'])
def test():
    """
    Test route to trigger TinyAgent asynchronously.
    """
    query_text = "Create a meeting with Sid and Lutfi for tomorrow 2pm to discuss the meeting notes."
    
    response = asyncio.run(query_tiny_agent(query_text))
    return jsonify({"response": response})

# Get all tasks of the day
@tinyagent_bp.route('/tasks/all', methods=['GET'])
def get_tasks():
    """
    Retrieve all tasks.
    """
    tasks = get_all_tasks()
    return jsonify({"tasks": tasks})

# Get a specific task by ID
@tinyagent_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """
    Retrieve a specific task by its ID.
    """
    task = get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)

# Execute all tasks asynchronously
@tinyagent_bp.route('/tasks/execute', methods=['POST'])
def execute_tasks():
    """
    Execute all pending tasks.
    """
    statuses = asyncio.run(execute_all_tasks())
    return jsonify({"statuses": statuses})

# Execute a specific task by ID
@tinyagent_bp.route('/tasks/execute/<task_id>', methods=['POST'])
def execute_task(task_id):
    """
    Execute a specific task.
    """
    status = asyncio.run(execute_task_by_id(task_id))
    if not status:
        return jsonify({"error": "Task not found or already executed"}), 404
    return jsonify({"status": status})

# Add task to queue
@tinyagent_bp.route('/tasks/submit', methods=['POST'])
def submit_task():
    """
    Submit a task to the queue for TinyAgent to process.
    """
    data = request.json
    query_text = data.get("query", "")

    if not query_text:
        return jsonify({"error": "Query is required"}), 400

    task_id = add_task(query_text)
    return jsonify({"task_id": task_id, "status": "pending"})
