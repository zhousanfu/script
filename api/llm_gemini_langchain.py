#!python3.10
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2024-04-28 21:40:24
 LastEditors: courageux_san WX
 LastEditTime: 2024-06-16 10:33:36
 FilePath: /script/api/llm_gemini_langchain.py
'''
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
import requests
# !pip install -U --quiet langchain-google-genai  langchain


GENAI_API_KEY = os.getenv('GENAI_API_KEY')
ai_max_length = 1000
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.getenv('GENAI_API_KEY')

class CustomLLM(LLM):
    url: str
    api_key: str
    mode_name: str

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer "+ self.api_key
        }
        data = {
            "model": self.mode_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        response = requests.post(url=self.url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"url": self.url}

def gemini_chat(text):
    chat_template = ChatPromptTemplate.from_messages([
            SystemMessage(content=("")),
            HumanMessagePromptTemplate.from_template("{text}"),
        ])
    chat_message =  chat_template.format_messages(text=text)

    model = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)
    result = model(chat_message)
    print(result.content)


if __name__ == '__main__':
    gemini_chat("你是谁")
    
    chat_llm = CustomLLM(
        url="https://gemini-openai-proxy2.zeabur.app/v1/chat/completions",
        api_key=GENAI_API_KEY,
        mode_name="gpt-4"
        )
    res = chat_llm("你是谁")
    print(res)