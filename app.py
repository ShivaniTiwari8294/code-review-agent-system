from flask import Flask, render_template, request, jsonify
import os
from orchestrator import review_file

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    files = request.files.getlist("files")
    results = []
    for file in files:
        if file and file.filename:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            data = review_file(file_path)
            results.append(data)
    return jsonify(results)


@app.route("/chat", methods=["POST"])
def chat():
    """Simple rule-based assistant for explaining errors"""
    msg = request.json.get("message", "").lower()

    responses = {
        "docstring": "A docstring is a string literal right after a function/class definition that describes what it does. Example: def foo():\\n    \\\"\\\"\\\"This function does X.\\\"\\\"\\\"",
        "trailing whitespace": "Trailing whitespace means extra spaces at the end of a line. Most editors can auto-remove this with 'Trim Trailing Whitespace' on save.",
        "hardcoded password": "Never write passwords directly in code. Instead, store them in environment variables: os.environ.get('PASSWORD')",
        "nested loop": "A nested loop (loop inside a loop) can slow down your program for large inputs. Try using dictionaries or sets to avoid repeated searching.",
        "var": "'var' in JavaScript has function-level scope and can cause bugs. Use 'let' (changeable) or 'const' (constant) instead - they have block-level scope.",
        "console.log": "console.log() is for debugging. Remove these before submitting production code, or use a proper logging library.",
        "eval": "eval() executes code from strings, which is a major security risk if the string comes from user input. Avoid it.",
        "bare except": "A bare 'except:' catches ALL errors, even ones you didn't expect (like KeyboardInterrupt). Always specify: 'except ValueError:' or similar.",
        "score": "Your code quality score is based on issue density: Score = 10 - (issues/lines * 10). Fewer issues per line = higher score!",
        "hello": "Hi! I'm your code review assistant. Ask me about any error type (e.g. 'what is trailing whitespace?') or how scoring works.",
        "hi": "Hello! Ask me about any detected issue and I'll explain it and how to fix it.",
    }

    for key, response in responses.items():
        if key in msg:
            return jsonify({"reply": response})

    return jsonify({"reply": "I can explain issues like: docstrings, trailing whitespace, hardcoded passwords, nested loops, var vs let, console.log, eval, bare except, or how scoring works. Try asking about one of these!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)