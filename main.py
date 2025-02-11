import streamlit as st
import pandas as pd
import random
from datetime import date

if 'question_number' not in st.session_state:
    st.session_state.question_number = 0
    st.session_state.csv = pd.read_csv('responses_to_surface.csv'
                                       , index_col = 0)
    
    # initialise empty lists to store responses from user
    st.session_state.best_source = [None]*len(st.session_state.csv)
    st.session_state.response_comments = [None]*len(st.session_state.csv)
    st.session_state.policy_choices = [None]*len(st.session_state.csv)
    st.session_state.policy_comments = [None]*len(st.session_state.csv)

def next_question():
    # append user responses to list
    st.session_state.best_source[st.session_state.question_number] = response_dict[best_response]
    st.session_state.response_comments[st.session_state.question_number] = response_comment
    st.session_state.policy_choices[st.session_state.question_number] = policy_choice
    st.session_state.policy_comments[st.session_state.question_number] = policy_comment

    # reset the text box to empty
    st.session_state.response_comment = ''
    st.session_state.policy_comment = ''
    
    # save responses as we go
    st.session_state.csv['best_response'] = st.session_state.best_source
    st.session_state.csv['response_comments'] = st.session_state.response_comments
    st.session_state.csv['policy_choices'] = st.session_state.policy_choices
    st.session_state.csv['policy_comments'] = st.session_state.policy_comments
    # st.session_state.csv.to_csv('results.csv')

    # advance to next question
    st.session_state.question_number += 1 


if st.session_state.question_number < len(st.session_state.csv):
    response_dict = eval(st.session_state.csv.loc[st.session_state.question_number].response_dict)
    policy_numbers = eval(st.session_state.csv.loc[st.session_state.question_number].policies_sorted)

    # write the question to the user
    st.header(f'Question {st.session_state.question_number+1}/{len(st.session_state.csv)}')
    st.write(st.session_state.csv\
            .loc[st.session_state.question_number].question)
    st.divider()


    # get the best responses
    best_response = st.radio(
        'Which of the following is the best response?'
        , response_dict.keys()
    )

    # option for user to provide more information 
    response_comment = st.text_area('(Optional) Provide additional comments about responses here', 
                                    key='response_comment', height=70)

    # user needs to select which policy numbers are relevant to answering this question 
    policy_choice = st.multiselect('Select the policies that are relevant to the question', policy_numbers)

    # option for user to provide more information
    policy_comment = st.text_area("(Optional) If there are policy numbers not supplied above, include them in this space", 
                                    key='policy_comment', height=70)

    st.button('Next', on_click=next_question)
else: 
    def convert_df(df):
        return df.to_csv()

    csv = convert_df(st.session_state.csv)

    st.write("You're at the end, thank you! Please download your responses and share it with a team member :)")
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f"results_{date.today()}.csv",
        mime="text/csv",
    )
    