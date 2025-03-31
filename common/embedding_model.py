from openai import OpenAI
# from sentence_transformers import SentenceTransformer
import pandas as pd
import ast
from dotenv import load_dotenv
import os


load_dotenv()


def openai_embedding(text_data: list[str] | str):

    """

    df = pd.read_excel(r"./gpt_texts.xlsx")[:3]
    df["openai_embedding"] = df["gpt 정제"].apply(lambda x: openai_embedding(x))
    df["openai_embedding"] = df["openai_embedding"].apply(eval).apply(np.array) # convert string to array
    df["openai_embedding"] = df["openai_embedding"].apply(lambda x: x.tolist() if isinstance(x, np.ndarray) else x)
    df.to_csv('./embedded_data.csv', index=False)

    """

    embedding_client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY", None),
    )

    models = embedding_client.models.list()
    # print(models)

    responses = embedding_client.embeddings.create(
        input=text_data,
        model="text-embedding-3-small",  # embedding dimension size = 1536
    )

    return responses.data[0].embedding


# def local_embedding(text_data: list[str] | str, output_dim=False):
#     # Initialize your custom embedding model
#     embedding_model = SentenceTransformer("dragonkue/BGE-m3-ko")
#
#     if output_dim:
#         # Dimension of embeddings model
#         embedding_dim = int(embedding_model[1].word_embedding_dimension)
#         return embedding_dim
#
#     return embedding_model.encode(text_data).tolist()


def save_embedding(text_data_path, text_column):
    df = pd.read_excel(text_data_path)
    df["openai_embedding"] = df[text_column].apply(lambda x: openai_embedding(x))
    df.to_csv('./gto_embedded_data.csv', index=False)

    print("saved!")


def load_embedding(text_data_path):
    df = pd.read_csv(text_data_path)
    df["openai_embedding"] = df["openai_embedding"].apply(ast.literal_eval)

    return df["openai_embedding"].to_list()


if __name__ == '__main__':
    docs = [
        """복지 메뉴의 어르신 카테고리의 시설 안내에는 장기 요양 시설에 대한 내용이 포함되어 있다. 시흥시 오동마을로 6번길 6, 4층에 위치한 장기요양시설의 연락처는 031-435-2000이다. 정왕동에는 아가페 재가복지센터가 경기도 시흥시 서울대학로264번길 35, 601호에 있으며, 연락처는 031-318-9924이다. 또한 정왕동에는 참사랑방문요양이 경기도 시흥시 중심상가로 155, 503호에 위치하고 연락처는 031-432-1477이다. 큰솔재가복지센터는 경기도 시흥시 큰솔공원로 30에 있으며, 연락처는 031-699-0650이다. 시흥돌봄장기요양센터는 경기도 시흥시 오동마을로6번안길 34에 위치하고 연락처는 031-509-8284이다. 효사랑방문요양센터는 경기도 시흥시 옥구천동로 449, 2층 208호에 있으며, 연락처는 031-318-6722이다. 무지개어르신 재가복지센터는 경기도 시흥시 오이도로157번길 32, 101호에 위치하고, 연락처는 031-317-0005이다. 더하기노인복지센터는 경기도 시흥시 옥구천서로373번길 8, 1층에 있으며, 연락처는 070-8877-8852이다. 홍익노인재가센터는 경기도 시흥시 정왕신길로49번길 19, 2층 210호에 위치하고 연락처는 031-312-0321이다. 참평안 재가방문요양센터는 경기도 시흥시 공단1대로 204, 34동 323호에 있으며,"""
    ]

    # print(openai_embedding(docs[0]) == openai_embedding(docs))

    # save_embedding(r"./gpt_texts.xlsx")
    # print(load_embedding('./embedded_data.csv'))

    # df = pd.read_excel(r"./gpt_texts.xlsx")[:10]
    # df["openai_embedding"] = df["gpt 정제"].apply(lambda x: openai_embedding(x))
    # print(df)

    save_embedding(text_data_path=r"C:\Users\gukhwan\OneDrive - (주)스위트케이\바탕 화면\RAVEN\lab\search_engine\qdrant\gto_proposal_processed.xlsx", text_column="processed")