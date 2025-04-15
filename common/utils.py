from openai import OpenAI, AsyncOpenAI
from langfuse import Langfuse
from dotenv import load_dotenv
import os


load_dotenv(r"C:\Users\gukhwan\OneDrive - (주)스위트케이\바탕 화면\ChatRFP\monitoring\.env")


def fetch_prompt(prompt_id, label="latest", version=None):
    """

    [Dev Only]
    Get prompt from langfuse server

    """
    langfuse = Langfuse(
        host="http://localhost:3000"
    )
    if version is None:
        return langfuse.get_prompt(prompt_id, label=label).compile()

    else:
        return langfuse.get_prompt(prompt_id, version=version).compile()


def inference(gpt=False, system_msg="", query="", model="gpt-4o-mini", temperature=0.2):

    """
    Calls for OpenAI or OpenAI-Compatible Server
    """

    if gpt:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", None)
        )

        message = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": query}
        ]

        chat_response = client.chat.completions.create(
            model=model,
            messages=message,
            temperature=temperature,
            max_completion_tokens=8192,
            stream=False
        )

        return chat_response.choices[0].message.content

    client = OpenAI(
        api_key="test123",
        base_url="http://175.196.78.7:30000/v1",
    )

    message = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": query}
    ]

    chat_response = client.chat.completions.create(
        model="vllm",
        messages=message,
        temperature=temperature,
        max_completion_tokens=8192,
        stream=False
    )

    return chat_response.choices[0].message.content


async def ainference(gpt=False, system_msg="", query="", model="gpt-4o-mini", temperature=0.2):
    if gpt:
        client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY", None),
        )

        message = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": query}
        ]

        # Await the response
        chat_response = await client.chat.completions.create(
            model=model,
            messages=message,
            temperature=temperature,
            max_completion_tokens=8192,
            stream=False
        )

        return chat_response.choices[0].message.content


def convert_to_html(filepath="./sample.html", file_name=None, budget_text=None, time_text=None, mar_text=None, sfr_text=None):

    """
    Convert final output as formatted html

    """

    text_style = """
    <style>
            body {
                font-family: sans-serif;
                line-height: 1.6;
                margin: 20px;
            }
            h2 {
                color: #333;
                border-bottom: 2px solid #eee;
                padding-bottom: 10px;
            }
            ul {
                list-style-type: disc;
                margin-left: 20px;
            }
            li {
                margin-bottom: 8px;
            }
            .summary {
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
        </style>
    """

    html_text = f"""
            <!DOCTYPE html>
            <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                {text_style}
            </head>
            <body>

                <h2>RFP Summary</h2>

                <div class="summary">
                    <p>문서명: {file_name}</p>
                    <p>{budget_text}</p>
                    <p>{time_text}</p>
                </div>

                <h2>MAR 핵심 사항</h2>

                <ul>
                    {mar_text}
                </ul>

                <h2>SFR 핵심 사항</h2>

                <ul>
                    {sfr_text}
                </ul>

            </body>
            </html>
            """

    # with open(filepath, "w", encoding="utf-8") as f:
    #     f.write(html_text)

    print("HTML converted and saved!")

    return html_text


