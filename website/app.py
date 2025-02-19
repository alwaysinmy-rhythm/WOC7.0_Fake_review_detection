from flask import Flask, render_template, request ,jsonify

import pickle
import nltk
# nltk.download('stopwords')

# from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

import string 

import gensim
from gensim.models import Word2Vec,KeyedVectors

from amazonReview import loginAmazon, getAmazonReviews

exclude = string.punctuation
def remove_punc(text):
  return text.translate(str.maketrans('', '' , exclude))

# stop_words = set(stopwords.words('english'))
stop_words = {'he', 'all', 'them', 'had', 'during', 'through', 'will', 'more', 'under', "that'll", 'on', 'they', "should've", 'himself', "couldn't", 'be', 'his', 'other', 'herself', 'your', 'then', 'too', 'out', 'have', 'doesn', 'has', 'to', 'wasn', 'each', 'him', "you'd", 'this', "wasn't", 'with', 'our', 'whom', 'yourselves', 'theirs', 'wouldn', 'the', 'only', 'than', 'into', "isn't", "hadn't", 'an', 'such', "haven't", 'isn', 'hasn', 'no', 'where', 'who', 'why', 'few', "shan't", 'weren', "doesn't", 'here', "mustn't", "she's", 'myself', 'but', 'my', 'or', 'don', 'ours', 'own', 'll', 'a', 'ma', 'those', 'before', 'most', 'very', "weren't", 'do', "mightn't", 'being', 'she', 'did', 'between', "won't", 'does', 'd', 'aren', 'yours', 'hadn', 'below', 'as', 'until', 'we', 'am', 'should', 'both', 'at', 'having', 'that', 'were', "shouldn't", 'further', 'shouldn', 'for', 'again', 'couldn', "you're", 're', 'didn', 'while', 'ourselves', 'doing', 'ain', 'me', 's', 'been', 'when', 'any', 'nor', 'shan', 'so', 'once', 'are', 't', 'won', 'not', 'mustn', "it's", 'if', 'is', "don't", 'haven', 'now', 've', "wouldn't", "you've", 'yourself', "you'll", 'their', 'her', 'there', 'was', 'mightn', 'itself', 'against', 'i', 'm', 'you', 'it', 'o', 'can', 'down', 'needn', "needn't", 'just', 'same', 'its', 'from', "aren't", 'by', 'how', 'hers', 'up', "didn't", 'of', 'which', 'in', 'themselves', 'over', 'above', 'what', 'y', 'these', 'because', 'and', 'after', 'some', 'off', "hasn't", 'about'}
def remove_stopwords(text):
    # Replace stopwords with an empty string but preserve spaces
    return " ".join([word if word not in stop_words else '' for word in text.split()])

def give_token(text):
  return word_tokenize(text)

wordnet_lemmatizer = WordNetLemmatizer()
def lemmatize_words(text):
    return [wordnet_lemmatizer.lemmatize(word) for word in text]


with open("./static/vectorize.pkl", "rb") as file:
    model = pickle.load(file)
def get_vector(text):
    return model.get_mean_vector(text)


def process(text):
    text = text.lower()
    text = remove_punc(text)
    text = remove_stopwords(text)
    text = give_token(text)
    text = lemmatize_words(text)
    text = get_vector(text)

    text = text.reshape(1,-1)

    with open("./static/review_model.pkl", "rb") as file : 
        model = pickle.load(file)
    
    pred = model.predict(text)
    return pred 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


reviews = ["As someone who frequently drops this phone, this case has done its job. I don't like how the case comes off fairly easily, but has not ever come off by accident. It has protected my phone from several falls already.", "The case looks nice it's a matted foggy style case. Make sure to choose clear if you want the clar one. You can still the see the design of the phone and it's feels nice. Although it doesn't really feel very protective", "Good quality product, I think it's a little expensive.", "Love this phone the camera is awesome it's an Easy to use it's a light weight phone I love the glyphs the speakers is awesome as well as the ring tones I will recommend this phone", 'Good grip and transparent case.', 'Good quality.', "This case fits the phone perfectly - the cut outs are all exact and even. The frosted white is nice, and if you have the white version of the phone it's maybe twice as milky as the actual back panel. You can still see the design on the back but it definitely makes it a bit more subtle.\n\nThe only thing I don't like is that it adds a bit if thickness to the phone. This case makes the phone a slab, so it adds the thickness that the camera bump is to even out the back. I'm pretty sure it adds at least 1/3rd of the thickness of the phone.\n\nThe buttons are still very nice and clicky, and the protection is probably very good for dropping with the added thickness", "Does the job, let's me enjoy the back design with a bit of protection. Would buy again.", "I'm using it on a black body, but when combined with the sheer feeling of red, it's a burgundy-like color", 'Unlike the Nothing case, this is not a fingerprint magnet. Great case.', 'It fits perfectly well. It has a good grip.', "The cover looks very good, sleek and doesn't get as dirty as the classic transparent ones, it leaves the beautiful design of the phone visible and helps to keep it cleaner. Good material and excellent fit I recommend it.", 'Everything was great', 'I saw his review on NothingForum.com, then decided to take it. Arrived in 1 week with Sendeo. The quality is excellent. A very successful case for Nothing Phone', 'Good quality!', "Nice case, matches the design of the brand. It is slightly transparent, which gives it a chic look. So far so good. Haven't had any drop tests yet.", 'Purchased for my son, as of today it is perfectly preserved and protected', 'But turns yellow quickly', 'Great phone for a great price.', 'This product is good quality and looks fantastic and quick delivery aswell.']


@app.route("/submit", methods=["POST"])
def submit():

    product_url = request.get_json()
    product_url = product_url.get("user_input", "")
    if len(product_url) == 0 : 
        return []
    # print(product_url)
    reviews = getAmazonReviews(product_review_url=product_url)
    # print(len(reviews))
    if reviews == -1 : 
        return jsonify("some thing went wrong!") 
    result = [] 
    for review in reviews:
        pred = process(review)
        result.append({
            "review": review , 
            "pred" : pred[0]    
        })
    print(result)
    return jsonify({"result": result}) # Return JSON response



if __name__ == "__main__":
    login = loginAmazon()
    if(login == -1 ):
        print("failed to login, restart the server!")
    app.run(debug=True,use_reloader=False)

