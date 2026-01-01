RULES = {
    "Food": ["zomato", "swiggy", "restaurant", "cafe"],
    "Shopping": ["amazon", "flipkart", "myntra"],
    "Transport": ["uber", "ola", "metro", "fuel"],
    "Bills": ["electricity", "recharge", "bill"],
}

def rule_based_category(text):
    for category, keywords in RULES.items():
        for kw in keywords:
            if kw in text:
                return category
    return None
