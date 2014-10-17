...
#Get the count of friends of friends
user = api.get_user(screenName)
friendsCount = str(user._json['friends_count'])
print screenName + ' has ' + friendsCount + ' friends, and '

friendCountFile.write('"USER", "FRIENDCOUNT"\n')
friendCountFile.write(user.name.encode('utf-8') + ', ' + friendsCount + '\n')

for friend in user.friends(count=int(friendsCount)):
	friendsCount = str(api.get_user(friend.screen_name).friends_count)
	print friend.name + ' has ' + friendsCount + ' friends'
	friendCountFile.write(friend.name.encode('utf-8') + ', ' + friendsCount + '\n')
...