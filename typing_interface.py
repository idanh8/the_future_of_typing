import streamlit as st
import algorithms
import random
import streamlit_antd_components as sac
from streamlit_modal import Modal
import time
import google.generativeai as genai
from whisper_speech_to_text import whisper_stt
from api_keys import WHISPER_API_KEY, GEMINI_API_KEY

# https://nicedouble-streamlitantdcomponentsdemo-app-middmy.streamlit.app/


NUM_WORDS = 7
NUM_PHRASES = 5

modal1 = Modal(key="up", title="Thank you for your feedback!")
modal2 = Modal(key="down", title="We're Sorry! Thank you for your feedback")

# Input App - for style, segmented bar
sac.segmented(
    items=[
        sac.SegmentedItem(icon='facebook'),
        sac.SegmentedItem(icon='whatsapp'),
        sac.SegmentedItem(icon='google'),
        sac.SegmentedItem(icon='linkedin'),
    ], size=15, radius=50, align='center', use_container_width=True, key='input_app', index=1, return_index=True)

# session state is the backbone saving variables
if "previous_input" not in st.session_state:
    st.session_state.previous_input = ""

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
    st.session_state.refreshed_words = []
    st.session_state.refreshed_phrases = []
    st.session_state.first = False
    st.session_state.first_recommendation = True
    st.session_state.prev_mood = "neutral"
    st.session_state.prev_app = ' text message conversation'
    st.session_state.emotion = 'neutral'
    st.session_state.need_to_refresh_words = False
    st.session_state.previous_input = []

    # gemini model
    gemini_api_token = GEMINI_API_KEY
    genai.configure(api_key=gemini_api_token)
    model = genai.GenerativeModel('gemini-pro')
    st.session_state.model = model

if st.session_state.first_recommendation:
    # first recommendation
    st.session_state.first_recommendation = False
    st.session_state.words = algorithms.get_first_word_predictions()
    st.session_state.sentences = algorithms.get_first_sentence_predictions()
    st.rerun()


def refresh_words(app_style=None, spinner_label='Loading inputs...'):
    with st.spinner(spinner_label):
        # time.sleep(3)  # use this if you want to see loading affect if the generation is too quick...
        st.session_state.words = algorithms.get_word_predictions(model=st.session_state.model,
                                                                 current_sentence=st.session_state.message_input,
                                                                 style=app_style,
                                                                 mood=st.session_state.emotion)
        while len(set(st.session_state.words)) != NUM_WORDS:  # solves duplicate button for words
            st.session_state.words = algorithms.get_word_predictions(model=st.session_state.model,
                                                                     current_sentence=st.session_state.message_input,
                                                                     style=st.session_state.app_style,
                                                                     mood=st.session_state.emotion)

        st.session_state.sentences = algorithms.get_sentence_predictions(model=st.session_state.model,
                                                                         current_sentence=st.session_state.message_input,
                                                                         style=app_style,
                                                                         mood=st.session_state.emotion)
        while len(set(st.session_state.sentences)) != NUM_PHRASES:  # solves duplicate button for words
            st.session_state.sentences = algorithms.get_sentence_predictions(model=st.session_state.model,
                                                                             current_sentence=st.session_state.message_input,
                                                                             style=st.session_state.app_style,
                                                                             mood=st.session_state.emotion)
    st.session_state.need_to_refresh_words = False
    st.rerun()


if st.session_state.need_to_refresh_words:
    refresh_words(st.session_state.app_style)


def handle_text_chosen(text, from_whisper=False):
    text_to_add = text.replace(".", "")
    if st.session_state.message_input == "":
        st.session_state.message_input += text_to_add
    else:
        st.session_state.message_input += (" " + text_to_add)

    # Define predictive text options
    display_loading_text = ""
    if from_whisper:
        display_loading_text = "Processing recording..."
    else:
        display_loading_text = 'Loading inputs...'
    with st.spinner(display_loading_text):
        # time.sleep(3)  # use this if you want to see loading affect if the generation is too quick...
        st.session_state.words = algorithms.get_word_predictions(model=st.session_state.model,
                                                                 current_sentence=st.session_state.message_input,
                                                                 style=st.session_state.app_style,
                                                                 mood=st.session_state.emotion)

        while len(set(st.session_state.words)) != NUM_WORDS:  # solves duplicate button for words
            st.session_state.words = algorithms.get_word_predictions(model=st.session_state.model,
                                                                     current_sentence=st.session_state.message_input,
                                                                     style=st.session_state.app_style,
                                                                     mood=st.session_state.emotion)

        st.session_state.sentences = algorithms.get_sentence_predictions(model=st.session_state.model,
                                                                         current_sentence=st.session_state.message_input,
                                                                         style=st.session_state.app_style,
                                                                         mood=st.session_state.emotion)
        while len(set(st.session_state.sentences)) != NUM_PHRASES:  # solves duplicate button for words
            st.session_state.sentences = algorithms.get_sentence_predictions(model=st.session_state.model,
                                                                             current_sentence=st.session_state.message_input,
                                                                             style=st.session_state.app_style,

                                                                             mood=st.session_state.emotion)
    st.session_state.refreshed_words = []
    st.session_state.refreshed_phrases = []
    st.success('Done!')  # because of the rerun we are not seeing this pop up...
    st.rerun()


def update_message_input(new_text):
    st.session_state.message_input = new_text


def handle_click(key):
    # Handle the key press event here
    st.text_input("You pressed:", key)


def refresh_button(words=True):
    if words:
        st.session_state.refreshed_words.append(st.session_state.words)
        with st.spinner(''):
            st.session_state.words = algorithms.get_word_predictions(model=st.session_state.model,
                                                                     current_sentence=st.session_state.message_input,
                                                                     style=st.session_state.app_style,
                                                                     mood=st.session_state.emotion,
                                                                     refresh=True,
                                                                     words=st.session_state.refreshed_words)
            while len(set(st.session_state.words)) != NUM_WORDS:  # solves duplicate button for words
                st.session_state.words = algorithms.get_word_predictions(model=st.session_state.model,
                                                                         current_sentence=st.session_state.message_input,
                                                                         style=st.session_state.app_style,
                                                                         mood=st.session_state.emotion,
                                                                         refresh=True,
                                                                         words=st.session_state.refreshed_words)


    else:
        st.session_state.refreshed_phrases.append(st.session_state.sentences)
        with st.spinner(''):
            st.session_state.sentences = algorithms.get_sentence_predictions(model=st.session_state.model,
                                                                             current_sentence=st.session_state.message_input,
                                                                             style=st.session_state.app_style,
                                                                             mood=st.session_state.emotion,
                                                                             refresh=True,
                                                                             phrases=st.session_state.refreshed_phrases)
        while len(set(st.session_state.sentences)) != NUM_PHRASES:  # solves duplicate button for words
            st.session_state.sentences = algorithms.get_sentence_predictions(model=st.session_state.model,
                                                                             current_sentence=st.session_state.message_input,
                                                                             style=st.session_state.app_style,
                                                                             mood=st.session_state.emotion,
                                                                             refresh=True,
                                                                             phrases=st.session_state.refreshed_phrases)
    st.success('Done!')  # because of the rerun we are not seeing this pop up...
    st.rerun()


def handle_backspace(text):
    words = text.split()
    if words:
        words.pop()
        updated_text = " ".join(words)
        return updated_text
    else:
        return ""


# defining app_style from segmented slider
if st.session_state["input_app"] == 0:
    st.session_state.app_style = ' facebook social media post'
    if st.session_state.prev_app != st.session_state.app_style:
        st.session_state.prev_app = st.session_state.app_style
        st.session_state.need_to_refresh_words = True
        st.rerun()

elif st.session_state["input_app"] == 1:
    st.session_state.app_style = ' text message conversation'
    if st.session_state.prev_app != st.session_state.app_style:
        st.session_state.prev_app = st.session_state.app_style
        st.session_state.need_to_refresh_words = True
        st.rerun()

elif st.session_state["input_app"] == 2:
    st.session_state.app_style = ' search query'
    if st.session_state.prev_app != st.session_state.app_style:
        st.session_state.prev_app = st.session_state.app_style
        st.session_state.need_to_refresh_words = True
        st.rerun()

elif st.session_state["input_app"] == 3:
    st.session_state.app_style = ' professional linkedin post'
    if st.session_state.prev_app != st.session_state.app_style:
        st.session_state.prev_app = st.session_state.app_style
        st.session_state.need_to_refresh_words = True
        st.rerun()

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

# Bottom buttons layout
col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 1, 1, 10, 1, 1, 1])
with col3:
    if st.button("🔄", key='left_ref'):
        refresh_button(True)
with col4:
    if st.button("👍", key='left_tu'):
        modal1.open()
with col5:
    if st.button("👎", key='left_td'):
        modal2.open()
with col7:
    if st.button("🔄", key='right_ref'):
        refresh_button(False)
with col8:
    if st.button("👍", key='right_tu'):
        modal1.open()
with col9:
    if st.button("👎", key='right_td'):
        modal2.open()

# thumbs up and down button popups
if modal1.is_open():
    with modal1.container():
        st.write("Feel free to provide more feedback by writing to us at jacob.link@campus.technion.ac.il.")
        st.write("Please close the popup to return to the typing screen.")
if modal2.is_open():
    with modal2.container():
        st.write("Feel free to provide more feedback by writing to us at jacob.link@campus.technion.ac.il.")
        st.write("You can always get new suggestions by clicking the refresh button.")
        st.write("Please close the popup to return to the typing screen.")

# text bar and submit button
with st.form('chat_input_form'):
    text_bar_col1, text_bar_col2, text_bar_col3 = st.columns([13, 1, 1])

    with text_bar_col1:
        prompt = st.text_input(label="Insert text here", value=st.session_state.message_input,
                               label_visibility='collapsed',
                               placeholder="Start Writing...")
    with text_bar_col2:
        if st.form_submit_button("🔙"):
            updated_text = handle_backspace(st.session_state.message_input)
            st.session_state.message_input = updated_text
            refresh_words(spinner_label='')

    with text_bar_col3:
        submitted = st.form_submit_button('⬆')

    if prompt and submitted:
        st.write(
            f'{random.choice(["Amazing!", "Awesome!", "Incredible!", "Good on ya!"])}  \nYou were able to create the sentence: "{prompt}"  \n 👏🏻 👏🏻 👏🏻')
        st.balloons()
        st.session_state.previous_input.append(st.session_state.message_input)
        st.session_state.message_input = ""
        st.session_state.first_recommendation = True
        time.sleep(5)
        st.rerun()

# Mood slider at the bottom
mood = st.select_slider("How are you feeling today?", ["😭", "😔", "😐", "😊", "😄"], key="mood", value="😐")

if mood == "😄":
    st.session_state.emotion = 'overjoyed'
    if st.session_state.prev_mood != st.session_state.emotion:
        st.session_state.prev_mood = st.session_state.emotion
        refresh_words()
elif mood == "😊":
    st.session_state.emotion = 'happy'
    if st.session_state.prev_mood != st.session_state.emotion:
        st.session_state.prev_mood = st.session_state.emotion
        refresh_words()
elif mood == "😐":
    st.session_state.emotion = 'neutral'
    if st.session_state.prev_mood != st.session_state.emotion:
        st.session_state.prev_mood = st.session_state.emotion
        refresh_words()
elif mood == "😔":
    st.session_state.emotion = 'sad'
    if st.session_state.prev_mood != st.session_state.emotion:
        st.session_state.prev_mood = st.session_state.emotion
        refresh_words()
elif mood == "😭":
    st.session_state.emotion = 'devastated'
    if st.session_state.prev_mood != st.session_state.emotion:
        st.session_state.prev_mood = st.session_state.emotion
        refresh_words()

# Input Type
sac.segmented(
    items=[
        sac.SegmentedItem(icon='mic'),
        sac.SegmentedItem(icon='eye'),
    ], size=20, radius=50, align='center', use_container_width=True, index=1, key='input_type', return_index=True)

if st.session_state['input_type'] == 0:
    whisper_text = whisper_stt(openai_api_key=WHISPER_API_KEY, language='en', just_once=True)

    if whisper_text:
        if whisper_text == "Recording too long, keep recordings less than 10 seconds":
            st.write(whisper_text)
        else:
            if st.session_state.message_input == "":
                handle_text_chosen(whisper_text, from_whisper=True)
            else:
                handle_text_chosen(whisper_text.lower(), from_whisper=True)

col10, col11, col12 = st.columns([5, 5, 5])
with col11:
    chat_history = st.session_state.previous_input[::-1]
    with st.popover("Chat History", use_container_width=True):
        for sentence in chat_history:
            st.write(sentence)

st.header("Debug:")
st.write(st.session_state)
