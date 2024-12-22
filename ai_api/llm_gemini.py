#!python3.10
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2024-04-25 20:18:20
LastEditors: sanford courageux_san@wechat.com
LastEditTime: 2024-12-22 23:19:17
FilePath: /script/ai_api/llm_gemini.py
'''
import os
import requests
import PIL.Image
from io import BytesIO
import google.generativeai as genai
from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


GENAI_API_KEY = os.getenv('GENAI_API_KEY')
ai_max_length = 1000

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

def split_text_into_chunks(text, max_length=ai_max_length):
    """
    Split text into chunks with a maximum length, ensuring that splits only occur at line breaks.
    """
    lines = text.splitlines()
    chunks = []
    current_chunk = ''
    for line in lines:
        if len(current_chunk + ' ' + line) <= max_length:
            current_chunk += ' ' + line
        else:
            chunks.append(current_chunk)
            current_chunk = line
    chunks.append(current_chunk)
    return chunks

# geminni 直连 文字
def rewrite_text_with_genai(text, model_name="gemini-pro", prompt="Please rewrite this text:"):
    chunks = split_text_into_chunks(text)
    rewritten_text = ''
    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel(model_name)
    for chunk in chunks:
        _prompt=f"{prompt}\n{chunk}",
        response = model.generate_content(
            contents=_prompt, 
            generation_config=genai.GenerationConfig(
                temperature=0.1,
            ),
            stream=True,
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_DANGEROUS",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
            ]
        )
        for _chunk in response:
            if _chunk.text is not None:
                rewritten_text += _chunk.text.strip()

    return rewritten_text

# gemini 直连 多媒体
def gemini_media(image_url, prompt):
    r = requests.get(image_url)
    image = PIL.Image.open(BytesIO(r.content))
    image.save('api/image2.png', 'PNG')
    image = PIL.Image.open('api/image.png')
    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(image)
    response = model.generate_content([prompt, image], stream=True)
    response.resolve()

    return response.text

# gemini 直连 langchain
def gemini_langchain_chat(text, model_name="gemini-pro"):
    chat_template = ChatPromptTemplate.from_messages([
            SystemMessage(content=("")),
            HumanMessagePromptTemplate.from_template("{text}"),
        ])
    chat_message =  chat_template.format_messages(text=text)

    model = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)
    result = model(chat_message)
    print(result.content)

# gemini 代理 文字
def gemini_chat_proxy(url, prompt, mode_name="gpt-4"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+ GENAI_API_KEY
    }
    data = {
        "model": mode_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url=url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']


if __name__ == '__main__':
    res = rewrite_text_with_genai(text='', prompt='你是谁')

    # res = gemini_media(
    #     image_url='https://mmilabel-1258344707.cos.ap-guangzhou.myqcloud.com/upload/unpack/cardli/20240507/image/1005129185_b1d78a1a84f376cdf76980885253c666.jpg_ocrmt_new.jpg',
    #     prompt="""你需要使用一句英文句子来总结图片中的核心内容, 句子类似于图片标题一样的, 如果是一些产品图片只用说明产品是什么就行。 要求: 1. 句子要简洁明了，能够体现出主图片的主题; 2. 句子不要过长，不用描述一些很细节的东西; 3. 可以描述清楚它是什么牌子的，它是什么东西，它是干什么的。"""
    #     )

    # res = gemini_chat_proxy(
    #     url="https://gemini-openai-proxy2.zeabur.app/v1/chat/completions",
    #     mode_name="gpt-4",
    #     prompt="你是谁?"
    #     )
    # print(res)

