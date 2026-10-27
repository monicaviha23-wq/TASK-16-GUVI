import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# PAGE OBJECT MODEL (POM) CLASS

class WorldPopulationPage:
    """Page class to store locators and actions for the World Population page."""

    def __init__(self, driver):
        self.driver = driver
        # Defining the XPATH locator properly inside __init__
        self.population_xpath = "//div[contains(@class,'hero-cine__counter')]"

    def open_page(self):
        """Navigates to the given target URL."""
        self.driver.get(
            "https://www.theworldcounts.com/challenges/planet-earth/state-of-the-planet/world-population-clock-live")

    def get_population_count(self):
        """Waits for the population element to be visible and extracts its text using XPATH."""
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.population_xpath))
        )
        return element.text



# PYTEST FIXTURE & TEST CASE

@pytest.fixture
def setup_browser():
    # initialize Chrome driver and tear it down after the test."""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_extract_population_count(setup_browser):
    """Test case to extract the population count successfully and generate report data."""
    driver = setup_browser
    page = WorldPopulationPage(driver)

    # 1) Go to the URL
    page.open_page()

    print("\n--- Population Extraction Started ---")

    # Run for 5 live checks so pytest exits cleanly and records the test result
    for i in range(5):
        population = page.get_population_count()
        assert population is not None, "Failed to retrieve population count."
        print(f"[{i + 1}/5] Current World Population: {population}")
        time.sleep(1)

    print("--- Population Extraction Completed Successfully ---")