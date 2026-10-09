# AskScience Subreddit Analysis

Analysis of r/AskScience Reddit posts to understand what makes a post successful
(high score) and to train a model that predicts a post's score bucket from its
title, body, and metadata.

The project answers two questions:

1. Which post attributes are associated with a higher score (tag, title and
   body length, citation count, number of questions, posting year)?
2. Can a model predict the score of a post from its title, body, and metadata?
   Scores are binned into balanced classes (a classification problem, not
   regression, because the score distribution is heavily skewed), and a
   PyTorch network (RedditNet) classifies each post into one of the score
   buckets using title/body embeddings plus engineered features.

The analysis was run on Python 3.8 with the package versions in
[requirements.txt](requirements.txt).

## Repository structure

- `notebook/Subreddits_Analysis_AskScience.ipynb` - main analysis notebook:
  feature engineering, score distribution study, embedding fine-tuning,
  model training, and evaluation.
- `notebook/extracting_comments_from_posts.ipynb` - downloads post comments
  through the Reddit API and saves them for inspection.
- `utils/data_utility.py` - text cleaning and feature extraction helpers
  (`DataUtil`) used by the main notebook.
- `htmls/` - rendered HTML copies of both notebooks for quick reading.
- `snapshots/` - figures referenced by this README.
- `data/` - not committed to the repo. It holds the raw CSVs, processed
  dataframes, embeddings, and trained model artifacts that the notebooks
  read and write (see "How to run").

## How to run

1. Create a Python environment and install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Place the input files in a local `data/` directory (not tracked by git):
   `askscience_data.csv` for the main notebook. The notebooks write processed
   CSVs, pickles, and model artifacts back into `data/`.

3. Reddit API credentials are required only for the comment extraction
   notebook. Provide them as environment variables; no secrets live in the
   repo:

   ```bash
   export PRAW_REDDIT_CLIENT_ID="<client id>"
   export PRAW_REDDIT_CLIENT_SECRET="<client secret>"
   export PRAW_REDDIT_USER_AGENT="<user agent>"
   ```

4. Run the notebooks in order:

   1. `notebook/Subreddits_Analysis_AskScience.ipynb` - the full analysis
      and model training pipeline.
   2. `notebook/extracting_comments_from_posts.ipynb` - optional comment
      download for qualitative inspection (needs the credentials above).

## What the analysis shows

- Metadata features such as post tag, title length, body length, number of
  questions, and citation count show clearer associations with score than
  author name, day, or month. Posting year is correlated with score in this
  dataset but is not usable for real-time prediction.
- Zero-score posts mostly come from deleted posts or from data captured
  before scores were recorded; they are removed before training.
- Scores are quantized into balanced buckets and predicted with RedditNet,
  which combines title embeddings, body embeddings (max-pooled), and the
  engineered metadata features. A model graph is rendered in
  `snapshots` via the torchviz output in the notebook.

![feature correlation](snapshots/feature_matrix.png)
![tag correlation](snapshots/tag_corr.png)
![citation correlation](snapshots/cite.png)
![score distribution](snapshots/score_dist.png)
![score bins](snapshots/score_bins.png)
![scores after cleanup](snapshots/scores_after.png)
![model architecture](notebook/reddit_torchviz.png)

## Notes

- The LLM-based alternative sketched in the original README (prompting a
  fine-tuned language model to predict scores) was exploratory and is not
  implemented here; the implemented approach is the classifier described
  above.
- Embeddings were fine-tuned from
  [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
  on the post tags as a downstream task.
