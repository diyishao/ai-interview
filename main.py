import streamlit as st
from langchain.memory import ConversationBufferMemory
from utils import get_chat_response

#from audiorecorder import audiorecorder

#st.title("Audio Recorder")
#audio = audiorecorder("Click to record", "Click to stop recording")

#if len(audio) > 0:
    # To play audio in frontend:
    #st.audio(audio.export().read())

    # To save audio to a file, use pydub export method:
    #audio.export("audio.wav", format="wav")

    # To get audio properties, use pydub AudioSegment properties:
    #st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")

with st.sidebar:
    language = st.select_slider("", options=["English", "中文"], value="中文")

    if "language" in st.session_state and language != st.session_state["language"]:
        if "memory" in st.session_state:
            del st.session_state["memory"]
        if "messages" in st.session_state:
            del st.session_state["messages"]

    st.session_state["language"] = language
    #if language == "English":
    #    openai_api_key = st.text_input("Please input your OpenAI API Key：", type="password")
    #    st.markdown("[Get OpenAI API key here](https://platform.openai.com/account/api-keys)")
    #else:
    #    openai_api_key = st.text_input("请输入OpenAI API Key：", type="password")
    #    st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")

if st.session_state["language"] == "English":
    st.title("AI Interviewer")
else:
    st.title("AI 面试官")

if "memory" not in st.session_state:
    memory = ConversationBufferMemory(return_messages=True)

    st.session_state["memory"] = memory

    st.session_state["messages"] = []

if st.session_state["language"] == "English":
    resume = st.file_uploader("Please upload your resume to begin:", type=["txt"])
else:
    resume = st.file_uploader("请上传你的简历，然后开始跟面试官聊天:", type=["txt"])

if resume:
    for message in st.session_state["messages"]:
        if message["role"] != "system":
            st.chat_message(message["role"]).write(message["content"])

input = st.chat_input(disabled=not resume)

if input:
    resume_content = resume.read()
    print(resume_content)
    st.session_state["messages"].append({"role": "human", "content": input})
    st.chat_message("human").write(input)

    with st.spinner("AI interviewer is listening..."):
        response = get_chat_response(input, st.session_state["memory"], resume_content, st.session_state["language"])

    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)

