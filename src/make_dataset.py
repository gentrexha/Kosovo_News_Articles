# -*- coding: utf-8 -*-
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import pandas as pd
from utils import clean_text, remove_tags
from ast import literal_eval
from utils import NEWS_SITES, logger
from tqdm import tqdm
import lxml.html
from lxml import etree


def clean_html(_html_string: str):
    try:
        document = lxml.html.document_fromstring(_html_string)
        return "".join(etree.XPath("//text()")(document))
    except lxml.etree.ParserError as e:
        logger.error(f"Could not convert html string={_html_string} due to {e}. Returning empty string.")
        return ""


def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger.info("Making final data set from raw data.")

    clean_data()
    merge_data()


def merge_data():
    keys = NEWS_SITES.keys()

    dfs = []
    for news_site, web_page in tqdm(NEWS_SITES.items()):
        df = pd.read_csv(
            project_dir / f"data/processed/{news_site}.csv",
            dtype={"content": str, "title": str, "category": str, "author": str},
            parse_dates=["date"],
        )
        dfs.append(df)

    df = pd.concat([df.assign(source=key) for key, df in zip(keys, dfs)])

    df.to_csv(
        project_dir / f"data/processed/Kosovo-News-Articles.csv", index=False,
    )


def clean_data():
    for news_site, web_page in tqdm(NEWS_SITES.items()):
        # Load data
        logger.info(f"Loading {news_site} posts.")
        df = pd.read_csv(project_dir / f"data/raw/{news_site}_posts.csv", converters={"categories": literal_eval},)
        df_categories = pd.read_csv(project_dir / f"data/raw/{news_site}_categories.csv")
        # News sites without public authors
        na_authors = ["Bota_al", "JavaNews_al", "Kallxo.com", "Shekulli"]
        if news_site not in na_authors:
            df_users = pd.read_csv(project_dir / f"data/raw/{news_site}_users.csv")
        else:
            # Ballkani doesn't have public authors
            df_users = pd.DataFrame()

        # Drop rows with missing values
        df = df.dropna()

        # Clean text
        logger.info(f"Cleaning {news_site} posts text.")
        # todo: debug this if it is working as inteded.
        df["content"] = df["content"].apply(lambda x: clean_html(str(x)))
        df["content"] = clean_text(df["content"])

        # Add categories
        logger.info(f"Adding {news_site} categories.")
        df = df.explode("categories")
        df = df.reset_index(drop=False)
        df = pd.merge(df, df_categories, left_on="categories", right_on="id", how="left")
        df.drop(["id", "categories"], inplace=True, axis=1)
        df = (
            df.groupby(["index", "author", "content", "date", "title"])["category"]
            .apply(lambda x: ";".join(x.astype(str)))
            .reset_index()
        )

        # Add users
        logger.info(f"Adding {news_site} users.")
        if news_site not in na_authors:
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
    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
