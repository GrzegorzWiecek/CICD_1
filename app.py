import os
from flask import Flask, render_template, request
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from PIL import Image
import numpy as np
from google import genai
from dotenv import load_dotenv

load_dotenv()
# The client gets the API key from the environment variable `GEMINI_API_KEY`.


data = load_digits()
X, y = data.data, data.target

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    digit = None
    if request.method == 'POST':
        file = request.files['image']
        img = Image.open(file).convert('L')
        img = img.resize((8,8))
        data = np.array(img)
        # print(data)
        data = 16 - data / 255 * 16
        # print(data)
        data = data.flatten().reshape(1,-1)
        # print(data)
        digit = model.predict(data)[0]
        # print(digit)

    return render_template("digits.html", digit=digit)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    response_text = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model="gemini-3-flash-preview", contents=prompt
        )
        response_text = response.text
        #print(response.text)
    return render_template('chat.html', response=response_text)

@app.route('/add', methods=['GET', 'POST'])
def add():
    a = b = suma = None
    if request.method == 'POST':
        a = int(request.form['a'])
        b = int(request.form['b'])
        suma = a + b

    return render_template('index.html', a=a, b=b, s=suma)

if __name__ == '__main__':
    app.run(debug=True)