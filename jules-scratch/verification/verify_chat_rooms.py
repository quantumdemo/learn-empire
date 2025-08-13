from playwright.sync_api import sync_playwright, Page, expect
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Seed the database to ensure a clean state
    page.goto("http://127.0.0.1:5000/seed-db")
    expect(page).to_have_title("Home - E-Learning Platform")
    time.sleep(1) # Add a small delay for db write

    # Log in as the student user
    page.goto("http://127.0.0.1:5000/login")
    page.get_by_label("Email").fill("student@example.com")
    page.get_by_label("Password").fill("password")
    page.get_by_role("button", name="Login").click()

    # Take a screenshot right after login attempt to see what's happening
    page.screenshot(path="jules-scratch/verification/login_attempt.png")

    # Wait for the login to complete by waiting for the dashboard URL
    expect(page).to_have_url("http://127.0.0.1:5000/student/dashboard")

    # Now that we are logged in, navigate to the new chat rooms list page
    page.goto("http://127.0.0.1:5000/chat/rooms")

    # Wait for the main content to be visible to ensure the page has loaded
    expect(page.locator(".room-list")).to_be_visible()

    # Take a screenshot of the chat rooms list page
    page.screenshot(path="jules-scratch/verification/chat_rooms_list.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
