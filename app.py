from flask import Flask, request, jsonify, render_template
import Script.model_predict as model_predict
import numpy as np
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins='http://localhost:3000')

model = pickle.load(open(os.path.join("Model","recomm.pickle"), "rb"))
tfidf = pickle.load(open(os.path.join("Model","recomm_fit_transform.pickle"), "rb"))
new_df = pd.read_csv(os.path.join("Data",'final.csv'), index_col=0)


@app.route('/predict', methods = ['POST'])
def predict():
    music = list(request.json.values())[0]
    output = model_predict.predict_song(music, model, new_df, tfidf, cosine_similarity)
    result = {"prediction": model_predict.fetch_image(output)}
    return jsonify(result)

    # return render_template('index.html', prediction_text = model_predict.fetch_image(output))

if __name__ == '__main__': 
    app.run(debug=True)