from enum import Enum

from bs4 import BeautifulSoup
from langchain_core.messages import HumanMessage, SystemMessage

from tinyagent.src.tiny_agent.sub_agents.sub_agent import SubAgent

from openai import OpenAI
import os

def ask_question(question):
    return ([
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
                "Provide accurate information as fast as possible."
            ),
        },
        {   
            "role": "user",
            "content": (
                f"Question: {question}"
            ),
        },
    ])

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY") 
client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")

class SonarAgent(SubAgent):
    async def __call__(
        self,
        question: str
    ) -> str:
        # CHANGE TO USE SONAR
        messages = ask_question(question)
        
        response = client.chat.completions.create(
            model="sonar",
            messages=messages,
        )

        completion = response.choices[0].message.content
        citations = response.citations
        
        return ("ASKING SONAR...\n\nCompletion: " + completion + "\n\nCitations: [" + ",".join(citations) + "]") 