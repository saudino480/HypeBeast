library(tidyverse)
library(dplyr)
library(ggrepel)

source("../helper.R")

hypebeast = read.csv("../hypebeast_working.csv")
hypebeast = hypebeast %>%
  select(-(X))

hypebeast_summary = hypebeast %>%
  group_by(Main_brand) %>%
  dplyr::summarize(count = n(), SD = sd(Price), MEAN = mean(Price), MEDIAN = median(Price)) %>%
  filter(count > 1000) %>%
  mutate(SE = SD / sqrt(count)) %>%
  mutate(low_mean = MEAN - (SE*1.96), high_mean = MEAN + (SE*1.96))

cheap_brands = c("GILDAN", "FRUIT OF THE LOOM", "HANES")

expensive_brands = c("GIVENCHY", "BAPE", "SUPREME", "OFF-WHITE", "COMME DES GARCONS")

brand_lists = c("ANTI SOCIAL SOCIAL CLUB", "ADIDAS", "SUPREME", "GILDAN", "FRUIT OF THE LOOM", 
                "GIVENCHY", "BURBERRY", "BAPE", "HANES", "OFF-WHITE")

brands_density(brand_lists, hypebeast)

brands_hist(brand_lists, hypebeast)

brands_boxplot(brand_lists, hypebeast)  

brand_density("ANTI SOCIAL SOCIAL CLUB", hypebeast)
brand_hist("ANTI SOCIAL SOCIAL CLUB", hypebeast)

brand_density("ADIDAS", hypebeast)

brand_density("GILDAN", hypebeast)

brand_hist("GILDAN", hypebeast)

brands_means_intervals(expensive_brands, hypebeast_summary)

#shows brands essentially have same average price
brands_anova("GIVENCHY", "OFF-WHITE", hypebeast)
#F VALUE 0.186 KEEP NULL HYPOTHESIS

#shows brands have essentially same average price
brands_anova("FRUIT OF THE LOOM", "HANES", hypebeast)
#F-VALUE 0.645 KEEP NULL

#shows that GILDAN is the lowest priced clothing, so we'll make that our "baseline"

brands_anova("GILDAN", "FRUIT OF THE LOOM", hypebeast)
#F VALUE 3.07e-15


brands_anova("GILDAN", "HANES", hypebeast)
#F VALUE 5.9e-16

brands_anova("GILDAN", "NFL", hypebeast)
#F VALUE 0.381

#make list of cost "multipliers"
gildan_price = hypebeast_summary %>%
  filter(Main_brand == "GILDAN") %>%
  select(MEAN)

gildan_price = gildan_price[[1]]

test_beast = hypebeast_summary %>%
  mutate(MULTIPLIER = MEAN / gildan_price)

multiplier_chart = test_beast %>%
  ggplot(aes(x = MULTIPLIER, y = MEDIAN)) +
  geom_point(aes(color = Main_brand, size = MULTIPLIER)) +
  geom_label_repel(aes(label = Main_brand),
                   box.padding   = 0.35, 
                   point.padding = 0.5,
                   segment.color = 'grey50') +
  theme(legend.position ="None") + ggtitle("Sanity Check: Median vs Multipliers") +
  xlab("Brand price 'Multiplier'") + ylab("Median Listing")

multiplier_chart
