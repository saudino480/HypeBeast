library(tidyverse)
library(dplyr)

brand_hist = function(brand, df) {
   df %>%
    filter(df$Main_brand == brand) %>%
    ggplot(aes(x = Price)) +
    geom_histogram(binwidth = 5)
}

brands_hist = function(brands, df) {
  df %>%
    filter(df$Main_brand %in% brands) %>%
    ggplot(aes(x = Price)) +
    geom_histogram(binwidth = 5, aes(fill = Main_brand), position = position_stack(reverse = TRUE)) +
    labs(fill = "Brands") + ylab("Number of Listings") +
    ggtitle("Distribution of Listing Prices")
}

brand_density = function(brand, df) {
  df %>%
    filter(df$Main_brand == brand) %>%
    ggplot(aes(x = Price)) +
    geom_density()
}

brands_density = function(brands, df) {
  df %>%
    filter(df$Main_brand %in% brands) %>%
    ggplot(aes(x = Price)) +
    geom_density(aes(color = Main_brand)) + xlab("Price (in US $)") +
    ylab("Density") + labs(color = "Brands") + ggtitle("Distribution of Listing Prices as Density")
}

brands_boxplot = function(brands, df) {
  df %>%
    filter(df$Main_brand %in% brands) %>%
    ggplot(aes(x = Main_brand, y = Price)) +
    geom_boxplot() + xlab("Brand") + ylab("Price (in US $)") + theme(axis.text.x = element_text(angle = 60, hjust = 1)) +
    labs(fill = "Brands") + ggtitle("Distribution of Listing Prices as Boxplot")
}

brands_means_intervals = function(brands, df) {
  df %>%
    filter(df$Main_brand %in% brands) %>%
    ggplot(aes(x = Main_brand, y = MEAN)) +
    geom_point(size = 4) +
    geom_errorbar(aes(ymax = low_mean, ymin = high_mean)) +
    xlab("Brand") + ylab("Mean Price of Listings (in US $)") +
    theme(axis.text.x = element_text(angle = 60, hjust = 1)) +
    ggtitle("Means and 95% Confedence Intervals")
}

brands_anova = function(brand1, brand2, dataframe) {
  test = dataframe %>%
    filter(dataframe$Main_brand %in% c(brand1, brand2)) %>%
    select(Main_brand, Price)
  
  
  ANOVA_RESULTS = aov(test$Price ~ test$Main_brand, df = test)
  
  summary(ANOVA_RESULTS)
}


