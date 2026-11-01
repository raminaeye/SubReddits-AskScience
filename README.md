# AskScience Subreddit Analysis

Explores what makes an r/AskScience post score well, then trains a PyTorch model that predicts a post's score bucket from its title, body and metadata.

## What's inside

- `notebook/Subreddits_Analysis_AskScience.ipynb` has the analysis and model
- `notebook/extracting_comments_from_posts.ipynb` collects comments
- `utils/` holds text helpers

## How to run

```bash
pip install -r requirements.txt "pandas<2" "numpy<2" "scikit-learn<1.6" "sentence-transformers==2.7.0"
jupyter notebook notebook/Subreddits_Analysis_AskScience.ipynb
```

Use Python 3.8 to 3.10.

The notebook needs your own `data/askscience_data.csv`; it is not included. In the first cell, change `pandas_profiling` to `ydata_profiling`.
