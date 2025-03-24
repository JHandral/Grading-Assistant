import streamlit as st
import autograder
import csv
import re
import json

st.title('LIGN 167 Grading Assistant')
TEST_MODE = False

# Setup state variables if needed
if 'state' not in st.session_state:
    st.session_state.state = "files"
if 'results' not in st.session_state:
    st.session_state.results = {}

# Creates the pretty table with results from the CSV output :)
def format_results(results):
    html = """
            <style>
            .correct { background: #00a67d; }
            .incorrect { background: #df3079; }
            </style>
            <table>
            """
    total_pts = 0
    total_poss = 0
    cur_question = None
    for result in results:
        qnum = int(result["qnum"])
        pts_earned = float(result["pts_earned"])
        pts_poss = float(result["pts_possible"])
        correct = bool(result["correct"])
        summary = result["criteria"] if "criteria" in result else ""
        feedback = result["feedback"] if "feedback" in result else ""

        if cur_question != qnum:
            cur_question = qnum
            # html += f"<tr><th colspan=\"3\"><center>Question {qnum}</center></th></tr>"
            html += "<tr><th scope=\"col\">Points</th><th scope=\"col\">Criteria</th><th scope=\"col\">Reasoning</th></tr>"
        total_pts += pts_earned
        total_poss += pts_poss
        hclass = "correct" if correct else "incorrect"
        html += f"""
                <tr>
                    <td class=\"{hclass}\">{pts_earned}/{pts_poss}</td>
                    <td>{summary}</td>
                    <td>{feedback}</td>
                </tr>
                """
    html += "</table><br>"
    # html += f"<b><i>Total points: {total_pts}/{total_poss}</i></b>"
    # st.session_state.pts_earned += total_pts
    # st.session_state.pts_poss += total_poss
    st.markdown(html.replace("\n",""), unsafe_allow_html=True)
    return True

# Shows the results of a single question.
# msg - The message from chatgpt, which should be a CSV-formatted table with details of the grading.
# question - The ordinal number of the question.
def show_results(question):
    if question not in st.session_state.results:
        return
    msg = st.session_state.results[question].strip()
    raw_msg = msg
    start_re = re.search("```(json)*", msg)
    if start_re is not None:
        end = msg.find("```", start_re.span()[1])
        msg = msg[start_re.span()[1]:end].strip()

    # Try parsing json
    parsed_msg = None
    res = False
    try:
        parsed_msg = json.loads(msg)
        if isinstance(parsed_msg, dict):
            parsed_msg = [parsed_msg]
        res = format_results(parsed_msg)
    except Exception as err:
        st.error(f"There was a problem, ChatGPT gave the following output:\n{raw_msg}\n\nwhich resulted in the following exception:\n{err}")
        return False

    if parsed_msg is not None:
        st.json(parsed_msg[0] if len(parsed_msg) == 1 else parsed_msg, expanded=False)

    return res

# Grades the given answer file with the given key and assignment files.
def begin(answers, key, assignment):
    with st.spinner('Preparing...'):
        st.session_state.grader = autograder.Grader(answers, key, assignment, TEST_MODE)
        st.session_state.state = "ready"

def grade(question):
    st.session_state.state = "grading"
    st.session_state.question = question 

# Files uploading
if st.session_state.state == "files":
    st.text('Welcome to the grading assistant! Please input the assignment, answers, and rubric.')
    answers = st.file_uploader("Choose student answers")
    key = st.file_uploader("Choose key")
    assignment = st.file_uploader("Choose assignment file")
    if (answers is not None and assignment is not None and key is not None):
        st.button('Begin', on_click=begin, args=[answers, key, assignment])

if st.session_state.state in ["ready", "grading"]:
    containers = []
    for i in range(st.session_state.grader.num_questions()):
        st.divider()
        container = st.container()
        containers.append(container)
        with container:
            st.header(f"Question {i+1}")
            with st.expander(f"Student's Answer", expanded=True):
                st.code(st.session_state.grader.get_ans(i))
            with st.expander(f"GPT Key", expanded=False):
                st.code(st.session_state.grader.get_rub(i))
            is_graded = i in st.session_state.results
            if is_graded:
                with st.expander("GPT's Suggested Grading", expanded=True):
                    show_results(i)
            st.button("Regrade" if is_graded else "Grade", key=i, on_click=grade, args=[i], disabled=st.session_state.state == "grading")

    if st.session_state.state == "grading":
        container = containers[st.session_state.question]
        with container.status("Preparing...") as status:
            def status_callback(str):
                status.update(label=str)
            st.session_state.results[st.session_state.question] = st.session_state.grader.grade_question(st.session_state.question, status_callback)
        st.session_state.state = "ready"
        st.rerun()
