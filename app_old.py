app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    a = b = suma = None
    if request.method == 'POST':
        a = int(request.form['a'])
        b = int(request.form['b'])
        suma = a + b

    return render_template('index.html', a=a, b=b, s=suma)

if __name__ == '__main__':
    app.run(debug=True)
