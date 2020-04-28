from bs4 import BeautifulSoup
import requests
import tkinter as tk
import pickle
import os
import spacy
from collections import Counter
from spacy.lang.en.stop_words import STOP_WORDS
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import nltk
import numpy as np

# Calculate attributes
def token_word_count(text):
    # Return token count, individual word count, list of words
    token_list = []
    for token in text:
        if len(token)>0:
            if token.is_punct == False:
                token_list.append(token)
    return len(token_list), token_list

def remove_stop_words(token_list):
    filtered_token_list = [token for token in token_list if not token.text.lower() in STOP_WORDS and not token.is_punct]
    return len(filtered_token_list),filtered_token_list

def unique_words(token_list):
    word_list = []
    for token in token_list:
        word_list.append(token.text.lower())
    word_freq = Counter(word_list)
    unique_words = [word for (word, freq) in word_freq.items() if freq==1]
    return len(unique_words), unique_words

def rate_of_words(text):
    #Find rate of words in content
    token_count, token_list = token_word_count(text)
    if token_count != 0:
    
        non_stop_words_len, non_stop_words_tokens = remove_stop_words(token_list)

        # Rate of unique words in content
        unique_tokens, unique_token_list = unique_words(token_list)
        rate_of_unique_words = unique_tokens/token_count

        # Rate of non stop words
        rate_of_non_stop_words = (non_stop_words_len)/token_count

        # Rate of unique non stop words
        unique_non_stop_words, unique_non_stop_words_list = unique_words(non_stop_words_tokens)
        rate_of_unique_non_stop_words = (unique_non_stop_words)/unique_tokens 
        
        return rate_of_unique_words,rate_of_non_stop_words,rate_of_unique_non_stop_words
    else:
        return 0,0,0

# Input normal text
def text_sentiment(text):
    sent = TextBlob(text, analyzer = NaiveBayesAnalyzer())
    positive = sent.sentiment.p_pos
    negative = sent.sentiment.p_neg
    return positive, negative
    
def polarity_subjectivity(text): 
    return TextBlob(text).sentiment.polarity, TextBlob(text).sentiment.subjectivity

def calculate_input_parameters(text):
    nlp = spacy.load("en_core_web_sm")
    rate_of_unique_words,rate_of_non_stop_words,rate_of_unique_non_stop_words = rate_of_words(nlp(text))
    positive, negative = text_sentiment(text)
    polarity, subjectivity = polarity_subjectivity(text)
    return rate_of_unique_words,rate_of_non_stop_words,rate_of_unique_non_stop_words,positive,negative,polarity,subjectivity

def get_timesofindia(entry_url):
    # Get data from times of india
    url = entry_url.get()
    page = requests.get(url)
    soup = BeautifulSoup(page.text,"html.parser")
    title = soup.find("h1", class_="K55Ut")
    body_content = soup.find("div", class_="_3WlLe")
    for span in body_content("span"):
        span.decompose()
    for a in body_content("a"):
        a.decompose()
    return title.get_text(),body_content.get_text() 

def show_data(entry_url):
    title, body = get_timesofindia(entry_url)
    txt.insert(tk.END, "Title: \n"+title +"\n Content:\n"+body)
    button2.pack()

def go_viral(entry_url):
    ls = os.listdir()
    if 'final_model.sav' not in ls:
        os.chdir(os.getcwd()+'/Assets')
    loaded_model = pickle.load(open('final_model.sav', 'rb'))
    title, body = get_timesofindia(entry_url)
    rate_of_unique_words_content,rate_of_non_stop_words_content,rate_of_unique_non_stop_words_content,positive_content,negative_content,polarity_content,subjectivity_content = calculate_input_parameters(body)
    rate_of_unique_words_title,rate_of_non_stop_words_title,rate_of_unique_non_stop_words_title,positive_title,negative_title,polarity_title,subjectivity_title = calculate_input_parameters(title)
    y_pred = loaded_model.predict(np.array([[rate_of_unique_words_content,rate_of_non_stop_words_content,rate_of_unique_non_stop_words_content,positive_content,negative_content,polarity_content,subjectivity_content,rate_of_unique_words_title,rate_of_non_stop_words_title,rate_of_unique_non_stop_words_title,positive_title,negative_title,polarity_title,subjectivity_title]]).reshape(1,14)) 
    if y_pred.round() == 0:
        footer["text"] = "There is a 75% chance that this will not go viral"
    else:
        footer["text"] = "There is a 75% chance that this will go viral"
    footer.pack()

# GUI
window = tk.Tk()
txt = tk.Text(window)
heading = tk.Label(text="News Virality Checker", fg="black", bg="white")
entry_url = tk.Entry()
button1 = tk.Button(text ="Get Data", command= lambda: show_data(entry_url))
button2 = tk.Button(text ="Will it go Viral?", command= lambda: go_viral(entry_url))
footer = tk.Label(text="", fg="black", bg="white")
heading.pack()
entry_url.pack()
button1.pack()
txt.pack()
window.mainloop()