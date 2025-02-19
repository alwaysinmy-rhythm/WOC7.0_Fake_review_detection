# WOC7.0_Fake_review_detection
# Fake Review Detection Web Application

## Motive for the Project

In the AI-driven world, computer-generated reviews have increased significantly. This website aims to help customers by analyzing Amazon product reviews and detecting whether they are human-written or AI-generated. By scanning reviews with an ML model, users can make informed decisions before purchasing products.

## Work Flow

1.  Enter an Amazon product URL.
2.  The website scrapes all reviews using Selenium.
3.  Reviews are preprocessed for analysis.
4.  The ML model (SVM) scans the reviews and classifies them as human-written or computer-generated.
5.  The classified reviews are displayed on the website.

## Technology Used

*   Flask - For building the web application.
*   SVM Model - For classifying reviews.
*   Selenium - For web scraping Amazon reviews.

## Improvements

*   Enhance the preprocessing techniques for better review analysis.
*   Replace SVM with an Artificial Neural Network (ANN) to improve accuracy.
*   Expand the website’s functionality to support other e-commerce platforms beyond Amazon.

## How to Run

1.  Clone this repository.
2.  Install dependencies using:

    ```bash
    pip install -r requirements.txt
    ```

3.  Run the Flask application:

    ```bash
    python app.py
    ```

4.  Open the web browser and enter the product URL to analyze reviews.

## Contributing

Contributions are welcome! Feel free to fork the repo and submit pull requests with improvements or bug fixes.
