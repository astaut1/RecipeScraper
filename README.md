# Recipe Scraper

A Python-based recipe web scraper that collects recipe information from **two different websites** — one using static HTML and the other using dynamically loaded content (WordPress).

The project provides a **Tkinter GUI that allows users to enter a recipe URL, scrape the recipe, and modify ingredient amounts according to their desired serving size.

## Technologies Used
* **Python**
* **BeautifulSoup** – for parsing static HTML pages.
* **Selenium Wire** – for interacting with dynamically loaded websites.
* **Selenium** – for browser automation.
* **Tkinter** – for the graphical user interface.
* **Requests** – for making HTTP requests to static websites.

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd recipe-scraper
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Requirements

The project requires Python 3.x and the packages listed in `requirements.txt`.

The main dependencies are:

```text
beautifulsoup4
selenium
selenium-wire
requests
```

Tkinter is normally included with standard Python installations. On some Linux distributions, it may need to be installed separately.

## How to Use

1. Run the main Python file:

```bash
python main.py
```

2. Enter the URL of a recipe from one of the supported websites.

3. Start the scraping process.

4. The application retrieves and displays the recipe.

5. Change the desired serving amount using the GUI.

6. The ingredient quantities are automatically adjusted based on the new serving size.

### Example

If the original recipe is for **4 servings**:

```text
Flour: 200 g
Sugar: 100 g
Milk: 250 ml
```

Changing the serving size to **8 servings** will adjust the ingredients to:

```text
Flour: 400 g
Sugar: 200 g
Milk: 500 ml
```

## Static vs Dynamic Scraping

The project demonstrates two different approaches to web scraping.

### Static Website

For the static website, the scraper sends an HTTP request and uses **BeautifulSoup** to parse the returned HTML.

```text
Website
   ↓
HTTP Request
   ↓
HTML Response
   ↓
BeautifulSoup
   ↓
Recipe Data
```

### Dynamic Website

The dynamic website requires JavaScript to load its recipe information. For this website, **Selenium Wire** is used to control a browser and retrieve content after the page has loaded.

```text
Website
   ↓
Selenium WebDriver
   ↓
JavaScript / Dynamic Content
   ↓
Selenium Wire
   ↓
Recipe Data
```

This allows the project to demonstrate the difference between scraping content that is already present in the HTML and content that is generated or loaded dynamically.

This project is intended for educational purposes and demonstrates web scraping techniques.


