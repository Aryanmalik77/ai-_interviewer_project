import random
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.schema import HumanMessage
import streamlit as st

load_dotenv()

st.title("Ai interview app")
st.write("Answer AI interview Questions and It will give instant feedback and score for the same")
llm= HuggingFaceEndpoint(
    repo_id = "deepseek-ai/DeepSeek-V3.2-Exp",
    task = "text-generation",
    huggingfacehub_api_token="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"
)
model = ChatHuggingFace(llm=llm)



questions = ["tell me about your self ",
                "why should we hire you?",
                "which language you are best at?",
                "why you choose this language",
                 "Any project you have made it regarding this language"]
random.shuffle(questions)

selected_questions = questions[:]
print("welcome to ai intervier round")

prompt = PromptTemplate(
    template="question:{question}\n answer:{answer}\n give a score from rangig 0 to 10\n give a small feedback regarding my answer",

    input_variables = ["question", "answer"],

)
interview_question = []
if "q_index" not in st.session_state:
        st.session_state.q_index = 0
if "answer" not in st.session_state:
    st.session_state.answer = []
if st.session_state.q_index < len(selected_questions):
    questions = selected_questions[st.session_state.q_index]
    st.write("AI:"+ questions)
    answer = st.text_area("you:", key=f"answer_{st.session_state.q_index}")
    if st.button("next question"):
        if answer.strip():
            st.session_state.answer.append({"question":questions,"answer":answer})
            st.session_state.q_index +=1
            st.rerun()
        else:
            st.warning("please attach answer")
else:
    st.subheader("interview completed!!!")
    st.write("your feedback is given below")
    combined_answers="/n/n".join(
        [f"Q:{item["question"]}\nA:{item["answer"]}" for item in st.session_state.answer]
    )

    prompt = PromptTemplate(
    template=
        "You are an expert interviewer.\n"
        "Here are the candidate's responses:\n\n{answers}\n\n"
        "Now give detailed feedback:\n"
        "- Evaluate each answer briefly (1–2 lines per question)\n"
        "- Then give an overall performance rating (0–10)\n"
        "- Suggest areas for improvement",
    input_variables =["answers"])
    prompt_result = prompt.format(answers=combined_answers)
    response = model([HumanMessage(content=prompt_result)])
    st.write(response)
    feedback = response.content.strip()
    st.write(feedback)


