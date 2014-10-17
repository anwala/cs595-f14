...
#Login into LinkedIn
userLinkedInEmail = userLinkedInEmail.strip()
userLinkedInPassword = userLinkedInPassword.strip()

myFirefoxBrowser = webdriver.Firefox()
myFirefoxBrowser.implicitly_wait(3)
# or you can use Chrome(executable_path="/usr/bin/chromedriver")
myFirefoxBrowser.get("http://www.linkedin.com/")
assert 'LinkedIn' in myFirefoxBrowser.title

elem = myFirefoxBrowser.find_element_by_id('session_key-login')
elem.send_keys(userLinkedInEmail)
elem = myFirefoxBrowser.find_element_by_id('session_password-login')
elem.send_keys(userLinkedInPassword)
elem.send_keys(Keys.RETURN)

all_cookies = myFirefoxBrowser.get_cookies()
pleaseSleep()
...