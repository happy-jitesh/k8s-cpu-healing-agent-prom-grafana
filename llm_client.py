from openai import OpenAI

from config import (
    BASE_URL,
    API_KEY,
    MODEL
)

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)


def ask_llm(prompt):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content