from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

client=Groq(api_key=os.getenv("GROQ_API_KEY"))


def test_groq():
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": "Say hello in one sentence."
            }
        ],
        temperature=0
    )

    print(response.choices[0].message.content)
if __name__ == "__main__":
    test_groq()