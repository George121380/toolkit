from openai import OpenAI
import time
import tiktoken

def count_tokens_tiktoken(query: str, model: str = "gpt-4o") -> int:
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(query)
    return len(tokens)

Openai_key = "" # Fill your OpenAI key here
Deepseek_key = "" # Fill your Deepseek key here
Thirdparty_key = "" # Fill your thirdparty key here

# LLM_MODEL = "gpt-4o"
LLM_MODEL = "deepseek"
# LLM_MODEL = "thirdparty"

# empty the log file
with open("query_log.txt", "w") as log_file:
    log_file.write("")

def query_LLM(system,content):
    while True:
        try:
            if LLM_MODEL == "gpt-4o": # GPT-4o api
                # with open("/Users/liupeiqi/workshop/Research/api_key.txt","r") as f:
                #     api_key = f.read().strip()
                client = OpenAI(api_key=Openai_key)
                
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content":content}
                    ]
                )
            elif LLM_MODEL == "deepseek": # Deepseek api
                client = OpenAI(api_key=Deepseek_key, base_url="https://api.deepseek.com")
                completion = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": content},
                    ],
                    stream=False
                )
            elif LLM_MODEL == "thirdparty": # Taobao
                client = OpenAI(api_key=Thirdparty_key, base_url="https://api.feidaapi.com/v1")
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": content},
                    ],
                    stream=False
                )
            else:
                raise ValueError("Invalid LLM_MODEL")
            
            with open("query_log.txt", "a") as log_file:
                log_file.write(f"System: {system}\nContent: {content}\n\n")
                log_file.write(f"Response:\n{completion.choices[0].message.content}\n\n")
                log_file.write("Tokens: " + str(count_tokens_tiktoken(completion.choices[0].message.content)+count_tokens_tiktoken(system)+count_tokens_tiktoken(content)) + "\n")
                log_file.write("#"*80 + "\n\n")
            
            return completion.choices[0].message.content
            
        except Exception as e:
            print(e)
            time.sleep(1)
            continue