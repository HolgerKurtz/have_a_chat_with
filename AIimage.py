import os
import openai
from dotenv import load_dotenv

load_dotenv()


def generate_image(prompt_text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Image.create(
        prompt=prompt_text,
        n=1,
        size="256x256"
        )
    return response["data"][0]["url"]

if __name__ == "__main__":
    generate_image("brown wire haired dachshund, highly realistic photograph")

