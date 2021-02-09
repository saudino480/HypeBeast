library(dplyr)
#library(stringi)
library(tidyr)
library(stringr)

temp = list.files(path = "./", pattern="*.csv", full.names = TRUE)
myfiles = lapply(temp, read.csv, header = FALSE, stringsAsFactors = F)


GETHYPE = unique(do.call(rbind, myfiles))

colnames(GETHYPE) = c("Brand", "Description", "Size", "URL", "Old_Price", "Price", "Date", "Old_Date")

temp = GETHYPE

GETHYPE$Brand = as.character(GETHYPE$Brand)

GETHYPE$Old_Price = as.character(GETHYPE$Old_Price)

GETHYPE$Old_Price = lapply(GETHYPE$Old_Price, function(x) as.numeric(gsub("[$]", "", x)))

GETHYPE$Old_Price = unlist(GETHYPE$Old_Price)

GETHYPE$Price = as.character(GETHYPE$Price)

GETHYPE$Price = lapply(GETHYPE$Price, function(x) as.numeric(gsub("[$]", "", x)))

GETHYPE$Price = unlist(GETHYPE$Price)

GETHYPE$Main_brand = lapply(GETHYPE$Main_brand, function(x) gsub("ANTISOCIAL", "ANTI SOCIAL", x))

GETHYPE$Main_brand = unlist(GETHYPE$Main_brand)

testhype = GETHYPE %>%
  separate(Brand, into = 'Main_brand', sep = " × ", extra = 'drop', remove = FALSE)

testhype = testhype %>%
  filter(Price > 5) %>%
  filter(Price < 750)

typeof(testhype1$Old_Price)

testhype$Old_Price = unlist(testhype$Old_Price)

testhype$Price = unlist(testhype$Price)

unwanted_brands = c("AMERICAN VINTAGE", "BAND T SHIRT", "BAND TEE", "BAND TEES", "DESIGNER", "JAPANESE BRAND",
                    "MADE IN USA", "MOVIE", "UNKNOWN")

testhype = testhype %>%
  filter(!(Main_brand %in% unwanted_brands))

testhype$Main_brand[testhype$Main_brand == "ANTISOCIAL SOCIAL CLUB"] = "ANTI SOCIAL SOCIAL CLUB"

write.csv(testhype, file="../hypebeast_working.csv")
