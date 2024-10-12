from flask import Flask, render_template, request
import pickle
import requests
from bs4 import BeautifulSoup
import numpy as np

app = Flask(__name__)

# Load pre-trained model and vectorizer
clf = pickle.load(open('nlp_model.pkl', 'rb'))
vectorizer = pickle.load(open('tranform.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the movie name from the form input
    movie_name = request.form['movie_name']
    movie_reviews = {}

    try:
        # Construct the URL for IMDb reviews page (replace with actual scraping URL)
        url = f"https://www.imdb.com/search/title/?title={movie_name}"

        # Fetch the page content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract reviews using BeautifulSoup (customize based on actual IMDb structure)
        soup_result = soup.find_all("div", {"class": "text show-more__control"})
        print(f"Scraped reviews: {soup_result}")  # Debugging: Check if reviews are scraped

        # Check if any reviews were found
        if len(soup_result) == 0:
            return render_template('recommend.html', reviews={"error": "No reviews found."})

        # Process each review and make a sentiment prediction
        for reviews in soup_result:
            movie_review = reviews.get_text()  # Extract text from the review
            movie_review_list = np.array([movie_review])
            print(f"Review: {movie_review_list}")  # Debugging: Check each review

            # Transform review text to match model's expected input format
            movie_vector = vectorizer.transform(movie_review_list)
            
            # Predict sentiment using the loaded model
            pred = clf.predict(movie_vector)
            print(f"Predicted sentiment: {pred}")  # Debugging: Check prediction output

            # Map prediction to sentiment
            if pred == 0:
                sentiment = 'Negative'
            elif pred == 1:
                sentiment = 'Positive'
            else:
                sentiment = 'Neutral'

            # Store the review and its sentiment in the dictionary
            movie_reviews[movie_review] = sentiment

        print(f"Movie reviews and sentiments: {movie_reviews}")  # Debugging: Check the final dictionary

    except Exception as e:
        print(f"Error: {e}")  # Debugging: Capture any exceptions
        return render_template('recommend.html', reviews={"error": "An error occurred while fetching reviews."})

    # Pass the reviews and sentiments to the template for rendering
    return render_template('recommend.html', reviews=movie_reviews)

if __name__ == '__main__':
    app.run(debug=True)
