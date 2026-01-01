def categorize(df):
    categories = []

    for _, row in df.iterrows():
        rule_cat = rule_based_category(row['clean_desc'])
        categories.append(rule_cat if rule_cat else "Others")

    df['category'] = categories
    return df
