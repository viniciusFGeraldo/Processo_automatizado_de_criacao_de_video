from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=r"C:\Users\User\AppData\Local\Google\Chrome\User Data\Default",  
        headless=False,
        executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    )

    page = browser.new_page()
    page.goto("https://luvvoice.com/")
    page.wait_for_timeout(40000)
    browser.close()

    