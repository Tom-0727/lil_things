import yaml
from openai import OpenAI
from pydantic import BaseModel


class CallAPIs(BaseModel):
    api_base: str
    api_key: str

    def call_api(self, text_input):
        raise NotImplementedError("Subclass must implement this method")


class OpenAIAPI(CallAPIs):
    def call_api(self, text_input, model_name: str):
        client = OpenAI(base_url=self.api_base, api_key=self.api_key)
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text_input},
        ]

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
        )
        
        return response.choices[0].message.content



if __name__ == "__main__":
    with open("my_config.yaml", "r") as f:
        config = yaml.safe_load(f)
    openai_config = config["openai"]
    api = OpenAIAPI(api_base=openai_config["api_base"], api_key=openai_config["api_key"])
    print(api.call_api("Hello, how are you?", "o3"))