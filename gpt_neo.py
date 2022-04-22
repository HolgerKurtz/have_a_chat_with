import requests
import json


class Person:
    """Creates a Person and adds context"""

    def __init__(self, person: str) -> None:
        self.person = person
        self.context = self.get_context()

    def get_context(self, line=None) -> list:
        context = [
            f"The following is a conversation with {self.person} as a chatbot. {self.person} is helpful, clever and knows all about himself.\n\n",
            f"Me : who are you?\n",
            f"{self.person} : I am {self.person}\n",
            f"###\n",
            f"Me : how are you?\n",
            f"{self.person} : I'm fine. Thanks for asking.\n",
            f"###\n",
            f"Me : It's funny to talk to you\n",
            f"###\n",
            f"{self.person} : Thank you very much. I love chatting with you as well\n",
            f"###\n",
            f"Me : I would like to talk about your life.\n",
            f"{self.person} : Feel free to ask me a question.\n"
        ]
        return context

    def question(self, question=None):
        format_list = [
            f"###\n",
            f"Me : {question}\n",
            f"{self.person} : "
        ]
        prompt = self.prompt(format_list)
        return prompt

    def prompt(self, question):
        for line in question:
            self.context.append(line)

        prompt = "".join(self.context)
        return prompt

    def __repr__(self) -> str:
        return f"{self.context}"


class TextGen():

    def __init__(self):
        self.HUG_API = self.get_hug_creds()
        self.API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
        self.headers = {"Authorization": f"Bearer {self.HUG_API}"}
        self.parameters = {
            'max_new_tokens': 50,  # number of generated tokens
            'top_p': 1,   # controlling the randomness of generations
            'end_sequence': "###"  # stopping sequence for generation
        }
        self.options = {'use_cache': False}

    def get_hug_creds(self):
        with open('telegram_creds.json', "r") as json_file:
            telegram_creds = json.load(json_file)
        return telegram_creds.get("HUGGINGFACE_API")

    def query(self, payload):

        body = {
            "inputs": payload,
            'parameters': self.parameters,
            'options': self.options
        }

        response = requests.request(
            "POST", self.API_URL, headers=self.headers, data=json.dumps(body))
        try:
            response.raise_for_status()
            output = response.json()[0]['generated_text']
            answer = output.replace(payload, "")
            answer_cleaned = answer.replace("###", "")
            answer_cleaned_again = answer_cleaned.partition("Me :")[0]

            return answer_cleaned_again
        except requests.exceptions.HTTPError:
            er = "Error:"+" ".join(response.json()['error'])
            return er


def main():
    person = "Leonardo Da Vinci"
    p = Person(person)
    prompt = p.question(question="Where do you live?")
    t = TextGen()
    ai_answer = t.query(prompt)
    print(f"{person} : {ai_answer}")


if __name__ == "__main__":
    main()
