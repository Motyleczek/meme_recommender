import re
import string
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

import keras

from typing import Dict

def meme_prediction(sentiment_model: keras.Model,
                    all_model: keras.Model, 
                    path_to_img: str) -> Dict[str, int]:
    
    #image preprocessing
    width = 100
    height = 100
    X = []
    path = path_to_img
    img = keras.preprocessing.image.load_img(path,target_size=(width,height,3))
    img = keras.preprocessing.image.img_to_array(img)
    img = img/255.0
    X.append(img)
    X = np.array(X)
    
    prediction = {}
    
    # sentiment
    model_prediction = sentiment_model.predict(X)
    predicted_sentiment = np.argmax(model_prediction)
    dummy_translator_dict = {0: "negative",
                         1: "neutral",
                         2: "positive",
                         3: "very_negative",
                         4: "very_positive"}
    # dummy_translator_dict = {0: 1,
    #                      1: 2,
    #                      2: 3,
    #                      3: 0,
    #                      4: 4}
    prediction["sentiment"] = dummy_translator_dict[predicted_sentiment]
    
    # all else
    helper_dict = {0: "humour",
                    1: "sarcasm",
                    2: "offensive",
                    3: "motivational"}

    humour_dict = {0: "not_funny",
                   1: "funny",
                   2: "very_funny",
                   3: "hilarious"}
    sarcasm_dict = {0: "not_sarcastic",
                   1: "general",
                   2: "twisted_meaning",
                   3: "very_twisted"}
    offensive_dict = {0: "not_offensive",
                   1: "slight",
                   2: "very_offensive",
                   3: "hateful_offensive"}
    motivational_dict = {0: "not_motivational",
                         1: "motivational"}
    encoding_helper_dict = {"humour": humour_dict,
                            "sarcasm": sarcasm_dict,
                            "offensive": offensive_dict,
                            "motivational": motivational_dict}
    model_prediction = all_model.predict(X)
    for i, mini_pred in enumerate(model_prediction):
        pred_class = np.argmax(mini_pred)
        prediction[helper_dict[i]] = encoding_helper_dict[helper_dict[i]][pred_class]
        
    return prediction

if __name__ == "__main__":
    print("loading sent model")
    model_A = keras.models.load_model('model_A.keras')
    print("sent model loaded")
    print("loading all model")
    model_C = keras.models.load_model('model_C.keras')
    print("model all loaded")
    path = "etl_module/motivational_test.jpg"
    prediction = meme_prediction(model_A, model_C, path)
    print(prediction)