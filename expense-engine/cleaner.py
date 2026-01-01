import re

def clean_description(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    return text.strip()

def clean_data(df):
    df['clean_desc'] = df['description'].apply(clean_description)
    df = df[df['amount'] < 0]  # Only expenses
    df['amount'] = df['amount'].abs()
    return df
