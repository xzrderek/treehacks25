import asyncio  # Needed for running async functions
from tinyagent.src.tiny_agent.tiny_agent import TinyAgent
from tinyagent.src.tiny_agent.config import get_tiny_agent_config

# Set the correct path
config_path = "./Configuration.json"

# Load the TinyAgent configuration
tiny_agent_config = get_tiny_agent_config(config_path=config_path)
tiny_agent = TinyAgent(tiny_agent_config)

# Define an async function to test TinyAgent
async def test_tiny_agent():
    response = await tiny_agent.arun(query="Create a meeting with Sid and Lutfi for tomorrow 2pm to discuss the meeting notes.")
    print("TinyAgent Response:", response)

# Run the async function
asyncio.run(test_tiny_agent())