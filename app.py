from flask import Flask, render_template, request
import random

app = Flask(__name__)

class MarkovChain:
    def __init__(self):
        self.lookup_dict = {}

    def add_text(self, text):
        words = text.split()
        prev_word = None
        for word in words:
            if prev_word is None:
                self.lookup_dict.setdefault('$start', []).append(word)
            else:
                self.lookup_dict.setdefault(prev_word, []).append(word)
            prev_word = word
        self.lookup_dict.setdefault(prev_word, []).append('$end')

    def generate_text(self):
        current_word = random.choice(self.lookup_dict['$start'])
        text = []
        while current_word != '$end':
            text.append(current_word)
            current_word = random.choice(self.lookup_dict.get(current_word, ['$end']))
        return ' '.join(text)

mc = MarkovChain()

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_text = ""
    if request.method == 'POST':
        text_input = request.form['text_input']
        mc.add_text(text_input)
        generated_text = mc.generate_text()
    return render_template('index.html', generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True)
