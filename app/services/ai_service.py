from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def ask_openai(question: str, transaction: list[dict]) -> str:
    prompt = f"""
Ты финансовый помощник.

Отвечай только на основе данных пользователя.
Если данных недостаточно, скажи , что данных недостаточно.

Вопрос пользователя:
{question}

Транзакции пользователя:
{transaction}
"""
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt,
    )
    return response.output_text