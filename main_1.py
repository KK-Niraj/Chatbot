import streamlit as st
import openai
import os

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("my_api_key")

# Set the model and chatbot's name
model_name = 'gpt-3.5-turbo'
chatbot_name = 'ChatGPT Bot'

# Initialize conversation history
conversation = []


# Main function to interact with the chatbot
def run_chatbot(message):
    conversation.append({'role': 'user', 'content': message})

    # Create the list of messages for OpenAI API
    messages = [{'role': 'system', 'content': 'You are ChatGPT Bot.'}]
    messages.extend(conversation)

    # Call OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages
    )

    # Get the generated reply from the response
    reply = response['choices'][0]['message']['content']

    conversation.append({'role': 'bot', 'content': reply})
    return reply


# Streamlit app layout
def app_layout():
    st.title(chatbot_name)

    # Initial system message
    st.markdown('Chat with the ChatGPT Bot!')

    # User input
    user_input = st.text_input("User:", "")

    # Send user message and get bot's reply
    if st.button("Send"):
        bot_reply = run_chatbot(user_input)

        # Display bot's reply
        st.text_area("Bot:", value=bot_reply, height=100)


# Run the Streamlit app
if __name__ == '__main__':
    app_layout()