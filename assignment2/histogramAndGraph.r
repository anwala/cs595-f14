#!/usr/bin/env Rscript

rawInput <- read.table('AGE-MEMENTOCOUNT.txt', header=T)




bins <- seq(0, 21000, 1000)

hist(rawInput$MementoCount, breaks=bins, main="Chart 1: Distribution of URIs", xlab="URIs", col="lightblue")
plot(rawInput$Age, rawInput$MementoCount, log="xy", type="p", xlab="Age", ylab="No. of Mementos", col="dodgerblue1", main="Chart 2: Age vs. Memento Count")

