# Apartment lottery data visualization
## Description:
The project is part of the final university visualization course project.  
* I used a Scraper to collect the data from the list of government lotteries on the apartment. 
  The link to the lottery website is https://www.dira.moch.gov.il/ProjectsList.
* I used Python visualization libraries like Matplotlib, seaborn, and Plotly to learn about the data.
* Creating a web interactive plot using Streamlit so I could share my work with my academic colleagues
 
## Usage Instructions:
Use the following link to show the visualizations:
https://apartmentlottery-42u2m8mkvmgcon45voahnb.streamlit.app/

To get updated data, pull the Python file apartement_lottery_scrapign.ipynb and run the Scraper.

## Data Description:
The dataset contains information about government lotteries for apartments, with each row representing a single lottery entry. Below is a description of the columns in the dataset:

1. Lottery Number: The unique identifier for each lottery.
2. Last Date Registration: The deadline for registration for the lottery.
3. Location: The location where the apartment is situated.
4. Contractor: The name of the contractor responsible for the construction.
5. Number of Apartments: The total number of apartments available in the lottery.
6. Apartments for Natives: The number of apartments reserved for native residents.
7. Registered: Total number of registrations for the lottery.
8. Registered Natives: Number of registrations from native residents.
9. Price per Meter: Price per square meter of the apartments.
10. Grant: Shows who matches the grant in INS.
11. Natives' Chance to win: Probability of a native resident winning the lottery.
12. Non-Native's Chance to win: Probability of a non-native resident winning the lottery.
13. Region: The region where the apartment is located.
14. Country: The country where the apartment is located.
15. Construction Permit Name: Current status of the construction permit.
16. Project Status: Current status of the project.
17. LotteryId: Unique identifier for the lottery.
