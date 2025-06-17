"""
Unit tests for Dash dashboard in Vehicle Speed Violation Detection System.

This file tests the Dash frontend. It uses Selenium or other testing libraries to simulate user interaction with the dashboard and verify its functionality.
"""


import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@pytest.fixture
def driver():
    # Setup WebDriver for testing the Dash frontend
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver')  # Update path as necessary
    driver.get("http://127.0.0.1:8050")  # Localhost Dash app URL
    yield driver
    driver.quit()

def test_dashboard_title(driver):
    # Check if the dashboard title is correct
    title = driver.title
    assert title == "Vehicle Speed Violation Detection Dashboard", f"Expected title 'Vehicle Speed Violation Detection Dashboard', got {title}"

def test_live_feed(driver):
    # Check if the live feed is updating (you can check for an image change or element)
    live_feed = driver.find_element(By.ID, "live-video-feed")
    initial_src = live_feed.get_attribute('src')
    time.sleep(2)  # Allow time for live feed to update
    updated_src = live_feed.get_attribute('src')
    assert initial_src != updated_src, "Live feed should be updating"

def test_violations_table(driver):
    # Test if violations table is populated with data
    violations_table = driver.find_element(By.ID, "violations-table")
    rows = violations_table.find_elements(By.TAG_NAME, "tr")
    assert len(rows) > 1, "There should be at least one violation record in the table"
