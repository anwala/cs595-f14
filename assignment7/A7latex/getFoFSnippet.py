#algorithm gen
...
if( len(lines) == 0 ):
	#base case initialize with 1 degree+
	friends = getXFriendsOfFriendsFromTwitter(screenName, maxFriends)
	for friend in friends:
		inputOutputFile.write(userName + globalDelimeter2 + friend + '+\n' )
else:
	#non-base case expand item with smallest plus within tabcount
	mininumPlus = 1000
	item = ''
	itemTabCount = 0
	indexOfItem = -1

	i = 0
	for line in lines:

		plusCount, tabCount = getPlusCountAndTabCount(line)

		#print line.strip(), plusCount, tabCount
		#get minimum plus count which is within the set degree
		if( plusCount != 0 and plusCount < maxDegree ):
			if( plusCount < mininumPlus and tabCount < maxDegree ):
				mininumPlus = plusCount
				item = line
				itemTabCount = tabCount
				indexOfItem = i

		i += 1
	#print item.strip(), itemTabCount, indexOfItem
	if( indexOfItem > -1 ):
		inputOutputFile.close()

		#expand
		try:
			inputOutputFile = open(outputFileName, 'w')
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )
			return
		
		for i in range(0, len(lines)):

			if(i == indexOfItem):

				tabs = str('\t') * itemTabCount
				inputOutputFile.write(tabs + lines[i].strip() + '+\n')

				screenName = lines[i].strip()
				screenName = screenName.split(globalDelimeter)[1]
				screenName = screenName.replace('+','')

				#get userName
				userName = lines[i].strip()
				userName = userName.split(globalDelimeter)[0]
				userName = userName.split(globalDelimeter2)
				userName = userName[-1]

			
				friends = getXFriendsOfFriendsFromTwitter(screenName, maxFriends)

				for friend in friends:

					tabs = str('\t') * (itemTabCount+1)
					inputOutputFile.write( tabs + userName + globalDelimeter2 + friend + '+\n' )
			else:
				inputOutputFile.write(lines[i])
...