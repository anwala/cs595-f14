#!/usr/bin/env Rscript


rawInput <- read.csv(file='FoFCountFacebook.csv', head=TRUE, sep=",")
rawInput$FRIENDCOUNT <- sort(rawInput$FRIENDCOUNT, decreasing = FALSE)

plot(rawInput$FRIENDCOUNT, type='l', xlab='Friends', ylab='No. of Friends', main='Chart 2: Friend vs. FriendCount (Facebook)', col='blue')
rawInput$FRIENDCOUNT[12]
meanValue <- mean(rawInput$FRIENDCOUNT)
meanValue
medianValue <- median(rawInput$FRIENDCOUNT)
medianValue
standardDeviationValue <- sd(rawInput$FRIENDCOUNT)
standardDeviationValue


text(12, 114, "x", col = 'red')#I am 12th in sorted list
text(31, 114, "Alexander's Friends: 114")

text(64, meanValue, 'x', col = 'red')
text(82, meanValue, 'Mean: 538.3, SD: 538.4')

text(50, medianValue, 'x', col = 'red')
text(61, medianValue, 'Median: 395')

#text(64, standardDeviationValue, 'x', col = 'red')
#text(68, standardDeviationValue, 'sd: 538.401')



