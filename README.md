# ApexPlanet Task 3 — Interactive Deep-Dive Dashboard

This dashboard uses the cleaned Task 1 dataset and extends the Task 2 EDA themes.

## Files
- `app.py` — interactive Streamlit dashboard
- `requirements.txt` — required Python packages
- `data/ApexPlanet_Task1_Cleaned_Dataset.csv` — cleaned dataset used by the dashboard

## Dashboard features
- KPI cards: Total Sales, Unique Orders, Average Sales per Order, Units Sold
- Filters: date, category, city, age group, gender (when those columns exist)
- Charts: sales by category, monthly sales trend, top products, top cities
- Filtered data preview and CSV download

## Publish to get a live link
1. Upload all these files and the `data` folder to a GitHub repository.
2. Sign in to Streamlit Community Cloud at https://share.streamlit.io/.
3. Choose **Create app**, select your repository and branch, and set the main file path to `app.py`.
4. Click **Deploy**. After it finishes, copy the generated `https://....streamlit.app` URL as your live dashboard link.
