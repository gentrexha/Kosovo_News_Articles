# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import pandas as pd
from utils import clean_text, remove_tags
from ast import literal_eval
from utils import NEWS_SITES
from tqdm import tqdm
from lxml.html.clean import clean_html


def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info("Making final data set from raw data.")

    # clean_data(logger)
    merge_data(logger)


def merge_data(logger):
    keys = NEWS_SITES.keys()

    dfs = []
    for news_site, web_page in tqdm(NEWS_SITES.items()):
        df = pd.read_csv(
            project_dir / f"data/processed/{news_site}.csv",
            dtype={"content": str, "title": str, "category": str, "author": str},
            parse_dates=['date'],
        )
        dfs.append(df)

    df = pd.concat([df.assign(source=key) for key, df in zip(keys, dfs)])

    df.to_csv(
        project_dir / f"data/processed/Kosovo-News-Articles.csv",
        index=False,
    )


def clean_data(logger):
    for news_site, web_page in tqdm(NEWS_SITES.items()):
        # Load data
        logger.info(f"Loading {news_site} posts.")
        df = pd.read_csv(
            project_dir / f"data/raw/{news_site}_posts.csv",
            converters={"categories": literal_eval},
        )
        df_categories = pd.read_csv(
            project_dir / f"data/raw/{news_site}_categories.csv"
        )
        if news_site != "Ballkani":
            df_users = pd.read_csv(project_dir / f"data/raw/{news_site}_users.csv")
        else:
            # Ballkani doesn't have public authors
            df_users = pd.DataFrame()

        # Drop rows with missing values
        df = df.dropna()

        # Clean text
        logger.info(f"Cleaning {news_site} posts text.")
        if news_site == 'Telegrafi':
            df["content"] = clean_text(df["content"])
            df["content"] = df["content"].apply(lambda x: remove_tags(str(x)))
        else:
            df["content"] = df["content"].apply(lambda x: clean_html(str(x)))
            df["content"] = clean_text(df["content"])

        # Add categories
        logger.info(f"Adding {news_site} categories.")
        df = df.explode("categories")
        df = df.reset_index(drop=False)
        df = pd.merge(
            df, df_categories, left_on="categories", right_on="id", how="left"
        )
        df.drop(["id", "categories"], inplace=True, axis=1)
        df = (
            df.groupby(["index", "author", "content", "date", "title"])["category"]
            .apply(lambda x: ";".join(x.astype(str)))
            .reset_index()
        )

        # Add users
        logger.info(f"Adding {news_site} users.")
        if news_site != "Ballkani":
            df = pd.merge(df, df_users, left_on="author", right_on="id", how="left")
            df.drop(["author_x", "id", "index"], inplace=True, axis=1)
        else:
            df["author"] = "Unknown"
            df.drop(["index"], inplace=True, axis=1)

        # Save data
        logger.info(f"Saving {news_site} data.")
        df.to_csv(
            project_dir / f"data/processed/{news_site}.csv",
            index=False,
            header=["content", "date", "title", "category", "author"],
        )


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
