# -*- coding: utf-8 -*-
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from utils import NEWS_SITES, logger
import requests
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from random import choice, randint


def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger.info("Started making requests to News Sites.")

    for news_site, web_page in NEWS_SITES.items():
        extract_specific_data(news_site, web_page, extract_type="categories")
        extract_specific_data(news_site, web_page, extract_type="users")
        extract_posts(news_site, web_page)


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


def extract_specific_data(
    news_site, web_page, per_page=100, starting_page=1, extract_type="categories", page_checkpoint=10, headers=True,
):
    assert extract_type == "categories" or "users"
    logger.info(f"Starting getting {extract_type} of {news_site}")
    result = pd.DataFrame()
    try:
        # Find out total number of pages
        api = f"wp-json/wp/v2/{extract_type}?page={starting_page}&per_page={per_page}"
        url = web_page + api
        # create headers
        if headers:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/84.0.4147.135 Safari/537.36 "
            }
            # Make request
            r = requests.get(url=url, headers=headers)
        else:
            r = requests.get(url=url)
        # Extracting header information
        total_posts = int(r.headers["X-WP-Total"])
        total_pages = int(r.headers["X-WP-TotalPages"])
        logger.info(f"{news_site} has {total_posts} {extract_type} and {total_pages} pages.")
    except Exception as e:
        logger.info(e)
        logger.info(f"Failed getting total posts and pages of {news_site}.")
        return
    for page in tqdm(range(starting_page, total_pages + 1), desc=f"{extract_type}"):
        try:
            # Create url
            api = f"wp-json/wp/v2/{extract_type}?page={page}&per_page={per_page}"
            url = web_page + api
            # create headers
            if headers:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/84.0.4147.135 Safari/537.36 "
                }
                # Make request
                r = requests.get(url=url, headers=headers)
            else:
                r = requests.get(url=url)
            # Extracting data in json format
            data = r.json()

            if len(data) == 0:
                logger.info(f"No more {extract_type} could be found for {news_site} at page={page}")
                break
            else:
                temp = pd.DataFrame()
                for i in range(1, len(data)):
                    if extract_type is "categories":
                        extracted_data = extract_category_data(data[i])
                        temp = temp.append(extracted_data, ignore_index=True)
                    elif extract_type is "users":
                        extracted_data = extract_author_data(data[i])
                        temp = temp.append(extracted_data, ignore_index=True)
                    else:
                        logger.info(f"Error: extract_type={extract_type} not found!")
            result = result.append(temp, ignore_index=True)
            if page % page_checkpoint == 0 or page == total_pages or page == total_pages - 1:
                result.to_csv(f"../data/raw/{news_site}_{extract_type}.csv", index=False)
        except Exception as e:
            logger.info(e)
            logger.info(f"Failed getting {news_site} {per_page} {extract_type} at page={page}")


def extract_posts(
    news_site, web_page, per_page=100, starting_page=1, rerun=False, page_checkpoint=100, headers=True,
):
    session = requests.Session()
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.177 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15",
    ]
    logger.info(f"Starting getting posts of {news_site}")
    result = pd.DataFrame()
    try:
        # Find out total number of pages
        api = f"wp-json/wp/v2/posts?page={starting_page}&per_page={per_page}"
        url = web_page + api
        # create headers
        if headers:
            r = session.get(url=url, timeout=10, headers={
                "User-Agent": choice(user_agents),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Referer": web_page
            })
        else:
            r = session.get(url=url)
        # Extracting header information
        total_posts = int(r.headers["X-WP-Total"])
        total_pages = int(r.headers["X-WP-TotalPages"])
        logger.info(f"{news_site} has {total_posts} posts and {total_pages} pages.")
    except Exception as e:
        logger.info(e)
        logger.info(f"Failed getting total posts and pages of {news_site}.")
        return
    for page in tqdm(range(starting_page, total_pages + 1), desc="Page"):
        try:
            # Create url
            api = f"wp-json/wp/v2/posts?page={page}&per_page={per_page}"
            url = web_page + api
            # create headers
            if headers:
                r = session.get(url=url, timeout=10, headers={
                        "User-Agent": choice(user_agents),
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Referer": web_page
                    })
            else:
                r = session.get(url=url)
            # Extracting data in json format
            posts = r.json()
            if "code" in posts:
                logger.info(f"No more posts could be found for {news_site} at page={page}")
                break  # no more posts returned
            else:
                temp = pd.DataFrame()
                for i in range(0, per_page):
                    post_data = extract_post_data(posts[i])
                    temp = temp.append(post_data, ignore_index=True)
            result = result.append(temp, ignore_index=True)
            if page % page_checkpoint == 0 or page == total_pages or page == total_pages - 1:
                if rerun:
                    result.to_csv(
                        f"../data/raw/{news_site}_posts_{datetime.now().strftime('%Y_%m_%d')}.csv", index=False,
                    )
                else:
                    result.to_csv(f"../data/raw/{news_site}_posts.csv", index=False)
        except Exception as e:
            logger.info(e)
            logger.info(f"Failed getting {news_site} {per_page} posts at page={page}")


if __name__ == "__main__":
    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
