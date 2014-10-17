#!/usr/bin/env Rscript


rawInput <- read.csv(file='FoFCountLinkedIn.csv', head=TRUE, sep=",")
rawInput$FRIENDCOUNT <- sort(rawInput$FRIENDCOUNT, decreasing = FALSE)

plot(rawInput$FRIENDCOUNT, type='l', xlab='Friends', ylab='No. of Friends', main='Chart 3: Friend vs. FriendCount (LinkedIn)', col='blue')
rawInput$FRIENDCOUNT
meanValue <- mean(rawInput$FRIENDCOUNT)
meanValue
medianValue <- median(rawInput$FRIENDCOUNT)
medianValue
standardDeviationValue <- sd(rawInput$FRIENDCOUNT)
standardDeviationValue


text(62, 144, "x", col = 'red')#Jose is 62th on list
text(83, 115, "Jose's Friends: 144")

text(107, meanValue, 'x', col = 'red')
text(125, meanValue, 'Mean: 288.2414')

text(73, medianValue, 'x', col = 'red')
text(78, medianValue+80, 'Median: 172')

text(132, standardDeviationValue, 'x', col = 'red')
text(135, standardDeviationValue+80, 'SD: 471.4965')



