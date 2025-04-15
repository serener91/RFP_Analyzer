from openai import OpenAI
from sentence_transformers import SentenceTransformer
import pandas as pd
import ast
from dotenv import load_dotenv
import os
import json

load_dotenv()


def get_openai_embedding(text_data: list[str] | str, get_model_names: bool = False):

    """
    Get OpenAI embedding values for list of texts
    """

    embedding_client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY", None),
    )

    if get_model_names:
        models = embedding_client.models.list()
        return models

    else:
        responses = embedding_client.embeddings.create(
            input=text_data,
            model="text-embedding-3-small",  # embedding dimension size = 1536
        )

        return responses.data[0].embedding


def get_oss_embedding(text_data: list[str] | str, output_dim=False):

    """
    Get open-source model embedding values for list of texts
    """

    embedding_model = SentenceTransformer("dragonkue/BGE-m3-ko")
    if output_dim:
        # Returns a dimension of embeddings model
        embedding_dim = int(embedding_model[1].word_embedding_dimension)
        return embedding_dim

    return embedding_model.encode(text_data).tolist()


def save_embedding(text_data_path, text_column, openai_emd=True):

    """
    Get embedding values from either OpenAI or Open Sourced model and save it as CSV file
    """

    df = pd.read_excel(text_data_path)
    df["embedding"] = df[text_column].apply(lambda x: get_openai_embedding(text_data=x) if openai_emd else get_openai_embedding(text_data=x))
    df.to_csv('./embedding_values.csv', index=False)
    print("saved!")


def load_embedding(text_data_path):

    """
    Load embedding values from CSV file
    """

    df = pd.read_csv(text_data_path)
    # df["embedding"] = df["embedding"].apply(ast.literal_eval)
    df["embedding"] = df["embedding"].apply(json.loads)
    return df["embedding"].to_list()
