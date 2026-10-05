# Deploying

## Streamlit Community Cloud (free, public demo)
1. Sign in at share.streamlit.io with GitHub and choose **New app**.
2. Repository `Akalabyabissoyi/3r-bridge`, branch `main`, main file `app.py`. Python 3.12.
3. Copy the app URL into the README badge: `[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_URL)`.

Private repositories need access granted to Streamlit in your GitHub settings.

## Docker (institutional or offline use)
```bash
docker build -t 3r-bridge .
docker run -p 8501:8501 3r-bridge
```

## Hugging Face Spaces
Create a Docker Space, push this repository, and set `app_port: 8501` in the Space's README front matter.

## pip
```bash
pip install -e ".[app]"
streamlit run app.py
python -m bridge find --area gut
```
