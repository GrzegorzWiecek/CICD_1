from flask import Flask, render_template, request
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from PIL import Image
import numpy as np

data = load_digits()
X, y = data.data, data.target

model = RandomForestClassifier(n_estimators=100, random_state=42)
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


if __name__ == '__main__':
    app.run(debug=True)