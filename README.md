**A content-based book recommender system built with Flask, using fuzzy string matching and cosine similarity to suggest books based on user input.**
---
*View Live Page*: https://book-recommender-system-x4np.onrender.com
---
# 📚 Book Recommender System

This is a content-based book recommendation web application built using Flask. It suggests books similar to the user's input using fuzzy matching and cosine similarity based on book rating vectors.

## 🔍 Features

- Suggests books based on fuzzy keyword matching
- Cosine similarity is used to find related titles
- Interactive web interface with Flask and HTML templates
- Displays title, author, and book cover image for recommendations

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Libraries:** Pandas, NumPy, FuzzyWuzzy, Scikit-learn
- **Frontend:** HTML (Jinja2 templates)
- **Data:** Preprocessed CSVs and similarity matrix

## 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/sunoy2004/Book_Recommender_System.git
   cd Book_Recommender_System
   ````

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure the following files are in the root directory:**

   * `popular.csv`
   * `book_ratings.csv`
   * `Books.csv`
   * `similarity_scores.csv`

4. **Run the Flask app**

   ```bash
   python app.py
   ```

5. **Open in your browser**

   ```
   http://127.0.0.1:5000/
   ```

## 📂 Project Structure

```
.
├── templates/
│   ├── index.html
│   └── recommend.html
├── app.py
├── popular.csv
├── book_ratings.csv
├── Books.csv
├── similarity_scores.csv
└── requirements.txt
```

## ✨ How It Works

* The system uses FuzzyWuzzy to match user input with close book titles.
* Once matched, it fetches similar books using a precomputed cosine similarity matrix.
* Recommendations are displayed with titles, authors, and book covers.

## 🙌 Contributions

Contributions are welcome! Open issues or submit PRs for improvements or bug fixes.

---
