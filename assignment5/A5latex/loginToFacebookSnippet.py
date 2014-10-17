...
#Login into Facebook
myFirefoxBrowser = webdriver.Firefox()
myFirefoxBrowser.implicitly_wait(3)
# or you can use Chrome(executable_path="/usr/bin/chromedriver")
myFirefoxBrowser.get("http://www.facebook.org")
assert "Facebook" in myFirefoxBrowser.title

elem = myFirefoxBrowser.find_element_by_id("email")
elem.send_keys(userFaceBookEmail)
elem = myFirefoxBrowser.find_element_by_id("pass")
elem.send_keys(userFaceBookPassword)
elem.send_keys(Keys.RETURN)
...