from selenium import webdriver

browser = webdriver.Firefox()
browser.get("https://localhost")

assert "All courses" in browser.title
print('OK')

