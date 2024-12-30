import os
import re
import json
import traceback
from typing import List
from loguru import logger
from openai import OpenAI
from openai import AzureOpenAI
from openai.types.chat import ChatCompletion
import google.generativeai as gemini
from googleapiclient.errors import ResumableUploadError
from google.api_core.exceptions import *
from google.generativeai.types import *
from pydantic import BaseModel, Field
from config.config import cfg_llm




class AwardResponse(BaseModel):
    title: str
    summary: str
    _is: bool = Field(description="是否有奖励")


# def handle_exception(err):
#     if isinstance(err, PermissionDenied):
#         raise Exception("403 用户没有权限访问该资源")
#     elif isinstance(err, ResourceExhausted):
#         raise Exception("429 您的配额已用尽。请稍后重试。请考虑设置自动重试来处理这些错误")
#     elif isinstance(err, InvalidArgument):
#         raise Exception("400 参数无效。例如，文件过大，超出了载荷大小限制。另一个事件提供了无效的 API 密钥。")
#     elif isinstance(err, AlreadyExists):
#         raise Exception("409 已存在具有相同 ID 的已调参模型。对新模型进行调参时，请指定唯一的模型 ID。")
#     elif isinstance(err, RetryError):
#         raise Exception("使用不支持 gRPC 的代理时可能会引起此错误。请尝试将 REST 传输与 genai.configure(..., transport=rest) 搭配使用。")
#     elif isinstance(err, BlockedPromptException):
#         raise Exception("400 出于安全原因，该提示已被屏蔽。")
#     elif isinstance(err, BrokenResponseError):
#         raise Exception("500 流式传输响应已损坏。在访问需要完整响应的内容（例如聊天记录）时引发。查看堆栈轨迹中提供的错误详情。")
#     elif isinstance(err, IncompleteIterationError):
#         raise Exception("500 访问需要完整 API 响应但流式响应尚未完全迭代的内容时引发。对响应对象调用 resolve() 以使用迭代器。")
#     elif isinstance(err, ConnectionError):
#         raise Exception("网络连接错误, 请检查您的网络连接(建议使用 NarratoAI 官方提供的 url)")
#     else:
#         raise Exception(f"大模型请求失败, 下面是具体报错信息: \n\n{traceback.format_exc()}")


def generate_response(
        prompt: str,
        llm_provider: str = None,
        structur: bool = True,
        Response=None
        ) -> str:
    """
    调用大模型通用方法
        prompt
        llm_provider
    """
    results = ""
    api_version = ""  # for azure

    if llm_provider == "openai":
        api_key = cfg_llm.get("openai_api_key")
        model_name = cfg_llm.get("openai_model_name")
        base_url = cfg_llm.get("openai_base_url", "https://api.openai.com/v1")
    elif llm_provider == "xai":
        api_key = cfg_llm.get("xai_api_key")
        model_name = cfg_llm.get("xai_model_name")
        base_url = cfg_llm.get("xai_base_url")
    elif llm_provider == "moonshot":
        api_key = cfg_llm.get("moonshot_api_key")
        model_name = cfg_llm.get("moonshot_model_name")
        base_url = cfg_llm.get("moonshot_base_url", "https://api.moonshot.cn/v1")
    elif llm_provider == "ollama":
        api_key = "ollama"  # any string works but you are required to have one
        model_name = cfg_llm.get("ollama_model_name")
        base_url = cfg_llm.get("ollama_base_url", "")
        if not base_url:
            base_url = "http://localhost:11434/v1"
    elif llm_provider == "azure":
        api_key = cfg_llm.get("azure_api_key")
        model_name = cfg_llm.get("azure_model_name")
        base_url = cfg_llm.get("azure_base_url", "")
        api_version = cfg_llm.get("azure_api_version", "2024-02-15-preview")
    elif llm_provider == "gemini":
        api_key = cfg_llm.get("gemini_api_key")
        model_name = cfg_llm.get("gemini_model_name")
        base_url = "***"
    elif llm_provider == "qwen":
        api_key = cfg_llm.get("qwen_api_key")
        model_name = cfg_llm.get("qwen_model_name")
        base_url = "***"
    elif llm_provider == "cloudflare":
        api_key = cfg_llm.get("cloudflare_api_key")
        model_name = cfg_llm.get("cloudflare_model_name")
        account_id = cfg_llm.get("cloudflare_account_id")
        base_url = "***"
    elif llm_provider == "deepseek":
        api_key = cfg_llm.get("deepseek_api_key")
        model_name = cfg_llm.get("deepseek_model_name")
        base_url = cfg_llm.get("deepseek_base_url")
        if not base_url:
            base_url = "https://api.deepseek.com"
    elif llm_provider == "ernie":
        api_key = cfg_llm.get("ernie_api_key")
        secret_key = cfg_llm.get("ernie_secret_key")
        base_url = cfg_llm.get("ernie_base_url")
        model_name = "***"

    if llm_provider == "openai":
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
    elif llm_provider == "xai":
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
    elif llm_provider == "g4f":
        model_name = cfg_llm.get("g4f_model_name", "")
        if not model_name:
            model_name = "gpt-3.5-turbo-16k-0613"
        import g4f
        content = g4f.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
    elif llm_provider == "qwen":
        import dashscope
        from dashscope.api_entities.dashscope_response import GenerationResponse

        dashscope.api_key = api_key
        response = dashscope.Generation.call(
            model=model_name, messages=[{"role": "user", "content": prompt}]
        )
        if response:
            if isinstance(response, GenerationResponse):
                status_code = response.status_code
                if status_code != 200:
                    raise Exception(
                        f'[{llm_provider}] returned an error response: "{response}"'
                    )

                content = response["output"]["text"]
                return content.replace("\n", "")
            else:
                raise Exception(
                    f'[{llm_provider}] returned an invalid response: "{response}"'
                )
        else:
            raise Exception(f"[{llm_provider}] returned an empty response")
    elif llm_provider == "gemini":
        pass
        # import google.generativeai as genai

        # genai.configure(api_key=api_key, transport="rest")

        # safety_settings = {
        #     HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        #     HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        #     HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        #     HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        # }

        # model = genai.GenerativeModel(
        #     model_name=model_name,
        #     safety_settings=safety_settings,
        # )

        # try:
        #     response = model.generate_content(prompt)
        #     return response.text
        # except Exception as err:
        #     return handle_exception(err)
    elif llm_provider == "cloudflare":
        import requests

        response = requests.post(
            f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model_name}",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "messages": [
                    {"role": "system", "content": "You are a friendly assistant"},
                    {"role": "user", "content": prompt},
                ]
            },
        )
        result = response.json()
        logger.info(result)
        return result["result"]["response"]
    elif llm_provider == "ernie":
        import requests

        params = {
            "grant_type": "client_credentials",
            "client_id": api_key,
            "client_secret": secret_key,
        }
        access_token = (
            requests.post("https://aip.baidubce.com/oauth/2.0/token", params=params)
            .json()
            .get("access_token")
        )
        url = f"{base_url}?access_token={access_token}"

        payload = json.dumps(
            {
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.5,
                "top_p": 0.8,
                "penalty_score": 1,
                "disable_search": False,
                "enable_citation": False,
                "response_format": "text",
            }
        )
        headers = {"Content-Type": "application/json"}

        response = requests.request(
            "POST", url, headers=headers, data=payload
        ).json()
        return response.get("result")
    elif llm_provider == "azure":
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=base_url,
        )


    if structur:
            completion = client.beta.chat.completions.parse(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                response_format=Response,
            )
            results = completion.choices[0].message.content
    else:
        stream = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in stream:
            if chunk:
                res = chunk.choices[0].delta.content
                if res:
                    results += res

        return results



if __name__=="__main__":
    print(cfg_llm)
    # res = generate_response(prompt="你是谁", llm_provider="xai")
    # print(res)
