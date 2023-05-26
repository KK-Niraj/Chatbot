from __future__ import annotations
import os
import sys
import pandas as pd
from csv import writer


from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("my_api_key")

conversation_history = []


def get_api_response(prompt: str) -> str | None:
    text: str | None = None

    try:
        response: dict = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI:']
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text')

    except Exception as e:
        print('ERROR:', e)

    return text


def update_list(message: str, pl: list[str]):
    pl.append(message)


def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt


def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something went wrong....'

    return bot_response


def main():
    prompt_list: list[str] = ['You are a cat and will answer as a cat',
                              '\nHuman: What time is it?',
                              '\nAI: I have no idea, I\'m a cat!']
    ques = []
    resp = []
    while True:
        user_input: str = input('You: ')
        conversation_history.append(user_input)
        context = conversation_history + prompt_list

        if user_input.lower() == 'exit':
            lst = [ques, resp]
            with open('data.csv', 'a') as f_obj:
                writer_obj = writer(f_obj)

                writer_obj.writerow(lst)

                f_obj.close()

            df = pd.DataFrame(f_obj)
            df.to_csv('data.csv')
            sys.exit()

        response: str = get_bot_response(user_input, context)
        context.append(response)
        ques.append(user_input)
        resp.append(response)
        print(f'Bot: {response}')


if __name__ == '__main__':
    main()
