# Expense Categorizer

Expense Categorizer is a production-oriented expense analysis application that automatically categorizes personal bank transactions and visualizes spending patterns using a clean, modern interface.

The system is designed with a configuration-driven rule engine and real-world merchant coverage, making it easy to extend and maintain.

---

## Features

- Upload bank statements in CSV format
- Automatic expense categorization using configurable rules
- Broad merchant coverage across groceries, food delivery, shopping, transport, utilities, and subscriptions
- Monthly filtering of transactions
- Category-wise and total spend analytics
- User feedback loop to suggest categories for unmatched transactions
- Export categorized transactions as CSV
- Responsive, mobile-friendly UI
- Light and dark theme support

---

## Categorization Logic

- Transaction descriptions are cleaned and normalized
- Categorization is performed using rule-based keyword matching
- Rules are externalized in `categories.json` for easy updates
- Transactions that do not match any rule are labeled as `Others`
- Users can manually suggest categories for unmatched transactions

---