import asyncio
import uuid
from queue import Queue
from threading import Thread
from datetime import datetime
from .services import query_tiny_agent
import traceback

# Queue to store tasks
task_queue = Queue()
task_status = {}  # Dictionary to store task status

def add_thought(task_id, thought_text):
    """Helper function to add a thought to a task."""
    if task_id in task_status:
        if "thoughts" not in task_status[task_id]:
            task_status[task_id]["thoughts"] = []
        
        new_thought = {
            "step": len(task_status[task_id]["thoughts"]) + 1,
            "thought": thought_text,
            "timestamp": datetime.now().isoformat()
        }
        task_status[task_id]["thoughts"].append(new_thought)

def process_tasks():
    """Worker function to process tasks from the queue."""
    while True:
        if not task_queue.empty():
            task_id, query = task_queue.get()
            
            # Update status to processing and set started_at timestamp
            task_status[task_id].update({
                "status": "processing",
                "started_at": datetime.now().isoformat()
            })
            
            add_thought(task_id, "Starting task processing")
            
            try:
                add_thought(task_id, "Initializing agent query")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                add_thought(task_id, "Executing agent query with 30-second timeout")
                response, parsed_log = loop.run_until_complete(
                    asyncio.wait_for(
                        query_tiny_agent(query), 
                        timeout=30.0
                    )
                )
                loop.close()
                
                add_thought(task_id, "Query completed successfully")
                task_status[task_id].update({
                    "status": "completed",
                    "response": response,
                    "parsed_agent_log": parsed_log,
                    "completed_at": datetime.now().isoformat(),
                    "task_description": task_status[task_id]["task_description"]
                })
                
            except asyncio.TimeoutError:
                add_thought(task_id, "Task exceeded timeout limit")
                task_status[task_id].update({
                    "status": "failed",
                    "error_message": "Task exceeded 30 second timeout limit",
                    "completed_at": datetime.now().isoformat(),
                    "task_description": task_status[task_id]["task_description"]
                })
                
            except Exception as e:
                exc = traceback.format_exc()
                add_thought(task_id, f"Task failed with error: {str(e)}")
                task_status[task_id].update({
                    "status": "failed",
                    "response": f"Exception occured: {exc}",
                    "error_message": f"Exception: {str(e)}",
                    "error_trace": exc,
                    "completed_at": datetime.now().isoformat(),
                    "task_description": task_status[task_id]["task_description"]
                })
                
            task_queue.task_done()

# Start the background worker
worker_thread = Thread(target=process_tasks, daemon=True)
worker_thread.start()

def add_task(query):
    """Add a new task to the queue and return the task ID."""
    task_id = str(uuid.uuid4())
    current_time = datetime.now().isoformat()
    
    # Initialize task with all required fields
    task_status[task_id] = {
        "task_id": task_id,
        "task_description": query,
        "status": "pending",
        "date": current_time,
        "started_at": None,
        "completed_at": None, 
        "response": None,
        "error_message": None,
        "thoughts": [],
        "parsed_agent_log": {},
        "metadata": {
            "agent_version": "1.0",
            "priority": "normal",
            "retries": 0
        }
    }
    
    # Add initial thought
    add_thought(task_id, "Task created and added to queue")
    
    # Add task to processing queue
    task_queue.put((task_id, query))
    return task_id

def get_task_status(task_id):
    """Retrieve the status of a specific task."""
    return task_status.get(task_id, "not found")

def get_all_tasks():
    """Return all tasks and their statuses."""
    return task_status