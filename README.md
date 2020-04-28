# News/Article-Virality-Prediction

***Note: Currently scrapes only Times of India site***</br>

### Requirements
```
BeautifulSoup
requests
tkinter
pickle
spacy
textblob
sklearn
pandas
numpy
matplotlib
```
### Files
jupyter notebook --> check data extraction & model selection</br>
main.py --> run with python3 with all the dependecies </br>

## Steps Involved
1. Extract data from the dataset</br>
2. Prepare Data</br>
3. Test various ML algorithms on the data</br>
4. Select the best performing algorithm</br>
5. Deploy the application with the algorithm</br>

Steps 1,2,3,4 are done in the jupyter notebook.</br>

## Data Extraction & Preparation
Dataset used: https://webhose.io/free-datasets/popular-news-articles/ </br>
**Multiprocessing was used to extract the data from the content which can be checked in the notebook.** All available processors were used to create the dataset. </br>

Attributes extracted from the dataset are: 
```
rate_of_unique_words of content and title
rate_of_non_stop_words of content and title
rate_of_unique_non_stop_words of content and title
positive of content and title
negative of content and title
polarity of content and title
subjectivity of content and title
```
***Note: Due to hardware and time limitations could only extract attributes from 10000 files***

## Model Selection
**Attributes shown above will be independent variables & facebook shares will be dependent.**</br>
It is assumed that an article is viral if it crosses 500 shares. </br>
Various models have been tested on the dataset and it has been concluded that ***Linear Regression*** gives the best results.</br>
The model has been exported using pickle for later deployment.

## Article Extraction & Prediction
Only supports Times of India currently</br>
Sample links: </br>
https://timesofindia.indiatimes.com/spotlight/keen-on-getting-an-mba-start-your-journey-this-lockdown/articleshow/75409131.cms</br>
https://timesofindia.indiatimes.com/india/58-die-of-covid-infection-highest-in-a-day-cases-inch-close-to-30000/articleshow/75418782.cms</br>
https://timesofindia.indiatimes.com/city/lucknow/covid-fears-bring-good-fortune-for-astrologers/articleshow/75419977.cms</br>
https://timesofindia.indiatimes.com/city/meerut/up-man-kills-two-sadhus-near-temple-in-bulandshahr/articleshow/75420956.cms</br>

## Output
Predicts article is viral if it predicts more than 500 shares

### Improvements that can be done
1. Better hardware to create a better dataset
2. More available data
3. Use more algorithms like spam detection to detect spam score 
4. Use performace metrics from the publisher site
