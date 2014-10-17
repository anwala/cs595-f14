...
#open friends page
friendsLink = 'https://www.facebook.com/friends/'
myFirefoxBrowser.get(friendsLink)
myFirefoxBrowser.maximize_window()

#scroll to bottom of page
previousCountOfFriends = -1
while True:

	myFirefoxBrowser.execute_script("return window.scrollTo(0, document.body.scrollHeight);")
	html = myFirefoxBrowser.page_source.encode('utf-8') 

	soup = BeautifulSoup(html)
	parentOfUIProfileBlockContent = soup.findAll('div', { 'class' : 'uiProfileBlockContent' })

	#lastIndexOfFriends = html.rfind('<div class="uiProfileBlockContent">')
	lastIndexOfFriends = len(parentOfUIProfileBlockContent)

	#'Friends' not found
	if( lastIndexOfFriends == -1 ):
		break

	#No new entry
	if( previousCountOfFriends == lastIndexOfFriends ):
		htmlOutputFile.write(html)
		break
	else:
		previousCountOfFriends = lastIndexOfFriends

	sleepTime = randint(3,7)
	print "...sleeping for", sleepTime, "seconds"
	time.sleep(sleepTime)
...