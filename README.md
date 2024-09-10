# Amazon Scraper Project 2024



Description:

This project is designed to make Amazon scraping easier, faster, and more efficient using advanced tools like Playwright and Selectolax. 

You can extract essential product details such as:

- Product title

- Price (including currency symbols)

- High-quality Product Image URL



No complex setup required—simply run the script with a list of ASINs, and you'll get all the data you need in seconds.
More add on will coming 


Key Features:

## - **Efficient Scraping**: The scraper is optimized to handle large lists of ASINs, scraping each product swiftly and accurately.

- **Image Download**: The scraper not only fetches product data but also downloads high-resolution product images for you.

- **Customizable Proxy Support**: Built-in proxy handling ensures you can scrape Amazon safely, even at scale.



Files in this repository:

- **scraper2.py**: This is the main script that handles everything from fetching data to downloading product images.

- **env-virtual1/**: Directory for the virtual environment, ensuring all dependencies are isolated and easily manageable (this folder is ignored by Git).



Usage:

1. **Activate the virtual environment**: 

   Ensure you have all the required dependencies isolated in a virtual environment. If you're new to virtual environments, don't worry—it's as simple as running a single command.

2. **Run the scraper**: 

   Use the provided ASIN list or add your own, and let the scraper do its magic. The script will output product details and download images automatically.

3. **Customize with ease**: 

   Want to scrape more than just titles and prices? The scraper is modular and can be easily adapted to extract additional product details.



## Why This Scraper?

- **Save Time**: Automate product research without manual data entry.

- **No Hassle**: No need for deep technical knowledge—everything is straightforward to set up and run.

- **Scalable**: Whether you're scraping 10 or 1,000 ASINs, this tool is built to scale.

## Les bibliotheques 
pip install playwright
pip install selectolax
pip install requests


Author:

Jerome Fraisse
