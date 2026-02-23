from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException, TranslationNotFound

app = Flask(__name__)

# Supported languages map
LANGUAGES = {
    "auto": "Auto Detect",
    "en": "English",
    "hi": "Hindi",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "ja": "Japanese",
    "zh-CN": "Chinese",
    "ar": "Arabic",
    "pt": "Portuguese",
    "ru": "Russian",
}

@app.route("/", methods=["GET", "POST"])
def home():
    translated_text = ""
    error = None
    source = "auto"
    target = "hi"
    input_text = ""

    if request.method == "POST":
        input_text = request.form.get("text", "").strip()
        source = request.form.get("source", "auto")
        target = request.form.get("target", "hi")

        if not input_text:
            error = "Please enter some text to translate."
        elif source == target and source != "auto":
            error = "Source and target languages cannot be the same."
        elif len(input_text) > 2000:
            error = "Text is too long. Maximum 2000 characters allowed."
        else:
            try:
                translated_text = GoogleTranslator(
                    source=source, target=target
                ).translate(input_text)
            except LanguageNotSupportedException:
                error = "One of the selected languages is not supported."
            except TranslationNotFound:
                error = "Translation could not be found. Please try again."
            except Exception as e:
                error = f"Something went wrong: {str(e)}"

    return render_template(
        "index.html",
        translated_text=translated_text,
        error=error,
        input_text=input_text,
        source=source,
        target=target,
        languages=LANGUAGES,
    )


# Optional: AJAX endpoint for real-time translation (future use)
@app.route("/translate", methods=["POST"])
def translate_api():
    data = request.get_json()
    text = data.get("text", "").strip()
    source = data.get("source", "auto")
    target = data.get("target", "hi")

    if not text:
        return jsonify({"error": "No text provided"}), 400
    if len(text) > 2000:
        return jsonify({"error": "Text too long"}), 400

    try:
        result = GoogleTranslator(source=source, target=target).translate(text)
        return jsonify({"translated": result})
    except LanguageNotSupportedException:
        return jsonify({"error": "Language not supported"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)