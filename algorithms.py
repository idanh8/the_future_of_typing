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


def get_first_word_predictions():
    return ["The", "In", "What", "It", "This", "I", "There"]


def get_first_sentence_predictions():
    return ["What is the time?",
            "When will the...",
            "Is there a...",
            "My name is...",
            "Good idea!",
            "This is amazing!",
            "Terrible idea..."]
