from langchain_openai import ChatOpenAI
import logging

grammar_text_template = f"""
    please check the grammar and spelling mistake of this text and only send the correct text : 
"""

phrase_text_template = f"""
    please write about this text and only send the answer : 
"""

summerize_text_template = f"""
    please full summerize this text and only send the summerized text : 
"""

templates = {'grammar' : grammar_text_template,
             'phrase' : phrase_text_template,
             'summerize' : summerize_text_template}

def SendRequestToAPi(action:str ,text : str):
    logging.info(f"Starting bio analyzer...")
    base_url = "https://api.avalai.ir/v1"
    api_key = "AVALAI_API_KEY"
    model_name = "gpt-4o"

    llm = ChatOpenAI(
        base_url=base_url,
        name=model_name,
        api_key="YOUR_API_KEY",
    )

    response = dict(llm.invoke(templates[action] + text)).get('content',"timed out")
    return response
