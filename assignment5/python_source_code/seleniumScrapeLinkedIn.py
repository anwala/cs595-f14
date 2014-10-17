#credit to:
#https://gist.github.com/leostera/3535568
#https://pypi.python.org/pypi/selenium
#cookies problem: http://stackoverflow.com/questions/7854077/using-a-session-cookie-from-selenium-in-urllib2
#http://stackoverflow.com/questions/14583560/selenium-retrieve-data-that-loads-while-scrolling-down
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import os, sys
from bs4 import BeautifulSoup
import codecs
from random import randint
import getpass
import os


globalCSVOutputFile = 'linkedInFoFCountTuples.txt'


def pleaseSleep():
	sleepTime = randint(3,7)
	print "...sleeping for", sleepTime, "seconds"
	time.sleep(sleepTime)
			

def getFullNameOfUserAndConnectionCount(htmlString):
	
	fullName = ''
	connectionsCount = ''

	if( len(htmlString) > 0 ):

		soup = BeautifulSoup(htmlString)
		fullName = soup.find('span', { 'class' : 'full-name' })
		
		connectionsCount = soup.find('a', { 'class' : 'connections-link' })

		fullName = fullName.text
		connectionsCount = connectionsCount.text

	return fullName, connectionsCount


#write <connection, connectionCount> tuples into globalCSVOutputFile
#returns connection element ids of connections with 500+ connections to be dereferenced
def get2ndDegreeConnectionsFromHTML(connectionsHtml):

	dictionaryOfConnectionsToDereference = {}

	if ( len(connectionsHtml) > 0 ):

		try:
			 
			connectionsOutputFile = codecs.open(globalCSVOutputFile, 'w', 'utf-8')
			connectionsOutputFile.write('"USER", "FRIENDCOUNT"\n')

		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print fname, exc_tb.tb_lineno, sys.exc_info()
			return

		if( len(connectionsHtml) > 0 ):

			soup = BeautifulSoup(connectionsHtml)

			try:
				allConnections = soup.find('ul', { 'class' : 'conx-list' })
				allConnections = allConnections.findAll('li')
			except:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print fname, exc_tb.tb_lineno, sys.exc_info()
			


			indexOfConnection = 0
			for connection in allConnections:

				person = connection.find('input', { 'type' : 'checkbox' })
				#person is of form: <input type="checkbox" value="Marc Abramo Serr"/>

				if( person is not None ):
					person = str(person)
					connectionName = person.split('"')

					#get connection count, name is 3rd position
					if( len(connectionName) > 2 ):
						
						connectionCount = connection.find('div', { 'class' : 'conn-count' })
						connectionCount = connectionCount.text

						#get id
						idOfElement = str(connection)
						indexIdOfElement = idOfElement.find('id="')

						if( indexIdOfElement > -1 ):
							indexIdOfElement = indexIdOfElement + 4
							indexIdOfElementClosingQuotes =	idOfElement.find('"', indexIdOfElement)
							connectionHTMLElementID = idOfElement[indexIdOfElement : indexIdOfElementClosingQuotes]
							
							#print connectionName[3], connectionCount, connectionHTMLElementID + '\n'
							connectionCount = connectionCount.strip()
							if( connectionCount == '500+' ):
								dictionaryOfConnectionsToDereference[connectionName[3]] = connectionHTMLElementID
							else:
								connectionsOutputFile.write( connectionName[3].decode('utf-8') + ', ' + connectionCount +'\n')


			connectionsOutputFile.close()

	return dictionaryOfConnectionsToDereference	

#returns connection count for connection with 500+ connections
def getConnectionCountFor500PlusConnection(htmlString):

	resultCount = 0

	if( len(htmlString) > 0 ):
		soup = BeautifulSoup(htmlString)
		resultCount = soup.find('div', { 'id' : 'results_count' })

		resultCount = resultCount.text.split(' ')
		resultCount = resultCount[0]
		resultCount = resultCount.replace(',','')
	

	return resultCount

#logs into LinkedIn, goes to connections page, and sends the connection page html to get2ndDegreeConnectionsFromHTML
#gets a list of connection element ids of connections with 500+ connections...
def getHtmlOfAllConnections(userLinkedInEmail, userLinkedInPassword):

	if( len(userLinkedInEmail) > 0 and len(userLinkedInPassword) > 0):

		'''
		try:
			outputFile = open('connections.html', 'w')
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print fname, exc_tb.tb_lineno, sys.exc_info()
			return
		'''

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


		#open connections page
		myFirefoxBrowser.implicitly_wait(10) # seconds
		connectionsLink = 'https://www.linkedin.com/people/connections?trk=nav_responsive_tab_network'
		myFirefoxBrowser.get(connectionsLink)
		myFirefoxBrowser.maximize_window()

		

		html = myFirefoxBrowser.page_source.encode('utf-8')


		#outputFile.write(html)
		dictionaryOfConnectionsToDereference = get2ndDegreeConnectionsFromHTML(html)
		#call function to get <friend, friendCount> and get ids of 500+ connection count to be dereferenced

		if( len(dictionaryOfConnectionsToDereference) > 0 ):
			
			try:
				connectionsOutputFile = codecs.open(globalCSVOutputFile, 'a', 'utf-8')
				
			except:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print fname, exc_tb.tb_lineno, sys.exc_info()
				return

			count = len(dictionaryOfConnectionsToDereference)
			for connection, conElementID in dictionaryOfConnectionsToDereference.items():
				pleaseSleep()
				linkToGet = 'http://www.linkedin.com/profile/connections?id=' + conElementID
				myFirefoxBrowser.get(linkToGet)

				html = myFirefoxBrowser.page_source.encode('utf-8')
				connectionCount = getConnectionCountFor500PlusConnection(html)


				#append globalCSVOutputFile
				print "deref:", connection, connectionCount, count
				connectionsOutputFile.write( connection.decode('utf-8') + ', ' + connectionCount +'\n')
				count = count - 1



		connectionsOutputFile.close()
		myFirefoxBrowser.close()


if __name__ == "__main__":

	
	userNameLinkedIn = raw_input("Email ID: ")
	passwordLinkedIn = getpass.getpass('Password: ')

	userNameLinkedIn = str(userNameLinkedIn)
	passwordLinkedIn = str(passwordLinkedIn)

	userNameLinkedIn = userNameLinkedIn.strip()
	passwordLinkedIn = passwordLinkedIn.strip()

	getHtmlOfAllConnections(userNameLinkedIn, passwordLinkedIn)
	print "...Done"



