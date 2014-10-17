#writes tuples <friend, friendCount> into globalCSVOutputFile
def getFriendOfFriendsFromHtml(htmlText):
goAheadFlag = False
if( len(htmlText) > 0 ):
	try:
		outputFile = codecs.open(globalCSVOutputFile, 'w', 'utf-8')
		outputFile.write('"USER", "FRIENDCOUNT"\n')
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print fname, exc_tb.tb_lineno, sys.exc_info()
		return


	soup = BeautifulSoup(htmlText)
	parentOfUIProfileBlockContent = soup.findAll('div', { 'class' : 'uiProfileBlockContent' })

	for profile in parentOfUIProfileBlockContent:

			friendName = profile.find('div', { 'class' : 'fsl fwb fcb' })
			potentialFriendsCount = profile.find('a', { 'class' : 'uiLinkSubtle' })

			#potentialFriendsCount: x (f)riends | x mutual friends, etc, so split
			if( potentialFriendsCount is not None ):

				potentialFriendsCount = potentialFriendsCount.text.split(' ')

				if( len(potentialFriendsCount) > 1 ):
					if( len(potentialFriendsCount[1]) > 0):
						if( potentialFriendsCount[1][0].lower() == 'f' ):

							friendCount = potentialFriendsCount[0].replace(',','')

							stringToWrite = friendName.text + ', ' + friendCount + '\n'
							outputFile.write(stringToWrite)
							goAheadFlag = True
						

	outputFile.close()
return goAheadFlag