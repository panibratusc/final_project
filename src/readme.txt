#News Scraping Script

## Description 
This Python script scrapes recent news headlines and descriptions from three major news outlets:The National Broadcasting Company (NBC), The New York Times (NYT), Cable News Network (CNN)

#Instructions 
To run the script, follow these commands in your terminal: 
1. Make sure you have packages pre-installed. If not use the following commands in your terminal to install them: pip install 
2. **Runnning the Script** Execute the script using the following command: python get_data_2.py --source SOURCE --scrape NUM_RECORDS --save OUTPUT_FILE

#Example: 
python get_data_2.py --source NBC --scrape 7 --save output.csv

The command above will scrape 7 sources from the NBC "world" section online page  

#Additional information 
The script uses the 'requests' library to get the HTML data from the websites and `BeautifulSoup` for parsing the HTML.