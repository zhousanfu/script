#!python3.10
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2024-04-25 20:18:20
 LastEditors: Sanfor Chow
 LastEditTime: 2024-04-26 22:22:04
 FilePath: /script/api/llm_gemini.py
'''
import os
import google.generativeai as genai

GENAI_API_KEY = os.getenv('genai_api_key')
ai_max_length = 1000

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

def rewrite_text_with_genai(text, prompt="Please rewrite this text:"):
    chunks = split_text_into_chunks(text)
    rewritten_text = ''
    # pbar = tqdm(total=len(chunks), ncols=150)
    genai.configure(api_key=os.getenv('genai_api_key'))
    model = genai.GenerativeModel('gemini-pro')
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
    #     pbar.update(1)
    # pbar.close()
    return rewritten_text



if __name__ == '__main__':
    res = rewrite_text_with_genai(text='', prompt='你是谁')
    print(res)