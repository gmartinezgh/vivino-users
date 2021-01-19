# This script scrapes the top rated wines of a given set of vivino users from the vivino user pages
# "https://www.vivino.com/users/{user_id}/top"
# Web scraping is done with the package selenium, mozilla firefox and a webdriver for mozilla firefox: geckodriver
# https://selenium-python.readthedocs.io/installation.html#drivers
# Both mozilla firefox and geckodriver executables must be reachable via PATH environment variable

from selenium import webdriver
import re
import os
import pandas as pd
import logging
import time
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = spark._jvm.org.apache.log4j
logging.getLogger("py4j").setLevel(logging.ERROR)

USER_TOP_WINES_URL = "https://www.vivino.com/users/{user_id}/top"

webdrivers_path = "."
os.environ['PATH'] = os.getenv('PATH') + ":" + webdrivers_path


def new_webdriver(interactive=True):
    firefox_options = webdriver.firefox.options.Options()
    firefox_options.headless = not interactive
    return webdriver.Firefox(options=firefox_options)


def get_top_wines_of_user(user_id, driver):
    logging.debug(f"Scraping top ranked wines of user {user_id}")

    driver.get(USER_TOP_WINES_URL.format(user_id=user_id))

    wine_links = driver.find_elements_by_xpath('//a[@class="link-muted bold"]')
    wine_ids = [int(re.findall("/\d+", w.get_attribute("href"))[0].replace("/", "")) for w in wine_links]
    wine_names = [w.text for w in wine_links]

    ratings = driver.find_elements_by_xpath(
        '//div[@class="wine-rating row-no-gutter clearfix"]'
        '/div[@class="col-xs-4 col-sm-3 text-center"]'
        '/div[@class="row-no-gutter"]'
        '/span[@class="header-large text-block"]')
    wine_ratings = [float(x.text) for x in ratings]

    prices = driver.find_elements_by_xpath(
        '//div[@class="wine-rating row-no-gutter clearfix"]'
        '/div[@class="col-xs-4 col-sm-3 text-center"]'
        '/span[@class="header-large text-block wine-info-value wine-price-value"]')
    wine_prices = [float(x.text.replace("-", "0").replace(",", "")) for x in prices]

    user_ratings = driver.find_elements_by_xpath(
        '//div[@class="activity-rating text-small rating-section activity-section clearfix"]'
        '/span[@class="rating rating-xs text-inline-block"]')

    wine_user_ratings = [
        sum([int(re.findall("\d+", x.get_attribute("class"))[0])
             for x in w.find_elements_by_xpath("i")]
            ) / 100
        for w in user_ratings
    ]

    # Error control
    it = iter([wine_ids, wine_names, wine_user_ratings, wine_prices, wine_ratings])
    the_len = len(next(it))
    if not all(len(l) == the_len for l in it):
        logging.info(f"user_id {user_id}. Not all wine attributes lists have same length!")
        user_top_wines = {"wine_id": "", "name": "", "user_rating": "", "price": "", "rating": ""}
    else:
        user_top_wines = {
            "wine_id": wine_ids,
            "name": wine_names,
            "user_rating": wine_user_ratings,
            "price": wine_prices,
            "rating": wine_ratings
        }

    return user_top_wines


def scrape_vivino_users_ratings(users_df, batch_size=100, side_effect_writing=False, write_to_file=None):

    batches = len(users_df) // batch_size + 1
    df = pd.DataFrame()
    for i in range(0, batches):
        logging.info(f"Scraping top ranked wines batch {i+1}/{batches}")
        driver = new_webdriver(interactive=False)
        for user_id in users_df.id[batch_size * i:batch_size * (i + 1)]:
            top_wines = get_top_wines_of_user(user_id, driver)
            top_wines["user_id"] = [user_id] * len(top_wines["wine_id"])
            df = df.append(pd.DataFrame(top_wines))
        if side_effect_writing:
            # intermediate copies of the results to overcome system instability
            logging.info(f"Side effect writing selected. Writing batch {i+1} to disk")
            df.to_pickle("./" + write_to_file)
        driver.close()

    return df


# users_df contains most popular vivino users. Generated in scrape_top_ranked.py
users_df = pd.read_pickle('/dbfs/FileStore/shared_uploads/gustavo.martinez@mirai-solutions.com/vivino_top_ranked.pkl')

start = time.time()
ratings_df = scrape_vivino_users_ratings(users_df, batch_size=100, side_effect_writing=True, write_to_file="vivino_ratings.pkl")
print(f"Scraping {len(ratings_df)} wines took {time.time() - start} seconds")
