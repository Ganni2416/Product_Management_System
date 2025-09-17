from app import create_app, db
from app.exceptions import register_error_handlers
from app.logger import setup_logging  # Import the logging setup function
from app.scraper import scrape_products  # Your scraper function
from app.crud import save_products  # Function to save products to DB

SCRAPE_URL = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"

# Create the Flask app instance using your factory pattern
app = create_app()

# Set up the application context to initialize DB, error handlers, and run scraper
with app.app_context():
    db.create_all()  # Create database tables if they don't exist
    register_error_handlers(app)  # Register any custom error handlers

    # Run scraper and save scraped products to DB on startup
    products = scrape_products(SCRAPE_URL)
    if products:
        save_products(products)
        app.logger.info(f"Scraped and saved {len(products)} products.")
    else:
        app.logger.warning("No products scraped.")

# Set up logging before running the app
setup_logging(app)  # Configure structured logging for the app

if __name__ == "__main__":
    # Run the Flask app with debug mode on and a fixed port
    app.run(debug=True, port=5000)

