# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from utils import NEWS_SITES
import requests
import pandas as pd


@click.command()
@click.argument("per_page", type=int, default=100)
def main(per_page: int = 100):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info("Started making requests to News Sites.")

    for news_site, web_page in NEWS_SITES.items():
        extract_posts(logger, news_site, per_page, web_page)
        extract_categories(logger, news_site, web_page)


def extract_post_data(_post: dict) -> dict:
    post = {
        "date": _post["date"],
        "title": _post["title"]["rendered"],
        "categories": _post["categories"],
        "author": _post["author"],
        "content": _post["content"]["rendered"],
    }
    return post


def extract_categories(logger, news_site, web_page, per_page):
    logger.info(f"Starting getting categories of {news_site}")
    result = pd.DataFrame()
    page = 1
    while True:
        # Create url
        api = f"wp-json/wp/v2/categories?page={page}&per_page={per_page}"
        url = web_page + api
        # Make request
        r = requests.get(url=url)
        # Extracting data in json format
        categories = r.json()

        if len(categories) == 0:  # TODO: Check if this is the correct error code
            logger.info(f"No more categories could be found for {news_site} at page={page}")
            break  # no more posts returned
        else:
            logger.info(f"Getting {per_page} categories at page={page}")
            temp = pd.DataFrame()
            for i in range(1, len(categories)):
                post_data = extract_category_data(categories[i])
                temp = temp.append(pd.DataFrame(post_data), ignore_index=True)
        page += 1
        # TODO: Append data to general dataframe and save current progress
        result = result.append(temp, ignore_index=True)
        result.to_csv(f"../data/{news_site}_posts.csv")


def extract_posts(logger, news_site, per_page, web_page):
    logger.info(f"Starting getting posts of {news_site}")
    result = pd.DataFrame()
    page = 1
    while True:
        # Create url
        api = f"wp-json/wp/v2/posts?page={page}&per_page={per_page}"
        url = web_page + api
        # Make request
        r = requests.get(url=url)
        # Extracting data in json format
        posts = r.json()
        if "code" in posts:  # TODO: Check if this is the correct error code
            logger.info(f"No more posts could be found for {news_site} at page={page}")
            break  # no more posts returned
        else:
            logger.info(f"Getting {per_page} posts at page={page}")
            temp = pd.DataFrame()
            for i in range(0, 100):
                post_data = extract_post_data(posts[i])
                temp = temp.append(pd.DataFrame(post_data), ignore_index=True)
        page += 1
        # TODO: Append data to general dataframe and save current progress
        result = result.append(temp, ignore_index=True)
        result.to_csv(f"../data/{news_site}_posts.csv")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
