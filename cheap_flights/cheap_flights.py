"""
    Check the cheapest flight prices via skyscanner's API and send an email if prices are changed.
    Check the main for settings
"""
import json
import requests
import datetime
import os.path
import time
import smtplib, ssl
from multiprocessing import Pool
from getpass import getpass
import smtplib, ssl

def check_price(flight_date_query):
    """
        It returns the price for a given date using skyscanners API. If there is an error, it tries it again, for 3 times. If there is no offer, it returns NA.

        Parameters
        -----------
        flight_date_query : date
            The date for which you want to know the price of the cheapest direct flight.
        
        Return
        -----------
        float or string
            The price of the cheapest flight, if there is any. If no direct flight is found, returns "NA". In case there is an error with the API, returns "Error".
    """
    for i in range(3):
        url_wo_date = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/HU/EUR/hu/BUD-sky/DUB-sky/"
        headers = {
        'x-rapidapi-key': "34f96b7f2dmsh9deeb4335229e7bp16bc0cjsnf843e4da5c96",
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        }

        url = url_wo_date + flight_date_query.isoformat()
        response = requests.request("GET", url, headers=headers)
        interpreted = json.loads(response.text)

        if "Quotes" in interpreted:
            if interpreted["Quotes"]:
                minPrice = interpreted["Quotes"][0]["MinPrice"]
                return minPrice
                    
            else:
                return "NA"
        else:
            pass # unsuccessful request

        time.sleep(1)
        
    
    # no success after 3 trial
    print("An error occured requesting flight prices", flight_date_query.isoformat())
    return "Error"

if __name__ == '__main__':
    """
        This part is needed for the multiprocessing module.
    """

    # region settings
    flight_date = datetime.date(2021,1,3)   # starting point of the flights
    days = 30   # how many days should be checked

    port = 465  # For SSL
    emailpass = getpass()
    sender_email = "eltecomputeservers@gmail.com"
    receiver_email = "tuzesdaniel@gmail.com"
    subject = "Subject: new flight price\n\n"

    # endregion settings

    flight_dates = [flight_date]
    flight_prices = []

    for i in range(days):
        flight_dates.append(flight_dates[-1] + datetime.timedelta(days=1))
        flight_prices.append("")

    # Run this with a pool of 5 agents having a chunksize of 3 until finished
    nof_processes = min(days,50)

    ofile=open("flight_prices.dat","a")
    price_header = "# flight date\tflight price\toffer date\told flight price [€]\n"
    print(price_header, file=ofile, flush=True)
    
    while os.path.exists("delete_to_stop.md"):

        # get prices parallel
        with Pool(processes=nof_processes) as pool:
            result = pool.map(check_price, flight_dates, int(days/nof_processes))
        
        # if there will be new prices, a mail will be sent, and this mail's body is messagebody
        messagebody = price_header
        
        for i in range(days):
            if flight_prices[i] != result[i]:
                entry = flight_dates[i].isoformat() + "\t" + str(result[i]) + "\t" + str(datetime.datetime.now()) + "\t" + str(flight_prices[i])
                print(entry, file=ofile)
                messagebody += entry + "\n"
                flight_prices[i] = result[i]
        
        ofile.flush()
        if messagebody != price_header: # send an email
            context = ssl.create_default_context()
            message = subject + messagebody
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login(sender_email, emailpass)
                server.sendmail(sender_email, receiver_email, message.encode("utf8"))
                server.quit
            messagebody = price_header
            
        time.sleep(300)

    # the sciprt needs to stop because delete_to_stop.md cannot be found
    print("The file `delete_to_stop.md` has been deleted, python script stops now:", datetime.datetime.now())