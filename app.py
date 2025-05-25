# from flask import Flask, render_template, request
# import pandas as pd
# import numpy as np
# from fuzzywuzzy import fuzz, process



# # Load data from CSV files
# popular_df = pd.read_csv('popular.csv')
# pt = pd.read_csv('book_ratings.csv', index_col=0)  # Assuming pt.csv has an index column
# books = pd.read_csv('Books.csv')
# similarity_scores = np.loadtxt('similarity_scores.csv', delimiter=',')  # Assuming a 2D matrix

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html',
#                            book_name=list(popular_df['Book-Title'].values),
#                            author=list(popular_df['Book-Author'].values),
#                            image=list(popular_df['Image-URL-M'].values),
#                            votes=list(popular_df['num_ratings'].values),
#                            rating=list(popular_df['avg_rating'].values)
#                            )

# @app.route('/recommend')
# def recommend_ui():
#     return render_template('recommend.html')



# @app.route('/recommend_books', methods=['POST'])
# def recommend():
#     user_input = request.form.get('user_input').strip()

#     if not user_input:
#         return render_template('recommend.html', data=[], message="Please enter a book name.")

#     titles = list(pt.index)

#     # Use token_set_ratio for robust keyword matching
#     scored_titles = [(title, fuzz.token_set_ratio(user_input, title)) for title in titles]

#     # Filter and sort matches by score
#     good_matches = sorted([t for t in scored_titles if t[1] >= 60], key=lambda x: x[1], reverse=True)[:5]

#     if not good_matches:
#         return render_template('recommend.html', data=[], message="No similar books found.")

#     all_recommendations = []

#     for matched_title, score in good_matches:
#         try:
#             index = np.where(pt.index == matched_title)[0][0]
#         except IndexError:
#             continue

#         similar_items = sorted(
#             list(enumerate(similarity_scores[index])),
#             key=lambda x: x[1],
#             reverse=True
#         )[1:5]

#         recommended_books = []
#         for i in similar_items:
#             book_title = pt.index[i[0]]
#             temp_df = books[books['Book-Title'].str.lower() == book_title.lower()]
#             temp_df = temp_df.drop_duplicates('Book-Title')

#             if not temp_df.empty:
#                 recommended_books.append({
#                     'title': temp_df['Book-Title'].values[0],
#                     'author': temp_df['Book-Author'].values[0],
#                     'image': temp_df['Image-URL-M'].values[0]
#                 })

#         all_recommendations.append({
#             'matched_title': matched_title,
#             'recommendations': recommended_books
#         })

#     return render_template('recommend.html', data=all_recommendations)


# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

import os

# Initialize app and CORS
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Load data
popular_df = pd.read_csv('popular.csv')
pt = pd.read_csv('book_ratings.csv', index_col=0)
books = pd.read_csv('Books.csv')
similarity_scores = np.loadtxt('similarity_scores.csv', delimiter=',')

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input', '').strip()

    if not user_input:
        return render_template('recommend.html', data=[], message="Please enter a book name.")

    titles = list(pt.index)
    scored_titles = [(title, fuzz.token_set_ratio(user_input, title)) for title in titles]
    good_matches = sorted([t for t in scored_titles if t[1] >= 60], key=lambda x: x[1], reverse=True)[:5]

    if not good_matches:
        return render_template('recommend.html', data=[], message="No similar books found.")

    all_recommendations = []

    for matched_title, _ in good_matches:
        try:
            index = np.where(pt.index == matched_title)[0][0]
        except IndexError:
            continue

        similar_items = sorted(
            list(enumerate(similarity_scores[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:5]

        recommended_books = []
        for i in similar_items:
            book_title = pt.index[i[0]]
            temp_df = books[books['Book-Title'].str.lower() == book_title.lower()].drop_duplicates('Book-Title')
            if not temp_df.empty:
                recommended_books.append({
                    'title': temp_df['Book-Title'].values[0],
                    'author': temp_df['Book-Author'].values[0],
                    'image': temp_df['Image-URL-M'].values[0]
                })

        all_recommendations.append({
            'matched_title': matched_title,
            'recommendations': recommended_books
        })

    return render_template('recommend.html', data=all_recommendations)

# OPTIONAL: API endpoint to be called from Vercel frontend via fetch()
@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    data = request.get_json()
    user_input = data.get('user_input', '').strip()

    if not user_input:
        return jsonify({'message': 'Please enter a book name.', 'data': []})

    titles = list(pt.index)
    scored_titles = [(title, fuzz.token_set_ratio(user_input, title)) for title in titles]
    good_matches = sorted([t for t in scored_titles if t[1] >= 60], key=lambda x: x[1], reverse=True)[:5]

    if not good_matches:
        return jsonify({'message': 'No similar books found.', 'data': []})

    all_recommendations = []

    for matched_title, _ in good_matches:
        try:
            index = np.where(pt.index == matched_title)[0][0]
        except IndexError:
            continue

        similar_items = sorted(
            list(enumerate(similarity_scores[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:5]

        recommended_books = []
        for i in similar_items:
            book_title = pt.index[i[0]]
            temp_df = books[books['Book-Title'].str.lower() == book_title.lower()].drop_duplicates('Book-Title')
            if not temp_df.empty:
                recommended_books.append({
                    'title': temp_df['Book-Title'].values[0],
                    'author': temp_df['Book-Author'].values[0],
                    'image': temp_df['Image-URL-M'].values[0]
                })

        all_recommendations.append({
            'matched_title': matched_title,
            'recommendations': recommended_books
        })

    return jsonify({'message': 'Success', 'data': all_recommendations})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
# To run the app, use the command: python app.py