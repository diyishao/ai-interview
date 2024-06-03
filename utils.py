import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from prompt_template import system_template_text, chinese_system_template_text


def get_chat_response(user_input, memory, resume, language):
    if language == "English":
        system_prompt = system_template_text + str(resume)
    else:
        system_prompt = chinese_system_template_text + str(resume)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    model = ChatOpenAI(model="gpt-3.5-turbo",
                       openai_api_key=st.secrets["openai_api_key"],
                       openai_api_base="https://api.aigc369.com/v1")

    chain = ConversationChain(llm=model, memory=memory, prompt=prompt)

    response = chain.predict(input=user_input)
    return response
