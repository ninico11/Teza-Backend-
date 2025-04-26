from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENAI_KEY")
openai = OpenAI(api_key=API_KEY)

def translate_message_event(message, requested_language):
    output_format = """
    {
        "translated_message": here should be translated message

    }"""
    system_prompt = f"""
    Role:
    You are professional translator, you need to translete user message in requested language.
    
    User Message: ```{message}```
    Requested Language: ```{requested_language}```
    
    Task:
        In order to do your task you need to do this steps:
        Step 1: Analyze user message, it's context and grammar
        Step 2: Translate user message without losing context and respecting grammar of requested language
    
    You should output a JSON in this format:
        ```{output_format}```
    """
    
    response = openai.chat.completions.create(
        model="gpt-4.1-nano",
        temperature=0.01,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": system_prompt}]
    )

    return response.choices[0].message.content

def translate_for_snetiment(message):
    output_format = """
    {
        "translated_message": here should be translated message

    }"""
    system_prompt = f"""
    Role:
    You are professional translator, you need to translete user message in requested language.
    
    User Message: ```{message}```
    Requested Language: EN
    
    Task:
        In order to do your task you need to do this steps:
        Step 1: Analyze user message, it's context, grammar and sentiment
        Step 2: Translate user message without losing context and respecting grammar of requested language, if message have some jargons or another phrases with hidden meaning, try to find analog in english or put this hidden meaning in context.
    
    You should output a JSON in this format:
        ```{output_format}```
    """
    
    response = openai.chat.completions.create(
        model="gpt-4.1-nano",
        temperature=0.01,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": system_prompt}]
    )

    return response.choices[0].message.content