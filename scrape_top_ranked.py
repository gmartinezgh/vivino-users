import requests
import re
import logging
import pandas as pd
import time
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

COUNTRY_RANKING_URL = "https://www.vivino.com/users/x/country_rankings"
USERS_URL = "http://app.vivino.com/api/users/{seo_name}"
FOLLOWERS_URL = "http://app.vivino.com/api/users/{user_id}/followers"
FOLLOWING_URL = "http://app.vivino.com/api/users/{user_id}/following"


def retrieve_top_ranked_users(countries=["fr", "it", "es"], extract_per_country=10):
    logging.info(
        f"Parsing top ranked {extract_per_country} users from countries {countries}"
    )
    users_per_page = 10

    seo_names = set()
    pages = extract_per_country // users_per_page if extract_per_country >= 10 else 1
    for country in countries:
        for i in range(1, pages + 1):
            data = {"page": i, "country_code": country}
            headers = {"Content-Type": "application/json", "User-Agent": "postman"}
            response = requests.post(COUNTRY_RANKING_URL, json=data, headers=headers)
            found = re.findall(
                r"href=\\\'\/users\/([A-Za-z0-9.-]+)\\\'><figure", response.text
            )
            seo_names.update(found)

    return seo_names


def retrieve_user_info(seo_name):
    logging.debug(f"Parsing information on user {seo_name}")

    response = requests.get(USERS_URL.format(seo_name=seo_name))
    return response.json()


def retrieve_followers(user_id, limit=10):
    logging.debug(f"Parsing followers of user {user_id}")

    params = {"start_from": 0, "limit": limit}
    response = requests.get(FOLLOWERS_URL.format(user_id=user_id), params=params)
    if response.status_code != 200:
        return []
    return [user["id"] for user in response.json()]


def retrieve_following(user_id, limit=10):
    logging.debug(f"Parsing followings of user {user_id}")

    params = {"start_from": 0, "limit": limit}
    response = requests.get(FOLLOWING_URL.format(user_id=user_id), params=params)
    if response.status_code != 200:
        return []
    return [user["id"] for user in response.json()]


def scrape_vivino_users():
    users = []

    top_ranked_seo_names = retrieve_top_ranked_users(
        countries=["fr", "it", "es", "us", "ch", "de", "ru", "gb", "au", "ca"],
        extract_per_country=1000,
    )
    for seo_name in top_ranked_seo_names:
        info = retrieve_user_info(seo_name)
        if info["visibility"] != "all":
            #do not scrape users that need authorization to retrieve followers/following
            continue

        user_id = info["id"]
        info["followers"] = retrieve_followers(user_id, limit = 10000)
        info["following"] = retrieve_following(user_id, limit = 10000)

        users.append(info)

        logging.info(f"Retrieved info for user {seo_name}, id: {user_id}")

    df = pd.DataFrame(users)

    return df


start = time.time()
df = scrape_vivino_users()
print(f"Scraping {len(df)} users took {time.time() - start} seconds")

df.to_pickle("./vivino_top_ranked.pkl")

