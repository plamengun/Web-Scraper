import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.environ.get('OPENAI_ORG')
openai.api_key = os.environ.get('OPENAI_API_KEY')
completion = openai.ChatCompletion()


async def askgpt(role, questions, chat_log=None):
    if chat_log is None:
        chat_log = [{
            'role': 'system',
            'content': role
        }]
    
    if not questions:
        return chat_log
    
    question = questions[0]
    chat_log.append({'role': 'user', 'content': question})
    
    response = await openai.Completion.create(
        engine="text-davinci-003",
        prompt="\n".join([message['content'] for message in chat_log]),
        max_tokens=500
    )
    
    answer = await response.choices[0]['text']
    chat_log.append({'role': 'assistant', 'content': answer})
    
    # Recursively call askgpt with the remaining questions
    return await askgpt(role, questions[1:], chat_log)


# # questions = [PROMPT, "What are some tips for writing an effective proposal?", "How can I stand out to clients on Upwork?"]
# questions = [JOB_PROPERTIES]
# log = askgpt(ROLE_CONTENT, questions)
# # print(log)
# # for entry in log:
# #     print(entry)
# for entry in log:
#     if entry['role'] == 'assistant':
#         print(entry['content'])