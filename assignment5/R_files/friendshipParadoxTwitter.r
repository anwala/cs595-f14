#!/usr/bin/env Rscript


rawInput <- read.csv(file='FoFCountTwitter.csv', head=TRUE, sep=",")
rawInput$FRIENDCOUNT <- sort(rawInput$FRIENDCOUNT, decreasing = FALSE)

plot(rawInput$FRIENDCOUNT, type='l', xlab='Friends', ylab='No. of Friends', main='Chart 1: Friend vs. FriendCount (Twitter)', col='blue')

meanValue <- mean(rawInput$FRIENDCOUNT)
meanValue
medianValue <- median(rawInput$FRIENDCOUNT)
medianValue
standardDeviationValue <- sd(rawInput$FRIENDCOUNT)
standardDeviationValue


text(66, 148, "x", col = 'red')#Dr. Nelson is 66th on list
text(65, 48, "Dr. Nelson's Friends: 148")

text(100, meanValue, 'x', col = 'red')
text(120, meanValue, 'Mean: 404.87')

text(75, medianValue, 'x', col = 'red')
text(93, medianValue, 'Median: 191')

text(113.2, standardDeviationValue, 'x', col = 'red')
text(128, standardDeviationValue, 'SD: 545.02')



