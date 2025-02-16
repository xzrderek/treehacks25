import asyncio
from asyncio import TimeoutError

from tinyagent.src.tiny_agent.tiny_agent import TinyAgent
from tinyagent.src.tiny_agent.config import get_tiny_agent_config

AGENT_LOG_FILE_PATH = "/Users/akommula/Library/Application Support/TinyAgent/log.txt"

CONFIG_PATH = "config.json"
tiny_agent_config = get_tiny_agent_config(config_path=CONFIG_PATH)


def parse_agent_log():
    """
    Parse the first three sections of the agent scratchpad.
    Returns a tuple of (task_log, planner_response, agent_scratchpad)
    """
    
    with open(AGENT_LOG_FILE_PATH, "r") as f:
        content = f.read()
    
    task_log_end = content.find("=" * 80)
    task_log = content[:task_log_end].strip()

    planner_start = content.find("LLMCompiler planner response:", task_log_end)
    next_delimiter = content.find("=" * 80, planner_start)
    planner_response = content[planner_start:next_delimiter].strip()
    planner_response = planner_response.replace("LLMCompiler planner response:", "").strip()

    scratchpad_start = content.find("Agent scratchpad:", next_delimiter)
    next_delimiter = content.find("=" * 80, scratchpad_start)
    agent_scratchpad = content[scratchpad_start:next_delimiter].strip()
    agent_scratchpad = agent_scratchpad.replace("Agent scratchpad:", "").strip()

    return {
        "task_log": task_log,
        "planner_response": planner_response,
        "agent_scratchpad": agent_scratchpad
    }
    
    
async def query_tiny_agent(query: str):
    """
    Runs TinyAgent with the given query and returns the response.
    Exits if the query takes longer than 30 seconds.
    """
    
    # Clear log file before initializing agent
    open(AGENT_LOG_FILE_PATH, 'w').close()
    tiny_agent = TinyAgent(tiny_agent_config)

    try:
        task = asyncio.create_task(tiny_agent.arun(query=query))
                
        response = await asyncio.wait_for(task, timeout=30.0)
        parsed_log = parse_agent_log()
        
        return response, parsed_log
        
    except TimeoutError:
        task.cancel()
        
        try:
            await task 
        except asyncio.CancelledError:
            pass
        print("Query timed out after 30 seconds:", query)
        return None