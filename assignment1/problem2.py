import sys
import commands
import urllib2
from bs4 import BeautifulSoup
from time import sleep
import datetime
#test string: python problem2.py "Old Dominion" 60 "http://sports.yahoo.com/college-football/scoreboard/?week=1&conf=all" > problem2Output.html
defaultTimeIntervalInSeconds = 30.0

def wait(time_lapse):
	time_start = time.time()
	time_end = (time_start + time_lapse)
 
	while time_end > time.time():
		pass

def main():
	if len(sys.argv) != 4:
		print "Usage: ", sys.argv[0] + " <collegeName> <timeInSeconds> <uri> (e.g: " + sys.argv[0] + " Old\ Dominion 60 http://sports.yahoo.com/college-football/scoreboard/)"
		print len(sys.argv)
		return
	elif len(sys.argv) == 4:
		collegeName = sys.argv[1]
		timeInSeconds = sys.argv[2]
		uri = sys.argv[3]


		try:
			timeInSeconds = float(timeInSeconds)
		except:
			print "Error: improper time interval, using default value: ", defaultTimeIntervalInSeconds
			timeInSeconds = defaultTimeIntervalInSeconds

		
		while True:
			#problem1: #Texas A&M; instead of Texas A&M

			#problem2: uri = http://sports.yahoo.com/college-football/scoreboard/?week=1&conf=all returned wrong page!!!
			#consider this encoding: http://sports.yahoo.com/college-football/scoreboard/?week=1&amp;conf=1/, problem may be due to improper encoding
			#consider observation college names with substring format v&v had semicolon ending:Texas A&M; Florida A&M; Alabama A&M;
			#co = 'curl --silent ' + uri
			#page = commands.getoutput(co)

			response = urllib2.urlopen(uri)
			htmlPage = response.read()
			response.close()
			soup = BeautifulSoup(htmlPage)



			#explanation of print soup('table', {"class": "list"})[0].findAll('tr', {"class": "game  link"})[0].findAll('td', {"class": "away"})[0].em.string
			#first parent table => soup('table', {"class": "list"})[0]
			#first parent table(first game link) => soup('table', {"class": "list"})[0].findAll('tr', {"class": "game  link"})[0]
			#first parent table(first game link(first away team)) => soup('table', {"class": "list"})[0].findAll('tr', {"class": "game  link"})[0].findAll('td', {"class": "away"})[0].em.string

			parentScoresTables = soup('table', {"class": "list"})

			for table in parentScoresTables:
				#this is an array
				gameLinks = table.findAll('tr', {"class": "game  link"}) 
				#for live games
				#gameLinks = table.findAll('tr', {"class": "game live link"}) 

				for game in gameLinks:

					awayTeam = game.findAll('td', {"class": "away"})[0].em.string
					awayTeam = str(awayTeam)
					awayTeam = awayTeam.strip()

					homeTeam = game.findAll('td', {"class": "home"})[0].em.string
					
					awayTeamScoreIndexOHomeIndex1 = game.findAll('td', {"class": "score"})[0].findAll('span')
					awayTeamScore = awayTeamScoreIndexOHomeIndex1[0].string
					homeTeamScore = awayTeamScoreIndexOHomeIndex1[1].string

					awayTeamScore = str(awayTeamScore)
					awayTeamScore = awayTeamScore.strip()

					homeTeamScore = str(homeTeamScore)
					homeTeamScore = homeTeamScore.strip()

					#fix for beautiful soup semicolon when ampersand is seen issue:
					#BeautifulSoup parser appends semicolons to naked ampersands, mangling URLs?
					#http://stackoverflow.com/questions/7187744/beautifulsoup-parser-appends-semicolons-to-naked-ampersands-mangling-urls
					if( homeTeam[-1] == ';' ):
						homeTeam = homeTeam[:-1]

					if( awayTeam[-1] == ';' ):
						awayTeam = awayTeam[:-1]

					if(homeTeam.lower() == collegeName.lower() or awayTeam.lower() == collegeName.lower()):
						
						print awayTeam, awayTeamScore + ', ' + homeTeam, homeTeamScore


			print "...sleeping for " + str(timeInSeconds)

			sleep(timeInSeconds)
	
if __name__ == "__main__":
	main()