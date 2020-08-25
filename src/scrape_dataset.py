# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from utils import NEWS_SITES
import requests
import pandas as pd
import time
import random


# TODO: Improve click commands
@click.command()
@click.argument("per_page", type=int, default=100)
def main(per_page: int = 100):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info("Started making requests to News Sites.")

    for news_site, web_page in NEWS_SITES.items():
        extract_specific_data(logger, news_site, web_page, extract_type='categories')
        extract_specific_data(logger, news_site, web_page, extract_type='users')
        extract_posts(logger, news_site, web_page)


def extract_post_data(_post: dict) -> dict:
    post = {
        "date": _post["date"],
        "title": _post["title"]["rendered"],
        "categories": _post["categories"],
        "author": _post["author"],
        "content": _post["content"]["rendered"],
    }
    return post


def extract_category_data(_category: dict):
    category = {"id": _category["id"], "category": _category["name"]}
    return category


def extract_author_data(_author: dict):
    category = {"id": _author["id"], "author": _author["name"]}
    return category


def extract_specific_data(logger, news_site, web_page, per_page=100, page=1, extract_type='categories'):
    assert extract_type == 'categories' or 'users'
    logger.info(f"Starting getting {extract_type} of {news_site}")
    result = pd.DataFrame()
    while True:
        # Sleep to prevent any random blocks or limitations
        time.sleep(random.randint(30, 60))
        # Create url
        api = f"wp-json/wp/v2/{extract_type}?page={page}&per_page={per_page}"
        url = web_page + api
        # Make request
        r = requests.get(url=url)
        # Extracting data in json format
        data = r.json()

        if len(data) == 0:
            logger.info(
                f"No more {extract_type} could be found for {news_site} at page={page}"
            )
            break
        else:
            logger.info(f"Getting {per_page} {extract_type} at page={page}")
            temp = pd.DataFrame()
            for i in range(1, len(data)):
                if extract_type is 'categories':
                    extracted_data = extract_category_data(data[i])
                    temp = temp.append(extracted_data, ignore_index=True)
                elif extract_type is 'users':
                    extracted_data = extract_category_data(data[i])
                    temp = temp.append(extracted_data, ignore_index=True)
                else:
                    logger.info(f"Error: extract_type={extract_type} not found!")
        page += 1
        result = result.append(temp, ignore_index=True)
        result.to_csv(f"../data/{news_site}_{extract_type}.csv", index=False)


def extract_posts(logger, news_site, web_page, per_page=100, page=1):
    logger.info(f"Starting getting posts of {news_site}")
    result = pd.DataFrame()
    while True:
        # Sleep to prevent any random blocks or limitations
        time.sleep(random.randint(30, 60))
        # Create url
        api = f"wp-json/wp/v2/posts?page={page}&per_page={per_page}"
        url = web_page + api
        # Make request
        r = requests.get(url=url)
        # Extracting data in json format
        posts = r.json()
        if "code" in posts:
            logger.info(f"No more posts could be found for {news_site} at page={page}")
            break  # no more posts returned
        else:
            logger.info(f"Getting {per_page} posts at page={page}")
            temp = pd.DataFrame()
            for i in range(0, 100):
                post_data = extract_post_data(posts[i])
                temp = temp.append(post_data, ignore_index=True)
        page += 1
        result = result.append(temp, ignore_index=True)
        result.to_csv(f"../data/{news_site}_posts.csv", index=False)


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
