# _material_analysis
Project Summary:
Objective.
The company encounters issues with materials purchasing overseas for our linear lighting system. The assembling parts need to be shipped from east Europe, which is estimated with three months lead time arriving in Australia. Management and engineering team are struggling to calculate the purchasing amount. This report will show management the insights regarding product model selection, mian-component selection, annual sales reports

Technical Detail.
1. data acquirzation and cleaning
This project required me to obtain raw data from mutiple excel file (nearly 300 excel files) and then clean and convert those data in the certain format which I can use to do the analytics tasks. I created a data pipeline to recursively read data using Python and successfully store those data into a dataframe. There are some cleaning tasks in this project such as datatime format conversion, NA data removing, text data scraping etc.

2. data visualzation
The cleaned data will be used to create visual dashboards in aid with management team making purchasing decision. I attempted to use python dash and ploty library to create one-page interactive dashboard for user to review.

3. deployment
The dashboard is created and deployment to cloud using Heroku cloud service. Thus, the dashboard can be viewed by users remotely without restriction of time and location. 
