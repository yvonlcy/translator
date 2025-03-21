import gradio as gr
import logging
import os
from langdetect import detect, LangDetectException
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
#OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://192.168.55.26:11434")

MODEL = "gemma3:latest"

# bge-m3:latest
# starcoder2:3b
# llama3.2-vision:latest
# deepseek-r1:70b
# llama3.2:latest
# qwen2.5:latest
# gemma3:latest

# initialize ChatOllama client
chat_model = ChatOllama(base_url=OLLAMA_BASE_URL, model=MODEL)

# Supported languages
LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Cantonese": "zh-Hant-HK",
    "Chinese (Traditional)": "zh-TW",
    "Chinese (Simplified)": "zh-CN",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Italian": "it",
    "Portuguese": "pt",
    "Hindi": "hi",
    "Arabic": "ar",
    "Dutch": "nl",
    "Swedish": "sv",
    "Turkish": "tr",
    "Vietnamese": "vi",
    "Thai": "th"
}

LANG_CODES_TO_NAMES = {v: k for k, v in LANGUAGES.items()}

def call_ollama(prompt):
    try:
        response = chat_model.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        logger.error(f"Error calling ChatOllama: {e}")
        return ""

def detect_language(text):
    try:
        detected_code = detect(text)
        detected_language = LANG_CODES_TO_NAMES.get(detected_code, "English")
        return detected_language
    except LangDetectException:
        prompt = f"Identify the language of this text in one word:\n{text}"
        detected_language = call_ollama(prompt)
        return detected_language if detected_language in LANGUAGES else "English"

def translate_text(text, source_language, target_language):
    if source_language == "Auto Detect":
        source_language = detect_language(text)

    if source_language == target_language:
        return source_language, text

    prompt = (
        f"Translate the following text directly from {source_language} to {target_language} "
        f"without any reasoning, thoughts, or intermediate steps. Only provide the translation:\n{text}"
)

    translated_text = call_ollama(prompt)
    return source_language, translated_text

def swap_languages(source_lang, target_lang, input_text, output_text):
    if source_lang == "Auto Detect":
        return source_lang, target_lang, input_text, output_text
    return target_lang, source_lang, output_text, input_text

def on_input_change(text, source_lang):
    if source_lang == "Auto Detect" and text.strip():
        detected_lang = detect_language(text)
        return gr.update(value=detected_lang), f"Detected: {detected_lang}"
    return gr.update(), ""

# Gradio Interface
with gr.Blocks(title="AI Translator", theme=gr.themes.Soft(primary_hue="blue")) as iface:
    gr.Markdown(f"# 🌐 AI Translator ({MODEL})")

    with gr.Row():
        source_language = gr.Dropdown(LANGUAGES.keys(), value="Auto Detect", label="Source")
        swap_btn = gr.Button("🔄")
        target_language = gr.Dropdown([l for l in LANGUAGES if l != "Auto Detect"], value="Cantonese", label="Target")

    detected_language_display = gr.Markdown("")

    with gr.Row():
        input_text = gr.Textbox(label="Input Text", lines=7, placeholder="Enter text here...", interactive=True)
        output_text = gr.Textbox(label="Output Text", lines=7, placeholder="Translation will appear here...", interactive=True)

    with gr.Row():
        clear_btn = gr.Button("Clear")
        copy_btn = gr.Button("Copy")

    translate_btn = gr.Button("Translate", variant="primary")

    # Event handling
    translate_btn.click(
        translate_text,
        [input_text, source_language, target_language],
        [source_language, output_text]
    )

    swap_btn.click(
        swap_languages,
        [source_language, target_language, input_text, output_text],
        [source_language, target_language, input_text, output_text]
    )

    input_text.change(
        on_input_change,
        [input_text, source_language],
        [source_language, detected_language_display]
    )

    clear_btn.click(lambda: "", None, input_text)
    copy_btn.click(None, inputs=output_text, js="(text) => navigator.clipboard.writeText(text)")


iface.launch()
