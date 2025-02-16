import asyncio

from tinyagent.src.tiny_agent.tiny_agent import TinyAgent
from tinyagent.src.tiny_agent.config import get_tiny_agent_config

async def main():
    config_path = "./config.json"  # You'll need to specify your actual config path here
    tiny_agent_config = get_tiny_agent_config(config_path=config_path)
    tiny_agent = TinyAgent(tiny_agent_config)
    
    await tiny_agent.arun(query="Write an email tomorrow with Richard Chao for tomorrow 2pm to discuss the meeting notes.")

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
