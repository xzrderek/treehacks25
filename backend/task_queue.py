import asyncio
import uuid
from queue import Queue
from threading import Thread
from tinyagent.src.tiny_agent.tiny_agent import TinyAgent
from tinyagent.src.tiny_agent.config import get_tiny_agent_config

# Load TinyAgent configuration
CONFIG_PATH = "Configuration.json"
tiny_agent_config = get_tiny_agent_config(config_path=CONFIG_PATH)
tiny_agent = TinyAgent(tiny_agent_config)

# Queue to store tasks
task_queue = Queue()
task_status = {}  # Dictionary to store task status

def process_tasks():
    """Worker function to process tasks from the queue."""
    while True:
        if not task_queue.empty():
            task_id, query = task_queue.get()

            # Update task status to "processing"
            task_status[task_id] = "processing"

            try:
                response = asyncio.run(tiny_agent.arun(query=query))
                task_status[task_id] = {"status": "completed", "response": response}
            except Exception as e:
                task_status[task_id] = {"status": "failed", "error": str(e)}

            task_queue.task_done()

# Start the background worker
worker_thread = Thread(target=process_tasks, daemon=True)
worker_thread.start()

def add_task(query):
    """Add a new task to the queue and return the task ID."""
    task_id = str(uuid.uuid4())  # Generate a unique task ID
    task_status[task_id] = "pending"
    task_queue.put((task_id, query))
    return task_id

def get_task_status(task_id):
    """Retrieve the status of a specific task."""
    return task_status.get(task_id, "not found")