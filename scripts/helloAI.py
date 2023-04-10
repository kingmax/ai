import os
import openai

# https://github.com/openai/openai-python

openai.api_key = os.getenv('OPENAI_API_KEY')  # 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
# print(openai.api_key)

# list models
models = openai.Model.list()

# print the first model's id
print(models.data[0].id)

# create a completion
completion = openai.Completion.create(model="ada", prompt="Hello world")

# print the completion
print(completion.choices[0].text)


# Chat
completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world!"}])
print(completion.choices[0].message.content)

# Embeddings
# choose text to embed
text_string = "sample text"

# choose an embedding
model_id = "text-similarity-davinci-001"

# compute the embedding of the text
embedding = openai.Embedding.create(input=text_string, model=model_id)['data'][0]['embedding']
print(embedding)  # missing `numpy`
