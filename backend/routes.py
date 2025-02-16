from flask import Blueprint, request, jsonify
import asyncio
from datetime import datetime
from .services import query_tiny_agent
from .task_queue import add_task, get_task_status, get_all_tasks, task_status

tinyagent_bp = Blueprint('tinyagent', __name__)

@tinyagent_bp.route('/test', methods=['GET'])
def test():
    """Test route to trigger TinyAgent asynchronously."""
    query_text = "Create a meeting with Richard Chao for tomorrow 2pm to discuss the meeting notes."
    response = asyncio.run(query_tiny_agent(query_text))
    return jsonify({"response": response})

@tinyagent_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks and their statuses."""
    tasks_data = get_all_tasks()
    tasks_list = {
        task_id: {
            "task_id": task_id,
            "task_description": task_info.get("task_description", ""),
            "result": task_info.get("response", ""),
            "status": task_info["status"],
            "date": task_info.get("date", ""),
            "started_at": task_info.get("started_at"),
            "completed_at": task_info.get("completed_at"),
            "error_message": task_info.get("error_message")
        }
        for task_id, task_info in tasks_data.items()
    }
    return jsonify({"tasks": tasks_list})

@tinyagent_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Retrieve a specific task by its ID with detailed information."""
    task = get_task_status(task_id)
    if task == "not found":
        return jsonify({"error": f"Task not found, task id: {task_id}. Task Status: {task_status}; Args: {request.view_args}; URL: {request.url}"}), 404
    
    # Convert task object to dictionary if it's not already
    if not isinstance(task, dict):
        task = task.__dict__

    # Enhance the task data with additional details
    enhanced_task = {
        "task_id": task_id,
        "task_description": task.get("task_description", ""),
        "status": task.get("status", "pending"),
        "date": task.get("date", ""),
        "result": task.get("response", ""),
        "thoughts": task.get("thoughts"),
        "agent_log": task.get("parsed_agent_log"),
        "started_at": task.get("started_at"),
        "completed_at": task.get("completed_at"),
        "error_message": task.get("error_message"),
        "metadata": {
            "agent_version": task.get("agent_version", "1.0"),
            "priority": task.get("priority", "normal"),
            "retries": task.get("retries", 0)
        }
    }
    
    return jsonify(enhanced_task)

@tinyagent_bp.route('/tasks/submit', methods=['POST'])
def submit_task():
    """Submit a task to the queue for TinyAgent to process."""
    data = request.json
    # print("DEBUG, DATA: ", data)
    query_text = data.get("query", "")
    
    if not query_text:
        return jsonify({"error": "Query is required"}), 400
    
    # Create task with enhanced initial data
    task_id = add_task(query_text)
    
    # Update task with additional metadata
    if task_id in task_status:
        task_status[task_id].update({
            "started_at": datetime.now().isoformat(),
            "parsed_agent_log": {},
            "thoughts": [],  # Initialize empty thoughts array
            "metadata": {
                "agent_version": "1.0",
                "priority": "normal",
                "retries": 0
            }
        })
    
    return jsonify({
        "task_id": task_id,
        "status": "pending",
        "date": datetime.now().isoformat()
    })

@tinyagent_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a specific task."""
    try:
        if task_id in task_status:
            del task_status[task_id]
            return jsonify({'message': 'Task deleted successfully'}), 200
        return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
