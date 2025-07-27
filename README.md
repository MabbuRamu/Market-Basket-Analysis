🛒 Market Basket Analysis Web Application

This is an interactive web application built with Streamlit that performs Market Basket Analysis on transactional data. It helps users discover which products are frequently purchased together by identifying frequent itemsets and generating association rules using the efficient FP-Growth algorithm.

🌟 Overview

Market Basket Analysis is a data mining technique used to uncover associations between items. It works by looking for combinations of items that occur together frequently in transactions. For example, it can reveal that customers who buy bread are also likely to buy milk.

This application provides an easy-to-use interface to:

Upload your own transactional data (in .csv or .xlsx format).

Preprocess and clean the data automatically.

Tune analysis parameters like Minimum Support and Minimum Lift.

View the resulting frequent itemsets and association rules in clear, sortable tables.

This project uses the FP-Growth algorithm from the mlxtend library, which is significantly more memory-efficient and faster than the traditional Apriori algorithm, making it suitable for larger datasets.

✨ Features

Interactive UI: A clean and simple user interface powered by Streamlit.

File Uploader: Supports both CSV and Excel file formats for transaction data.

Dynamic Analysis: Adjust Minimum Support and Minimum Lift parameters on the fly to refine the analysis.

Efficient Backend: Uses the FP-Growth algorithm to handle large datasets without running out of memory.

Clear Results: Displays frequent itemsets and association rules in organized, easy-to-understand tables.

Data Preprocessing: Automatically cleans the data by handling missing values, removing credit transactions, and filtering out negative quantities.

Memory Optimization: Intelligently filters out very infrequent items before analysis to prevent memory errors.

🛠️ Installation and Setup

To run this application on your local machine, please follow these steps.

Prerequisites

Python 3.8 - 3.11

pip (Python package installer)

Step-by-Step Guide

Clone the Repository (or Download the Files)

If you are using Git, clone the repository:

Generated bash
git clone <repository-url>
cd <repository-directory>


Alternatively, just save app.py and requirements.txt in a new folder on your computer.

Create a Virtual Environment (Recommended)

It is highly recommended to create a virtual environment to keep project dependencies isolated.

Generated bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Install Required Libraries

Install all the necessary packages using the requirements.txt file.

Generated bash
pip install -r requirements.txt
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
🚀 How to Run the Application

Once the setup is complete, you can run the application with a single command:

Generated bash
streamlit run app.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Your default web browser will automatically open a new tab with the running application, usually at http://localhost:8501.

📋 How to Use the Application

Upload Data:

Use the sidebar on the left to upload your transactional data.

The file must be in .xlsx or .csv format.

The data must contain at least three columns: InvoiceNo (transaction identifier), Description (product name), and Quantity (number of items bought).

Set Parameters:

Minimum Support: Use the slider to set the minimum support threshold. This value represents the minimum frequency an itemset must have to be considered "frequent". Lower values will find more rules but may include less significant ones.

Minimum Lift: Use the slider to set the minimum lift threshold. Lift measures how much more likely the items are to be purchased together than if they were independent. A lift > 1 indicates a positive correlation.

Analyze Data:

Click the "Analyze Data" button.

The application will process the data and display the results.

Interpret Results:

Frequent Itemsets: This table shows the sets of products that are frequently bought together, along with their support value.

Association Rules: This table shows the rules in the format "If a customer buys {Antecedent}, then they are likely to buy {Consequent}". The lift, confidence, and support metrics help you gauge the strength of each rule.

📂 Project File Structure
Generated code
.
├── app.py              # The main Streamlit application script
├── requirements.txt    # List of Python dependencies
└── README.md           # This file
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
💾 Dataset Information

The application is designed to work with transactional data. The ideal dataset is the Online Retail Dataset from the UCI Machine Learning Repository, which can be downloaded here:

Link: UCI Online Retail Dataset

Your dataset should have a similar structure, with columns for transaction IDs, product descriptions, and quantities.
