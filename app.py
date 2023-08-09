from flask import Flask, render_template, request
import numpy as np
import requests as rq
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    message = request.form['message']

    #word counter threshold
    word_count = len(message.split())

    if word_count > 250:
        return render_template('index.html', message=message, word_count_error=True)

    BASE_URL='http://detectai.pythonanywhere.com/'
    payload={'input':message}
    response=rq.get(BASE_URL,params=payload)
    json_values=response.json()

    prediction=json_values['prediction']
    probability=json_values['probability']

    print(prediction[0])


    prob_percentage_0 = probability[0][0] * 100
    prob_percentage_1 = probability[0][1] * 100
    prob_percentage_0_formatted = "{:.2f}".format(prob_percentage_0)
    prob_percentage_1_formatted = "{:.2f}".format(prob_percentage_1)
    print(prob_percentage_0_formatted)
    print(prob_percentage_1_formatted)

    return render_template('index.html', prediction=prediction[0], message=message, prob_percentage_0_formatted=prob_percentage_0_formatted, prob_percentage_1_formatted=prob_percentage_1_formatted)

if __name__ == '__main__':
    app.run(debug=True)