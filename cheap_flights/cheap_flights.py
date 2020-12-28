"""
    Check the cheapest flight prices via skyscanner's API and send an email if prices are changed.
    Check the main for settings
"""
import json
import datetime
import os.path
import codecs
import time
import smtplib
import ssl
from multiprocessing import Pool
from getpass import getpass
from itertools import product
import requests


def check_price(flight_date_query, apikey):
    """Returns the price for a given date using skyscanners API.
    If there is an error, it tries it again, for 3 times.
    If there is no offer, it returns NA.

        Parameters
        -----------
        flight_date_query : date
            The date for which you want to know the price of the cheapest direct flight.

        Return
        -----------
        float or string
            The price of the cheapest flight, if there is any.
            If no direct flight is found, returns "NA".
            In case there is an error with the API, returns "Error".
    """
    for _ in range(3):
        url_wo_date = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/HU/EUR/hu/BUD-sky/DUB-sky/"
        headers = {
            'x-rapidapi-key': apikey,
            'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        }

        url = url_wo_date + flight_date_query.isoformat()
        response = requests.request("GET", url, headers=headers)
        interpreted = json.loads(response.text)

        if "Quotes" in interpreted:
            if interpreted["Quotes"]:
                min_price = interpreted["Quotes"][0]["MinPrice"]
                return min_price
            return "NA"

        time.sleep(1)

    # no success after 3 trial
    print("An error occured requesting flight prices",
          flight_date_query.isoformat())
    return "Error"


if __name__ == '__main__':

    # region settings
    flight_date = datetime.date(2021, 1, 3)   # starting point of the flights
    DAYS = 30   # how many days should be checked

    PORT = 465  # For SSL
    emailpass = getpass("Enter password for e-mail: ")
    SENDER_EMAIL = "eltecomputeservers@gmail.com"
    RECEIVER_EMAIL = "tuzesdaniel@gmail.com"
    SUBJECT = "Subject: new flight price\n\n"

    apikey_array = []
    # this way starmap can be fed with (date,key) pairs
    apikey_array.append(input("Enter rapidapi key: "))
    # endregion settings

    flight_dates = [flight_date]
    flight_prices = []

    for i in range(DAYS):
        flight_dates.append(flight_dates[-1] + datetime.timedelta(days=1))
        flight_prices.append("")

    # Run this with a pool of 5 agents having a chunksize of 3 until finished
    nof_processes = min(DAYS, 50)

    ofile = codecs.open("flight_prices.dat", "a", "utf-8")
    PRICE_HEADER = "# flight date\tflight price\toffer date\told flight price [€]"
    print(PRICE_HEADER, file=ofile, flush=True)

    while os.path.exists("delete_to_stop.md"):

        # get prices parallel
        with Pool(processes=nof_processes) as pool:
            result = pool.starmap(check_price, product(
                flight_dates, apikey_array), int(DAYS/nof_processes))

        # if there will be new prices, a mail will be sent, and this mail's body is messagebody
        MESSAGE_BODY = PRICE_HEADER

        for i in range(DAYS):
            if flight_prices[i] != result[i]:
                entry = flight_dates[i].isoformat() + "\t" + str(result[i]) + "\t" + str(
                    datetime.datetime.now()) + "\t" + str(flight_prices[i])
                print(entry, file=ofile)
                MESSAGE_BODY += "\n" + entry
                flight_prices[i] = result[i]

        ofile.flush()
        if MESSAGE_BODY != PRICE_HEADER:  # send an email
            context = ssl.create_default_context()
            message = SUBJECT + MESSAGE_BODY
            with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
                server.login(SENDER_EMAIL, emailpass)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL,
                                message.encode("utf8"))
            MESSAGE_BODY = PRICE_HEADER

        time.sleep(300)

    # the sciprt needs to stop because delete_to_stop.md cannot be found
    print("The file `delete_to_stop.md` has been deleted, python script stops now:",
          datetime.datetime.now())
