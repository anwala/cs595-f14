#!/usr/bin/env Rscript
rawInput <- read.table('BLOG-PAGECOUNT.txt', header=T)
hist(rawInput$PageCountFrequency, main="", xlab="BlogPageCount", col="lightblue")

