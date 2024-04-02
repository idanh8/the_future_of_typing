# pip install -q -U google-generativeai
import google.generativeai as genai
import prompts


def process_gemini_response(x):
    sentences = x.split("\n")
    sentences = [x.replace("*", "") for x in sentences]  # drop bold

    if len(sentences[0].split(" ")) > 2:  # phrase prediction
        sentences = ["..." + x[3:] for x in sentences]  # drop the index we defined in the prompt...
    else:
        sentences = [x[3:] for x in sentences]  # drop the index we defined in the prompt...

    # drop the dot at the end of each sentence if appears
    res = []
    for sentence in sentences:
        if sentence[-1] == ".":
            res.append(sentence[:-1])
        else:
            res.append(sentence)

    return res


def prompt_model(model: genai, prompt: str) -> list:
    generation_response = model.generate_content(prompt)

    count = 0
    while (len(generation_response.parts) == 0) and (count < 3):  # model returned empty response, allow 3 retries
        generation_response = model.generate_content(prompt)
        count += 1

    result_list = process_gemini_response(generation_response.text)
    return result_list


def get_word_predictions(model: genai, current_sentence: str, style: str, mood: str, refresh=False, words=None):
    prompt = prompts.get_prompt_for_next_word(current_sentence, style, mood, refresh, words)
    res = prompt_model(model, prompt)
    return res


def get_sentence_predictions(model: genai, current_sentence: str, style: str, mood: str, refresh=False, phrases=None):
    prompt = prompts.get_prompt_for_next_phrases(current_sentence, style, mood, refresh, phrases)
    res = prompt_model(model, prompt)
    return res


def get_first_word_predictions(app_style_index: int):
    apps = ["facebook", "whatsapp", "google", "linkedin"]
    app_style = apps[app_style_index]

    if app_style == "google":
        return ["Youtube", "Facebook", "Weather", "Gmail", "Translate", "Chatgpt"]  # top searches 2023

    if app_style == "facebook":
        return ["The", "In", "What", "It", "This", "I", "There"]

    if app_style == "whatsapp":
        return ["Hello", "How", "Why", "What", "Are", "I", "There"]

    if app_style == "linkedin":
        return ["Celebrating", "Wow", "Why", "What", "Are", "I", "There"]


def get_first_sentence_predictions(app_style_index: int, mood: str):
    apps = ["facebook", "whatsapp", "google", "linkedin"]
    app_style = apps[app_style_index]

    if (mood in ["funny", "happy"]) and (app_style == "whatsapp"):
        return ["Hey there...",
                "Whats up?",
                "Knock knock...",
                "What a beautiful...",
                "Thats amazing...",
                "Good stuff!"]

    if (mood in ["neutral", "serious"]) and (app_style == "whatsapp"):
        return ["Hey there...",
                "Whats up?",
                "I approve...",
                "That is interesting...",
                "I'm not sure...",
                "That's ok."]

    if (mood in ["sad", "angry"]) and (app_style == "whatsapp"):
        return ["No way!",
                "I'm struggling with...",
                "Can you help...",
                "That's not alright.",
                "How could you...",
                "That's not ok."]

    if (mood in ["funny", "happy"]) and (app_style == "facebook"):
        return ["Greetings Facebook friends!",
                "Hello world!",
                "Hi everyone...",
                "Knock knock...",
                "Happy birthday..."]

    if (mood in ["neutral", "serious"]) and (app_style == "facebook"):
        return ["I don't usually...",
                "Hello world!",
                "Hi everyone...",
                "What does everyone think...",
                "Happy birthday...",
                "How do you feel..."]

    if (mood in ["sad", "angry"]) and (app_style == "facebook"):
        return ["I don't usually...",
                "How is it possible...",
                "I am furious...",
                "Why the hell...",
                "Sad birthday...",
                "How do you feel..."]

    if (mood in ["funny", "happy"]) and (app_style == "linkedin"):
        return ["Greetings LinkedIn users!",
                "I am proud...",
                "I am delighted...",
                "Pleased to announce...",
                "Happy to share..."]

    if (mood in ["neutral", "serious"]) and (app_style == "linkedin"):
        return ["Hello LinkedIn users!",
                "I dont usually...",
                "What does everyone think...",
                "It is interesting...",
                "Would like to share..."]

    if (mood in ["sad", "angry"]) and (app_style == "linkedin"):
        return ["I don't usually...",
                "How is it possible...",
                "I am furious...",
                "Who thought of...",
                "I'm disappointed...",
                "Unfortunately, today..."]

    if app_style == "google":
        return ["How to...",
                "Whats the?",
                "Why do...",
                "Are the...",
                "Where are...",
                "Good stuff!"]
