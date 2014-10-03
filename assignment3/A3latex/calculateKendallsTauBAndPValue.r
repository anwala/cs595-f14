#!/usr/bin/env Rscript

pageRankVector <- c(1, 2, 2, 2, 2, 3, 3, 3, 3, 3)
tdIdfRankVector <- c(1, 2, 2, 2, 3, 3, 3, 3, 3, 4)

cor.test(pageRankVector, tdIdfRankVector, method="kendall")
