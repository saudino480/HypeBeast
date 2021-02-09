# HypeBeast
Webscrapper for Grailed T-shirts

Contained in this repo is the project: "Who's Afraid of the Hypebeast?" which was completed around Summer 2019.

The idea of the project was to ingest information from a website, in this case Grailed.com, in order to understand how the label of the clothes affects how much those clothes cost. For instance, How much more is a t-shirt made by Gucci as opposed to one made by Gilden? And could that information be used in order to give consumers in the aftermarket make informed decisions about their second hand street wear? I come to a couple of conclusions in my article, [here](www.google.com). Unfortunately, the scraper no longer works, as the Grailed website was redesigned shortly after I successfully scrapped my data, and this project stands as a record.

The main file of the project is the grailed_scrapper.py, which contains the majority of the scrapper's code--handling exceptions, etc. It is tightly tied to the helper.py file, which allows me to hide away some of the more complicated try/except blocks that scraping Grailed.

Data analysis is done in R, and the files for that are found in the /data_analysis folder. I chose R because I was more comfortable at the time with it. Maybe it would be a good challenge one day to return and redo the analysis in python.

The data from the project (now heavily antiquidated, circa 2019) is contained in the data folder, for free use.

Please feel free to reach out to me with any questions at saudino480@gmail.com

Thanks!
