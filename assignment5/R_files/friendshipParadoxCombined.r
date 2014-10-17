#!/usr/bin/env Rscript


rawInputTwitter <- read.csv(file='FoFCountTwitter.csv', head=TRUE, sep=",")
rawInputFacebook <- read.csv(file='FoFCountFacebook.csv', head=TRUE, sep=",")
rawInputLinkedIn <- read.csv(file='FoFCountLinkedIn.csv', head=TRUE, sep=",")

rawInputTwitter$FRIENDCOUNT <- sort(rawInputTwitter$FRIENDCOUNT, decreasing = FALSE)
rawInputFacebook$FRIENDCOUNT <- sort(rawInputFacebook$FRIENDCOUNT, decreasing = FALSE)
rawInputLinkedIn$FRIENDCOUNT <- sort(rawInputLinkedIn$FRIENDCOUNT, decreasing = FALSE)

plot(rawInputTwitter$FRIENDCOUNT, type='l', xlab='Friends', ylab='No. of Friends', main='Chart 4: Friend vs. FriendCount\n(Twitter-Red, Facebook-Green, LinkedIn-Blue)\nTwitter(TR), Facebook(FB), LinkedIn(LI)', col='red')
par(new=TRUE)
plot(rawInputFacebook$FRIENDCOUNT, type='l', xlab='', ylab='', main='', col='green', xaxt='n', yaxt='n')
par(new=TRUE)
plot(rawInputLinkedIn$FRIENDCOUNT, type='l', xlab='', ylab='', main='', col='blue', xaxt='n', yaxt='n')

text(66, 148, "x")#Dr. Nelson is 66th on list
text(65, 15, "Dr. Nelson's Friends (TR): 148")

text(20, 114, "x")#I am 12th in sorted list
text(31, 300, "Alexander's Friends (FB): 114")

text(62, 144, "x")#Jose is 62th on list
text(90, 210, "Jose's Friends (LI): 144")