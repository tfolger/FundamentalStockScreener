'''
Fundamental Stock Screener
'''

############
# PREAMBLE
############

'''
 IMPORTANT
 **********
 Please make sure to download all necessary packages. Additionally, you must 
 download the chrome driver from the following website 
 http://chromedriver.chromium.org/downloads
 and save it in your working directory. Otherwise the program will not work.
'''

# Load libraries
import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
import datetime as dt # package for dates
import time
import matplotlib.pyplot as plt # for graphs


# packages for scraping:
import bs4 as bs # scraping
import requests # get request
from selenium import webdriver # scraping
from selenium.common.exceptions import NoSuchElementException # error handling of scraping

# set executable_path
executable_path=r"C:\Users\Andi\Desktop\test2\chromedriver.exe"
#executable_path=r"C:\Users\Till\Desktop\test\chromedriver_win32\chromedriver.exe"

#define a function to print whole data set
def print_full(x) -> None:
    pd.options.display.max_columns = x.shape[1] # display all columns
    pd.options.display.max_rows = x.shape[0] # display all rows
    print(x)


#################################
## STEP 1: PROVIDE STOCK INDICES
#################################
    
'''
We provide two current stock indices with tickers and a short test list where you can choose from.
Additionally, we provide a ticker list with company names from which the user can choose in STEP 3.
'''

# Current S&P Companies
SP500 = ['A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADS', 'ADSK', 'AEE', 'AEP', 'AES', 'AFL', 'AGN', 'AIG', 'AIV', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'ALXN', 'AMAT', 'AMD', 'AME', 'AMG', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'ANSS', 'ANTM', 'AON', 'AOS', 'APA', 'APC', 'APD', 'APH', 'APTV', 'ARE', 'ARNC', 'ATVI', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO', 'BA', 'BAC', 'BAX', 'BBT', 'BBY', 'BDX', 'BEN', 'BF.B', 'BHF', 'BHGE', 'BIIB', 'BK', 'BKNG', 'BLK', 'BLL', 'BMY', 'BR', 'BRK.B', 'BSX', 'BWA', 'BXP', 'C', 'CAG', 'CAH', 'CAT', 'CB', 'CBOE', 'CBRE', 'CBS', 'CCI', 'CCL', 'CDNS', 'CE', 'CELG', 'CERN', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI', 'CINF', 'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COG', 'COO', 'COP', 'COST', 'COTY', 'CPB', 'CPRI', 'CPRT', 'CRM', 'CSCO', 'CSX', 'CTAS', 'CTL', 'CTSH', 'CTXS', 'CVS', 'CVX', 'CXO', 'D', 'DAL', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DISCA', 'DISCK', 'DISH', 'DLR', 'DLTR', 'DOV', 'DRE', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN', 'DWDP', 'DXC', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR', 'EOG', 'EQIX', 'EQR', 'ES', 'ESS', 'ETFC', 'ETN', 'ETR', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FANG', 'FAST', 'FB', 'FBHS', 'FCX', 'FDX', 'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FL', 'FLIR', 'FLR', 'FLS', 'FLT', 'FMC', 'FOX', 'FOXA', 'FRC', 'FRT', 'FTI', 'FTNT', 'FTV', 'GD', 'GE', 'GILD', 'GIS', 'GLW', 'GM', 'GOOG', 'GOOGL', 'GPC', 'GPN', 'GPS', 'GRMN', 'GS', 'GT', 'GWW', 'HAL', 'HAS', 'HBAN', 'HBI', 'HCA', 'HCP', 'HD', 'HES', 'HFC', 'HIG', 'HII', 'HLT', 'HOG', 'HOLX', 'HON', 'HP', 'HPE', 'HPQ', 'HRB', 'HRL', 'HRS', 'HSIC', 'HST', 'HSY', 'HUM', 'IBM', 'ICE', 'IDXX', 'IFF', 'ILMN', 'INCY', 'INFO', 'INTC', 'INTU', 'IP', 'IPG', 'IPGP', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW', 'IVZ', 'JBHT', 'JCI', 'JEC', 'JEF', 'JKHY', 'JNJ', 'JNPR', 'JWN', 'K', 'KEY', 'KEYS', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KR', 'KSS', 'KSU', 'L', 'LB', 'LEG', 'LEN', 'LH', 'LIN', 'LKQ', 'LLL', 'LLY', 'LMT', 'LNC', 'LNT', 'LOW', 'LRCX', 'LUV', 'LW', 'LYB', 'M', 'MA', 'MAA', 'MAC', 'MAR', 'MAS', 'MAT', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'MGM', 'MHK', 'MKC', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOS', 'MPC', 'MRK', 'MRO', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTD', 'MU', 'MXIM', 'MYL', 'NBL', 'NCLH', 'NDAQ', 'NEE', 'NEM', 'NFLX', 'NFX', 'NI', 'NKE', 'NKTR', 'NLSN', 'NOC', 'NOV', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NWL', 'NWS', 'NWSA', 'O', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OXY', 'PAYX', 'PBCT', 'PCAR', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'PPG', 'PPL', 'PRGO', 'PRU', 'PSA', 'PSX', 'PVH', 'PWR', 'PXD', 'PYPL', 'QCOM', 'QRVO', 'RCL', 'RE', 'REG', 'REGN', 'RF', 'RHI', 'RHT', 'RJF', 'RL', 'RMD', 'ROK', 'ROL', 'ROP', 'ROST', 'RSG', 'RTN', 'SBAC', 'SBUX', 'SCHW', 'SEE', 'SHW', 'SIVB', 'SJM', 'SLB', 'SLG', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRE', 'STI', 'STT', 'STX', 'STZ', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYMC', 'SYY', 'T', 'TAP', 'TDG', 'TEL', 'TFX', 'TGT', 'TIF', 'TJX', 'TMK', 'TMO', 'TPR', 'TRIP', 'TROW', 'TRV', 'TSCO', 'TSN', 'TSS', 'TTWO', 'TWTR', 'TXN', 'TXT', 'UA', 'UAA', 'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNM', 'UNP', 'UPS', 'URI', 'USB', 'UTX', 'V', 'VAR', 'VFC', 'VIAB', 'VLO', 'VMC', 'VNO', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VZ', 'WAT', 'WBA', 'WCG', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR', 'WLTW', 'WM', 'WMB', 'WMT', 'WRK', 'WU', 'WY', 'WYNN', 'XEC', 'XEL', 'XLNX', 'XOM', 'XRAY', 'XRX', 'XYL', 'YUM', 'ZBH', 'ZION', 'ZTS', 'A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADS', 'ADSK', 'AEE', 'AEP', 'AES', 'AFL', 'AGN', 'AIG', 'AIV', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'ALXN', 'AMAT', 'AMD', 'AME', 'AMG', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'ANSS', 'ANTM', 'AON', 'AOS', 'APA', 'APC', 'APD', 'APH', 'APTV', 'ARE', 'ARNC', 'ATVI', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO', 'BA', 'BAC', 'BAX', 'BBT', 'BBY', 'BDX', 'BEN', 'BF.B', 'BHF', 'BHGE', 'BIIB', 'BK', 'BKNG', 'BLK', 'BLL', 'BMY', 'BR', 'BRK.B', 'BSX', 'BWA', 'BXP', 'C', 'CAG', 'CAH', 'CAT', 'CB', 'CBOE', 'CBRE', 'CBS', 'CCI', 'CCL', 'CDNS', 'CE', 'CELG', 'CERN', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI', 'CINF', 'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COG', 'COO', 'COP', 'COST', 'COTY', 'CPB', 'CPRI', 'CPRT', 'CRM', 'CSCO', 'CSX', 'CTAS', 'CTL', 'CTSH', 'CTXS', 'CVS', 'CVX', 'CXO', 'D', 'DAL', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISCA', 'DISCK', 'DISH', 'DLR', 'DLTR', 'DOV', 'DRE', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN', 'DWDP', 'DXC', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR', 'EOG', 'EQIX', 'EQR', 'ES', 'ESS', 'ETFC', 'ETN', 'ETR', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FANG', 'FAST', 'FB', 'FBHS', 'FCX', 'FDX', 'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FL', 'FLIR', 'FLR', 'FLS', 'FLT', 'FMC', 'FOX', 'FOXA', 'FRC', 'FRT', 'FTI', 'FTNT', 'FTV', 'GD', 'GE', 'GILD', 'GIS', 'GLW', 'GM', 'GOOG', 'GOOGL', 'GPC', 'GPN', 'GPS', 'GRMN', 'GS', 'GT', 'GWW', 'HAL', 'HAS', 'HBAN', 'HBI', 'HCA', 'HCP', 'HD', 'HES', 'HFC', 'HIG', 'HII', 'HLT', 'HOG', 'HOLX', 'HON', 'HP', 'HPE', 'HPQ', 'HRB', 'HRL', 'HRS', 'HSIC', 'HST', 'HSY', 'HUM', 'IBM', 'ICE', 'IDXX', 'IFF', 'ILMN', 'INCY', 'INFO', 'INTC', 'INTU', 'IP', 'IPG', 'IPGP', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW', 'IVZ', 'JBHT', 'JCI', 'JEC', 'JEF', 'JKHY', 'JNJ', 'JNPR', 'JPM', 'JWN', 'K', 'KEY', 'KEYS', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KR', 'KSS', 'KSU', 'L', 'LB', 'LEG', 'LEN', 'LH', 'LIN', 'LKQ', 'LLL', 'LLY', 'LMT', 'LNC', 'LNT', 'LOW', 'LRCX', 'LUV', 'LW', 'LYB', 'M', 'MA', 'MAA', 'MAC', 'MAR', 'MAS', 'MAT', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'MGM', 'MHK', 'MKC', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOS', 'MPC', 'MRK', 'MRO', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTD', 'MU', 'MXIM', 'MYL', 'NBL', 'NCLH', 'NDAQ', 'NEE', 'NEM', 'NFLX', 'NFX', 'NI', 'NKE', 'NKTR', 'NLSN', 'NOC', 'NOV', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NWL', 'NWS', 'NWSA', 'O', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OXY', 'PAYX', 'PBCT', 'PCAR', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'PPG', 'PPL', 'PRGO', 'PRU', 'PSA', 'PSX', 'PVH', 'PWR', 'PXD', 'PYPL', 'QCOM', 'QRVO', 'RCL', 'RE', 'REG', 'REGN', 'RF', 'RHI', 'RHT', 'RJF', 'RL', 'RMD', 'ROK', 'ROL', 'ROP', 'ROST', 'RSG', 'RTN', 'SBAC', 'SBUX', 'SCHW', 'SEE', 'SHW', 'SIVB', 'SJM', 'SLB', 'SLG', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRE', 'STI', 'STT', 'STX', 'STZ', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYMC', 'SYY', 'T', 'TAP', 'TDG', 'TEL', 'TFX', 'TGT', 'TIF', 'TJX', 'TMK', 'TMO', 'TPR', 'TRIP', 'TROW', 'TRV', 'TSCO', 'TSN', 'TSS', 'TTWO', 'TWTR', 'TXN', 'TXT', 'UA', 'UAA', 'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNM', 'UNP', 'UPS', 'URI', 'USB', 'UTX', 'V', 'VAR', 'VFC', 'VIAB', 'VLO', 'VMC', 'VNO', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VZ', 'WAT', 'WBA', 'WCG', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR', 'WLTW', 'WM', 'WMB', 'WMT', 'WRK', 'WU', 'WY', 'WYNN', 'XEC', 'XEL', 'XLNX', 'XOM', 'XRAY', 'XRX', 'XYL', 'YUM', 'ZBH', 'ZION', 'ZTS']

# Current Dow Jones Industrial Companies
DJI = ['MMM', 'AXP', 'AAPL', 'CAT', 'CVX',	'CSCO', 'DWDP',	'XOM', 'INTC', 'IBM', 'JNJ', 'MRK', 'MSFT', 'NKE', 'PFE','KO',	'GS',	'PG', 'TRV', 'DIS', 'UTX', 'UNH', 'VZ', 'V', 'WBA', 'WMT']

# test list
test = ['GT', 'IVZ', 'LNC', 'MET', 'MOS', 'MPC', 'MRO', 'PRU', 'TAP', 'UNM', 'WRK']

# load ticker data
Ticker_List = pd.read_excel('Ticker_List.xlsx')


##############################
# STEP 2: STOCK SCREENER
##############################

##############################
# STEP 2.1 ASK USER FOR INPUT
##############################

# print welcome message
print("\nWelcome to the Fundamental Stock Screener!\nThis tool helps you to efficiently filter through stocks for your fundamental stock analysis and stock picking!")

# Ask user for index
print("\nYou can choose between two stock indices: Dow Jones Industrial (DJI) and S&P500. Which one do you want to choose?")    

# Check for user input
while True:
    try:
        # first get index from user:
        index = input(("Please enter either DJI or SP500 here: "))
        # check for input
        if index.lower() == "dji": #check if input is equal to index dji
            # use DJI later
            usedindex = DJI
            break # everything ends
        elif index.lower() == "sp500": #check if input is equal to index sp500
            # use SP500 later
            usedindex = SP500
            break # everthing ends
        elif index.lower() == "test": #check if input is equal to index test
            # use test later
            usedindex = test
            break
        #otherwise, give user again chance for input
        else:
            print("\nError. You must insert exactly one of the indices - DJI or SP500 or test - given. Please try again.") # print error message if input is not a number
            continue # ask user again to give an input
    
    
    # brauchen wir das überhaupt? (ist bei den anderen loops gleich...)
    # any other error:
    except: 
        print("\nError. You must insert exactly one of the indices - DJI or SP500 or test - given. Please try again.") # print error message if input is not a number
        continue # ask user again to give an input

print("\nThe stock index " + index + " will be analysed now. You now have to set the minimum requirements a stock must meet.")    


# lists to save data:
statistics_names = [] 
statistics_values = []   
    
# ask user for maximum pbr
print("\nWhat is the maximum Price to Book Ratio a stock may have? Note that investors usually set a number around 2 here. ")
while True:
    try:
        # let user insert a number
        max_pbr = float(input(("Please insert the maximum number of the Price to Book Ratio here: ")))
        # Append ratio name and value to lists:
        statistics_values.append(max_pbr)
        statistics_names.append(' Maximum Price to Book Ratio')
        break
    except ValueError:
        print("\nError. You have to enter a number. Make sure to use a dot to separate decimals. Please try again.") # print error message if input is not a number
        continue # ask user again to give an input which size will be checked again


# ask user for maximum p/e
print("\nWhat is the maximum Price to Earnings Ratio a stock may have? Note that investors usually set here a number around 20.")
while True:
    try:
        # let user insert a number for ratio
        max_pe = float(input(("Please insert the maximum number of the Price to Earnings Ratio here: ")))
        # Append ratio name and value to lists
        statistics_values.append(max_pe)
        statistics_names.append('Maximum Price to Earnings Ratio')
        break
    except ValueError:
        print("\nError. You have to enter a number. Please try again.") # print error message if input is not a number
        continue # ask user again to give an input which will be checked again


# ask user for maximum d/e
print("\nWhat is the maximum Debt to Equity Ratio a stock may have? Set it around 100 to get a result.")
while True:
    try:
        # let user insert a number for ratio
        max_de = float(input(("Please insert the maximum number of the Debt to Equity Ratio here: ")))
        # Append ratio name and value to lists
        statistics_values.append(max_de)
        statistics_names.append('Maximum Debt to Equity Ratio')
        break
    except ValueError:
        print("\nError. You have to enter a number. Please try again.") # print error message if input is not a number
        continue # ask user again to give an input which size will be checked again

# print message what follows
print("\nGreat! You will now get the stocks that meet the given requirements: \n")

     
Statistics_Frame = pd.DataFrame({
              'Ratio Name': statistics_names, 
              'Ratio Value': statistics_values})  

print(Statistics_Frame)

print("\nThis process may take a few minutes. Please be patient.")


####################################################
## STEP 2.2: SCRAPE DATA AND CHECK FOR REQUIREMENTS
####################################################

# Ouput: List of stocks that meet requirements

# create empty lists to save results in function
meetrequirements = []
meetrequirements_stock_name = []
PBR_list = []
PE_list = []
DE_list = []
PEG_list = []
error_list = []

#Webscrapper using Yahoo HTML Code / Here we use BeautifulSoup as it is faster than Selenium and works accurately for this data
def yahooKeystats(stock):
    try: 
        # url to be visited for each stock
        url = "https://finance.yahoo.com/quote/" + stock + "/key-statistics"
        # send get request for url and parse text
        r=requests.get(url)
        soup = bs.BeautifulSoup(r.text,"html.parser")        
        pbr = soup.find_all('td',{'class':'Fz(s) Fw(500) Ta(end)'})[6].text
        stock_name = soup.find_all('h1',{'class':'D(ib) Fz(16px) Lh(18px)'})[0].text
        
        # Check whether stocks meet some investment requirements set by user
        
        # 1.) Price to Book Ratio must be smaller than 1
        if float(pbr) < float(max_pbr):           
            #Used PE not PEG as Yahoo doesn't have this for a lot of stocks = producing errors
            # then scrape p/e:
            PE = soup.find_all('td',{'class':'Fz(s) Fw(500) Ta(end)'})[2].text
            
            # 2.) PE ratio must be smaller than some value
            if float(PE) < float(max_pe):
                # then scrape debt to equity ratio:
                DE = soup.find_all('td',{'class':'Fz(s) Fw(500) Ta(end)'})[26].text
                
                # 3.) DE ratio must be smaller than some value
                if float(DE) < float(max_de):
                    PEG5 = soup.find_all('td',{'class':'Fz(s) Fw(500) Ta(end)'})[4].text
                    
                    # Output given to the user:
                    print(stock_name + ' meets the requirements:')
                    print('----------------------------------------')
                    print('Price to Book Ratio: ', pbr)
                    print('Price to Earnings Ratio: ', PE)
                    print('Total Debt to Equity: ', DE)
                    print('PEG Ratio: ', PEG5)
                    print('----------------------------------------')
                    
                    # Append ratios and the ticker of a stock to lists created above
                    meetrequirements.append(stock)
                    meetrequirements_stock_name.append(stock_name)
                    PBR_list.append(pbr)
                    PE_list.append(PE)
                    DE_list.append(DE)
                    PEG_list.append(PEG5)
                    
    # Error handling
    except Exception as e:
      error_list.append(e) #write a list with all error messages
          
# Loop for each stock in the index list        
for eachStock in usedindex:
    yahooKeystats(eachStock)
    time.sleep(.1)


# print list of stocks that meet the requirements set
print("The tickers for the filtered stocks are: ")
print(meetrequirements)


# Create dataframe with all companies that meet requirements with all ratios
MeetRequirements_Frame = pd.DataFrame({
              'Company': meetrequirements_stock_name,
              'Price to Book': PBR_list,
              'Price to Earnings': PE_list,
              'Total Debt to Equity': DE_list,
              'PEG Ratio': PEG_list,}) 
    
    
# Ask user whether to print an excel file of the stocks that meet the requirements
while True:
    try:
        requirements_excel = input(("Do you want to have an Excel file of all stocks that meet the requirements including ratios? Insert Yes or No: "))
        if requirements_excel.lower() == "no":
            break # nothing happens
            
        elif requirements_excel.lower() == "yes":
            # write excel file
            with pd.ExcelWriter('MeetRequirements.xlsx') as writer:
                MeetRequirements_Frame.to_excel(writer, sheet_name='Stocks with Ratios')
                Statistics_Frame.to_excel(writer, sheet_name='Given Requirements')
            # give user information
            print("\nWe have now saved the file named 'MeetRequirements.xlsx' in your current working directory.")                      
            break # everthing ends
        
        else:
            print("\nError. Please insert 'Yes' or 'No'. Please try again.") # print error message 
            continue  # ask user again to give an input again after error message
    
    # error handling for any other error
    except:
        print("\nError. Please insert 'Yes' or 'No'. Please try again.") # print error message 
        continue  # ask user again to give an input again after error message



#############################
# STEP 3: PEER GROUP ANALYSIS
#############################

'''
Here you get the chance to conduct a peer group analysis with some stock. The peers
can be either manually inserted or you get a recommendation of peers.
'''

# Ask user whether to conduct a peer group analysis with the stock the user inserted:
print("\nDo you want to continue with a peer-group analysis for a chosen stock? ")

# Check for user input and conduct the analysis if requested
while True:
    try:
        group_an = input(("Please type Yes or No: "))
        if group_an.lower() == "no":
            # Give user information:
            print("\nNo peer group analysis provided.")
            break #no fundamental stock analysis ends
        
        elif group_an.lower() == "yes":
            
            ###########################
            # START PEER GROUP ANALYSIS
            ###########################
            
            # Ask user which ticker to further analyse
            while True:
                try:
                    # Ask for user input
                    target_stock = input(("Please pick a stock out of the filtered stocks from above or from the SP500 / DJI and insert its ticker: "))
                    # check if ticker is in SP500
                    if target_stock.upper() in SP500:
                        # continue with analysis
                        break
                    # check if ticker is in DJI
                    elif target_stock.upper() in DJI:
                        break
                    # Let user type in another ticker which is in index
                    else:
                        print("Error. Please insert a ticker from the given indices.") # print error message 
                        continue  # ask user again to give an input again after error message
                # error handling
                except:
                    print("\nError. Please insert a ticker from the given indices.") # print error message 
                    continue  
            
            # Ask user how to compare stock:
            print("\nDo you want to insert stocks for comparison manually or continue with recommended stocks?")
            while True:
                try:
                    option_no = input(("Please type 1 for manual insertion or 2 for recommendations: "))
                    
                    #######################################
                    # OPTION 1: MANUAL PEER GROUP ANALYSIS
                    ######################################
                    if option_no == "1":
                        while True:
                            try:
                                # Ask the user for input
                                #print("\nA list of all possible stocks and its tickers can be found here:")
                                #print_full(Ticker_List)
                                
                                peers = input(("\nIf you insert 'help' a full list with tickers will show up where you can choose from. Otherwise, directly insert the tickers here separated by commas: "))                                     
                                # copy input to new variable to check if user wants help                               
                                
                                # Transform user input
                                # split input by comma to get a list
                                peers = peers.split(',')  
                                # transform each ticker to upper letters:
                                peers = [i.upper() for i in peers]
                                # delete spaces in each entry of the list
                                peers = [i.strip(' ') for i in peers]
                                # delete duplicates from peers list
                                peers = list(dict.fromkeys(peers))
                                    
                                # merge indices
                                mergedindices = SP500 + DJI
                                # delete duplicates from mergedindices list
                                mergedindices = list(dict.fromkeys(mergedindices))                                                             
                                
                                # user needs help
                                if peers == ['HELP']:
                                    # print full Ticker_List (data loaded in preamble)
                                    print_full(Ticker_List)
                                    continue
                                
                                # user inserted something else than help
                                else:
                                    # test if all tickers exist in list check = true, otherwise, check = false
                                    check = False
                                    check = any(elem in peers for elem in mergedindices)
                                    
                                    # if all tickers exist in list (check = true)
                                    if check is True:
                                        # Stocks we will analyse now:
                                        print("\nWe now continue with the peer group analysis with the following tickers:")
                                        print(peers)
                                        break # if check is true ends
                                    
                                    # if tickers do not exist in our list (check = false), give user chance to inser new tickers:
                                    else:
                                        print("\nError. The tickers do not exist in our list. Please try again.")
                                        continue # with user input of peer stocks (option 1)
                                
                            # error handling     
                            except: 
                                print("\nError. The tickers do not exist in our list. Please try again. ") # error message
                                continue  # with user input of peer stocks (option 1)    
                        
                        break # everything ends of option number 1
                    
                    ################################
                    # OPTION 2: PEER RECOMMENDATION
                    ################################
                    elif option_no == "2":
                        print("\nPlease wait a moment while we identify your peer stocks. \nThis may take a few seconds.")
                               
                        # SCRAPER SETTINGS
                        # set options for driver
                        options = webdriver.ChromeOptions()
                        options.add_argument('--ignore-certificate-errors')
                        options.add_argument("--test-type")
                        options.binary_location = "/usr/bin/chromium"
                        
                        # start driver
                        driver = webdriver.Chrome(executable_path=executable_path)                     
                                                                    
                        # url to be visited
                        url = ('https://www.nasdaq.com/symbol/' + target_stock + '/stock-comparison')
                        
                        # get request
                        driver.get(url)
                        
                        # Wait for 5 seconds
                        time.sleep(5) 
                        
                        # handle cookies 
                        cookies_list = driver.get_cookies()
                        cookies_dict = []
                        for cookie in cookies_list:
                            cookies_dict.append([cookie['name'],cookie['value']])
                                               
                        # create empty lists where we add peer tickers
                        peers = []
                        peer_names = []
                                                                       
                        #loop to scrape tickers
                        for i in range(1, 5):
                            # scrape element
                            try:
                                # scrape peer ticker
                                peer_ticker = driver.find_element_by_xpath('//*[@id="quotes_content_left_SC_Symbol'+str(i)+'"]')
                                # get the attribute
                                peer_ticker = peer_ticker.get_attribute('value')
                                # add ticker to peers list
                                peers.append(peer_ticker)
                                
                                # scrape peer name
                                peer_name = driver.find_element_by_xpath('//*[@id="quotes_content_left_SC_CompanyPanel"]/table/tbody/tr[1]/td['+str(i+1)+']/div[2]/a')
                                # add name to peer_names list
                                peer_names.append(peer_name.text)
                            
                            # error handling if there does not exist such an element
                            except NoSuchElementException:
                                print("Peer number" + str(i) + "out of 5 not found!")
                                pass
                                    
                        # quit / close river
                        driver.quit()
                        
                        # create dataframe with stocks and tickers
                        Peer_Recommendation_Frame = pd.DataFrame({
                                      'Peer Name': peer_names}, 
                                      index = peers) 
                        # set ticker as index
                        Peer_Recommendation_Frame.index.name = 'Ticker'
                        
                        # print list of peer tickers
                        print("\nWe identified the following peer stocks for you:")                      
                        print(Peer_Recommendation_Frame)
                        
                         
                        # Message if no peers found:
                        if (len(peers) == 0):
                            print("Sorry, no peers found! Enter your own peers if you want to.")

                        break # option number 2 ends
                    
                    # if input is neither 1 or 2, give user chance for new input:
                    else:
                        print("\nError. Please insert a number: 1 for manual insertion or 2 for recommendations. Please try again.") # print error message if input is not a number
                        continue  # ask user again to give an input whose size will be checked again
                
                # ERROR HANDLING
                except: 
                    print("\nError. Please insert a number: 1 for manual insertion or 2 for recommendations. Please try again.") # print error message if input is not a number
                    continue  # ask user again to give an input
              
                
#################################
# STEP 4: PEER GROUP VALUATIONS
#################################

#Here you will be provided with financials of the peers from STEP 3 and the company you wanted to analyse. The output will be tables of bechmark valuations.
        
            
###########################
# STEP 4.1: PEER BENCHMARK
###########################
            
            print("\nBelow you can find some information about the benchmark stocks: \n")            

            # create empty lists to be filled by loop later
            Forward_PE_list = []
            EV_Revenue_list = []
            EV_EBITDA_list = []
            
            # Loop to scrape key statistics for chosen stocks
            for targetstock in peers:
                # url to be visited for each stock
                url = "https://finance.yahoo.com/quote/" + targetstock + "/key-statistics"
                # send get request for url
                r=requests.get(url)
                # parse text
                soup = bs.BeautifulSoup(r.text,"html.parser")  
            
                # SCRAPE KEY STATISTICS
                # Forward / PE
                Forward_PE = soup.find_all('td',{'class':'Fz(s) Fw(500) Ta(end)'})[3].text
                # append element to list
                Forward_PE_list.append(Forward_PE)
                    
                # EV / Revenue
                EV_Revenue = soup.find_all('td',{'class':'Fz(s) Fw(500) Ta(end)'})[7].text
                # append element to list
                EV_Revenue_list.append(EV_Revenue)
                    
                # EV / EBITDA
                EV_EBITDA = soup.find_all('td',{'class':'Fz(s) Fw(500) Ta(end)'})[8].text
                # append element to list
                EV_EBITDA_list.append(EV_EBITDA)
            
            # Create dataframe out of lists
            benchmarks = pd.DataFrame({
                          'Forward PE': Forward_PE_list, 
                          'EV / Revenue': EV_Revenue_list, 
                          'EV / EBITDA': EV_EBITDA_list},
                          index = peers)        
            
            # give index name
            benchmarks.index.name = 'Company Ticker'
            
            # Change 'N/A' to nan by pandas
            benchmarks = benchmarks.replace('N/A', np.nan)
            
            # create list of all statistics
            statistics = ['Forward PE', 'EV / Revenue', 'EV / EBITDA']
            
            # loop over each statistics:
            for stat in statistics:
                # change datatype for each statistics
                benchmarks[stat] = pd.to_numeric(benchmarks[stat])
                        
            # Compute mean and median and add it to the end of the dataframe
            benchmarks.loc['Average'] = benchmarks[:(len(benchmarks))].mean()
            benchmarks.loc['Median'] = benchmarks[:(len(benchmarks)-1)].median()
            
            # Show user benchmark analysis
            print_full(benchmarks)
            
            
            
#######################################
# STEP 4.2: TARGET COMPANY FINANCIALS
#######################################
            
            # create a list of index
            Target_Stock = []
            Target_Stock.append(target_stock.upper())
            
            # Create dataframe out of lists
            r=requests.get("https://finance.yahoo.com/quote/" + target_stock + "/key-statistics?p=" + target_stock)
            # parse text
            soup = bs.BeautifulSoup(r.text,"xml")        
            # scrape PE Ratio
            Forward_PE_target = soup.find_all('td',{'class':'Fz(s) Fw(500) Ta(end)'})[3].text
            # scrape EV-Revenue
            EV_Revenue_target = soup.find_all('td',{'class':'Fz(s) Fw(500) Ta(end)'})[7].text
            # Scrape EV-EBITDA
            EV_EBITDA_target = soup.find_all('td',{'class':'Fz(s) Fw(500) Ta(end)'})[8].text
            
            # Create dataframe
            Target_Frame = pd.DataFrame({
                          'Forward PE': Forward_PE_target, 
                          'EV / Revenue': EV_Revenue_target, 
                          'EV / EBITDA': EV_EBITDA_target},
                          index = Target_Stock)     
            
            Target_Frame.index.name = 'Company Ticker' 
            
            Target_Frame = Target_Frame.replace('N/A', np.nan)
            
            #Empty row for better overview
            print("\n", Target_Frame)
            
            
################
# STEP 5: PLOTS
################
            
#
#Here you will be provided with some plots of stock returns.
#

###############################
# STEP 5.1: INDEXED STOCK PLOT
###############################
            
            start = dt.datetime(2015,1,1)
            end = dt.datetime.today()
            
            print("\nFor a good comparison of stock price development, we will show an indexed stock plot.\nDo you want to add an industry index for that? ")
            
            # Check for user input
            while True:
                try:
                    # Ask user for answer
                    industry_index = input(("Please type Yes or No: "))
                    
                    # if user doesn't want to add an industry index
                    if industry_index.lower() == "no":
                        print("The plot will be provided without an industry index.")
                        break # no index ends
                    
                    # if user wants to add an industry index
                    elif industry_index.lower() == "yes":
                        
                        # define industry indices            
                        tech_index = 'IYW'
                        industrial_index = 'IYJ'
                        pharma_index = 'IHE'
                        finance_index='IYF'
                        energy_index='IYE'
                        telcom_index='IYZ'
                                    
                        # let user select industry index:
                        while True:
                            try:
                                add_index = input(("Please select your industry index. \nType 1 for Tech, 2 for Industrials, 3 for Pharma, 4 for Financials, 5 for Energy, 6 for Telecommunications. "))            
                                if add_index == "1":
                                    peers.append(tech_index) 
                                    print('\nYour selected tech index is: iShares Dow Jones US Technology')
                                    print('\nThe Ticker of your selected Index is: ' + tech_index)
                                    break
                                elif add_index == "2":
                                    peers.append(industrial_index)
                                    print('\nYour selected industrial index is: iShares Dow Jones US Industrial')
                                    print('\nThe Ticker of your selected Index is: ' + industrial_index)
                                    break
                                elif add_index == "3":
                                    peers.append(pharma_index)
                                    print('\nYour selected pharma index is: iShares US Pharmaceuticals')
                                    print('\nThe Ticker of your selected Index is: ' + pharma_index)
                                    break
                                elif add_index == "4":
                                    peers.append(finance_index)  
                                    print('\nYour selected finance index is: iShares Dow Jones US Financial Sector')
                                    print('\nThe Ticker of your selected Index is: ' + finance_index)
                                    break
                                elif add_index == "5":
                                    peers.append(energy_index)
                                    print('\nYour selected energy index is: iShares Dow Jones US Financials')
                                    print('\nThe Ticker of your selected Index is: ' + energy_index)
                                    break
                                elif add_index == "6":
                                    peers.append(telcom_index)
                                    print('\nYour selected telecom index is: iShares Dow Jones US Telecom')
                                    print('\nThe Ticker of your selected Index is: ' + telcom_index)
                                    break
                                else:
                                    print("\nError. Please insert an integer between 1 and 6. Please try again.") # print error message if input is not a number
                                    continue  # ask user again to give an input
                            
                            # error handling for industry index selection
                            except:
                                print("\nError. Please insert an integer between 1 and 6. Please try again.") # print error message if input is not a number
                                continue  # ask user again to give an input
                        
                        #Target Stock is added to the peer array in order to be displayed in the graph
                        peers.append(target_stock)
                        break # index choice ends        
                    
                    # if input is neither yes nor no:
                    else:
                        print("\nError. Please insert 'yes' or 'no'. Please try again.") # print error message if input is not a number
                        continue  # ask user again to give an input
                
                # error handling
                except: 
                    print("\nError. Please insert 'yes' or 'no'. Please try again.") # print error message if input is not a number
                    continue  # ask user again to give an input    
                    
            # GET DATA AND PLOT IT                  
            # function to get data from yahoo api
            def yahoodata(ticker_list):
                # Get data from yahoo
                try:
                    series = pdr.DataReader(ticker_list, 'yahoo', start, end)
                    return series
                # Error handling
                except Exception as e:
                    print('Sorry, data is currently not available: ' + str(e))
            
            # get data
            df = yahoodata(peers)
            
            # use adj close
            adj_price = df['Adj Close']
            
            # compute stock returns
            stock_return = adj_price.apply(lambda x: x / x[0])
            stock_return.head() - 1
            
            # Figure Settings
            # change figure size
            plt.rcParams['figure.figsize'] = [13.5, 9]
            # axis, grids and lines:
            stock_return.plot(grid = True).axhline(y = 1, color = "black", lw = 1)
            # title
            plt.title("Indexed stock price performance comparison", fontsize=14, fontweight='bold')
            # label of x-axis
            plt.xlabel("time")
            # label of y-axis
            plt.ylabel("Indexed stock prices")
            # show plot
            plt.show()
            
            
################################################
# STEP 5.2: TARGET STOCK & VOLA PLOTS
###############################################
                    
            # Ask user whether he likes additional technical stock data plot
            print("\nDo you want to get additional technical stock data?")
            while True:
                try:
                    # let user answer
                    tech_stock_data = input("Please write Yes or No: ")
                    # if user wants additional technical stock data:
                    if tech_stock_data.lower() == "yes":
                        # get data from yahoo
                        stock_data = yahoodata(target_stock) 
                        stock_data_close = pd.DataFrame(stock_data.Close)
                        
                        # compute means                       
                        stock_data_close['MA_50'] = stock_data_close.Close.rolling(50).mean()
                        stock_data_close['MA_100'] = stock_data_close.Close.rolling(100).mean()

                        # Figure settings
                        # figure size
                        plt.figure(figsize = (15,10))
                        # activate grid
                        plt.grid(True)
                        # title
                        plt.title("Stock price with 100 day MA and 50 day MA", fontsize=14, fontweight='bold')
                        # Plot series with respective names
                        plt.plot(stock_data_close['Close'], label= 'Closing Price')
                        plt.plot(stock_data_close['MA_100'], label= 'MA 100 day')
                        plt.plot(stock_data_close['MA_50'], label= 'MA 50 day')
                        plt.legend(loc=2)
                        # label x-axis
                        plt.xlabel("time")
                        # label y-axis
                        plt.ylabel("stock price")
                        # show plot
                        plt.show()
                        
                        #VOLATILITY
                        # 1. Historic Volatility
                        stock_data_close['change'] = np.log(stock_data_close['Close'] / stock_data_close['Close'].shift())
                        
                        # Figure settings
                        # figure size
                        plt.figure(figsize = (10,5))
                        # title
                        plt.title("Historical volatility", fontsize=14, fontweight='bold')
                        # Plot series
                        plt.plot(stock_data_close.change, color ='g')
                        # label x-axis
                        plt.xlabel("time")
                        # label y-axis
                        plt.ylabel("change")
                        # show plot
                        plt.show()
                        
                        # 2. Rolling historically volatility
                        stock_data_close['volatility'] = stock_data_close.change.rolling(21).std().shift()
                        
                        # Figure settings
                        # figure size
                        plt.figure(figsize = (10,5))
                        # title
                        plt.title("Rolling historical volatility",fontsize=14, fontweight='bold')
                        # plot series
                        plt.plot(stock_data_close.volatility, color ='orange')
                        # label x-axis
                        plt.xlabel("time")
                        # label y-axis
                        plt.ylabel("change")
                        # show plot
                        plt.show()                       
                        break # additional technical data ends
                    
                    # if user does not want an additional analysis:
                    elif tech_stock_data.lower() == "no":
                        print("\nNo additional technical data will be provided.")
                        break # no additional analysis ends
                
                
                    else:
                       print("Error. You have to enter Yes or No. Please try again.") # print error message if input is not possible
                       continue # ask user again to give an input 
                    
                except ValueError: # error handling for technical analysis
                    print("Error. Data currently not available. Please try again later. ") # print error message if input is not possible
                    continue # ask user again to give an input                                
                
                break # fundamental stock analysis ends (yes case)
                                              
        # if continuation input for peer-group analysis is neither yes or no, give user another chance:
        else:
            print("\nError. Please insert 'yes' or 'no'. Please try again.") # print error message
            continue  # ask user again to give an input 
                  
    # error handling for peer-group analysis  
    except ValueError:
        print("\nError. Please insert 'yes' or 'no'. Please try again.") # print error message
        continue  # ask user again to give an input

    break #everything ends

print("\nThanks for using the tool. The program will now end.")