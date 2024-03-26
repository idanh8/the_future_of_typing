import streamlit as st
import algorithms
import random
import streamlit_antd_components as sac
import time
import google.generativeai as genai
# https://nicedouble-streamlitantdcomponentsdemo-app-middmy.streamlit.app/


sac.segmented(
        items=[
            sac.SegmentedItem(icon='facebook'),
            sac.SegmentedItem(icon='whatsapp'),
            sac.SegmentedItem(icon='google'),
            sac.SegmentedItem(icon='linkedin'),
        ], size=15, radius=50, align='center', use_container_width=True, key='input_app', index=1, return_index=True)

if st.session_state["input_app"] == 0:
        st.header('LinkedIn')

# session state is the backbone saving variables
if 'message_input' not in st.session_state:
    st.session_state.message_input = ""

if 'words' not in st.session_state:
    st.session_state.words = []

if 'sentences' not in st.session_state:
    st.session_state.sentences = []

if 'first' not in st.session_state:
    st.session_state.first = True

if st.session_state.first:
    # built to get the first prediction which is rule based and initialize the model in a session_state, will run once
    st.session_state.first = False

    # gemini model
    api_token = "AIzaSyDMzc7JPMJsiu6nwKFWkng4K4gTr_q7Fi4"
    genai.configure(api_key=api_token)
    model = genai.GenerativeModel('gemini-pro')
    st.session_state.model = model

    # first recommendation
    st.session_state.words = algorithms.get_first_word_predictions()
    st.session_state.sentences = algorithms.get_first_sentence_predictions()
    st.rerun()



def handle_text_chosen(text):
    text_to_add = text.replace(".", "")
    if st.session_state.message_input == "":
        st.session_state.message_input += text_to_add
    else:
        st.session_state.message_input += (" " + text_to_add)

    # Define predictive text options
    with st.spinner('Loading inputs...'):
        # time.sleep(3)  # use this if you want to see loading affect if the generation is too quick...
        st.session_state.words = algorithms.get_word_predictions(model=st.session_state.model,
                                                                 current_sentence=st.session_state.message_input,
                                                                 mood="")
        st.session_state.sentences = algorithms.get_sentence_predictions(model=st.session_state.model,
                                                                         current_sentence=st.session_state.message_input,
                                                                         mood="")
    st.success('Done!')  # because of the rerun we are not seeing this pop up...
    st.rerun()


def update_message_input(new_text):
    st.session_state.message_input = new_text


def thumbs_up_button(words=True):
    if words:
        st.write('Good Word Suggestions')
    else:
        st.write('Good Phrase Suggestions')


def thumbs_down_button(words=True):
    if words:
        st.write('Bad Word Suggestions')
    else:
        st.write('Bad Phrase Suggestions')


def refresh_button(words=True):
    if words:
        st.write('Generating New Words')
    else:
        st.write('Generating New Sentences')


# Layout for predictive text buttons using columns
cont = st.container()
with cont:
    col0, col1, col2 = st.columns([10, 5, 10])
    with col0:
        cont1 = st.container(border=True)
        with cont1:
            col1a, col1b = st.columns(2)
            with col1a:
                for text in st.session_state.words[:4]:
                    if st.button(text):
                        handle_text_chosen(text)
            with col1b:
                for text in st.session_state.words[4:]:
                    if st.button(text):
                        handle_text_chosen(text)

    with col2:
        cont2 = st.container(border=True)
        with cont2:
            col2a, col2b = st.columns(2)
            with col2a:
                for text in st.session_state.sentences[:3]:
                    if st.button(text):
                        handle_text_chosen(text)
            with col2b:
                for text in st.session_state.sentences[3:]:
                    if st.button(text):
                        handle_text_chosen(text)


col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 1, 1, 10, 1, 1, 1])
with col3:
    if st.button("🔄", key='left_ref'):
        refresh_button(True)
with col4:
    if st.button("👍", key='left_tu'):
        thumbs_up_button(True)
with col5:
    if st.button("👎", key='left_td'):
        thumbs_down_button(True)
with col7:
    if st.button("🔄", key='right_ref'):
        refresh_button(False)
with col8:
    if st.button("👍", key='right_tu'):
        thumbs_up_button(False)
with col9:
    if st.button("👎", key='right_td'):
        thumbs_down_button(False)



# text bar and submit button
with st.form('chat_input_form'):
    text_bar_col1, text_bar_col2 = st.columns([13, 1])

    with text_bar_col1:
        prompt = st.text_input(label="Insert text here", value=st.session_state.message_input,
                               label_visibility='collapsed',
                               placeholder="Start Writing...")
    with text_bar_col2:
        submitted = st.form_submit_button('⬆')

    if prompt and submitted:
        st.write(
            f'{random.choice(["Amazing!", "Awesome!", "Incredible!", "Good on ya!"])}  \nYou were able to create the sentence: "{prompt}"  \n 👏🏻 👏🏻 👏🏻')
        st.balloons()
        st.session_state.message_input = ""

# Mood slider at the bottom
mood = st.select_slider("How are you feeling today?", ["😄", "😊", "😐", "😔", "😭"], key="mood", value="😐")
sac.segmented(
    items=[
        sac.SegmentedItem(icon='mic'),
        sac.SegmentedItem(icon='eye'),
        sac.SegmentedItem(icon='keyboard'),
    ], size=20, radius=50, align='center', use_container_width=True, index=1, key='input_type', return_index=True)

if st.session_state["input_type"] == 1:
    st.header('Eye Input')

st.header("Debug:")
st.write(st.session_state)