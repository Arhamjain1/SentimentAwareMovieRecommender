import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pickle

# Load your data
data = pd.read_csv('main_data.csv')  # Ensure the path to your CSV file is correct

# Create a CountVectorizer and fit it on your data
cv = CountVectorizer()
count_matrix = cv.fit_transform(data['comb'])  # Replace 'comb' with the appropriate column name

# Create and fit the TfidfTransformer
tfidf_transformer = TfidfTransformer()
tfidf_matrix = tfidf_transformer.fit_transform(count_matrix)

# Save the CountVectorizer and TfidfTransformer to disk
with open('tranform.pkl', 'wb') as f:
    pickle.dump(cv, f)

with open('tfidf_transformer.pkl', 'wb') as f:
    pickle.dump(tfidf_transformer, f)

print("CountVectorizer and TfidfTransformer have been saved.")
