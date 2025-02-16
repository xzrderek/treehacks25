import asyncio
import uuid
from queue import Queue
from tinyagent.src.tiny_agent.tiny_agent import TinyAgent
from tinyagent.src.tiny_agent.config import get_tiny_agent_config

CONFIG_PATH = "Configuration.json"
tiny_agent_config = get_tiny_agent_config(config_path=CONFIG_PATH)
tiny_agent = TinyAgent(tiny_agent_config)

task_queue = Queue()
task_store = {}  # Store task details by ID

async def query_tiny_agent(query: str):
    """
    Runs TinyAgent with the given query and returns the response.
    """
    response = await tiny_agent.arun(query=query)
    return response

### **1️⃣ Add a new task**
def add_task(task_description):
    """
    Add a new task to the queue and return the task ID.
    """
    task_id = str(uuid.uuid4())
    task_store[task_id] = {"task_id": task_id, "task_description": task_description, "status": "pending"}
    task_queue.put(task_id)
    return task_id

### **2️⃣ Get all tasks**
def get_all_tasks():
    """
    Retrieve all tasks stored.
    """
    return list(task_store.values())

### **3️⃣ Get a specific task by ID**
def get_task_by_id(task_id):
    """
    Retrieve a specific task by its ID.
    """
    return task_store.get(task_id)

### **4️⃣ Execute a specific task**
async def execute_task_by_id(task_id):
    """
    Execute a specific task using TinyAgent.
    """
    task = task_store.get(task_id)
    if not task or task["status"] in ["completed", "failed"]:
        return None

    task["status"] = "processing"

    try:
        response = await tiny_agent.arun(query=task["task_description"])
        task["status"] = "completed"
        task["response"] = response
    except Exception as e:
        task["status"] = "failed"
        task["error"] = str(e)

    return task["status"]

### **5️⃣ Execute all pending tasks**
async def execute_all_tasks():
    """
    Execute all pending tasks in order.
    """
    statuses = {}

    while not task_queue.empty():
        task_id = task_queue.get()
        status = await execute_task_by_id(task_id)
        statuses[task_id] = status
        task_queue.task_done()

    return statuses