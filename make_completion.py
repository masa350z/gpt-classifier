# %%
from openai import OpenAI
import pandas as pd
import os


class GPT:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("CHATGPT_KEY"))

    def make_completion(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )

        response_message = response.choices[0].message.content

        return response_message


def make_prompt(text_list, tag_list, input_text):

    prompt = '今から文章を読んでタグ付けをしてもらいます。いくつか例を上げます\n'
    for i in range(len(text_list)):
        prompt += '文章{}: 文章開始###{}###文章終了\n'.format(str(i+1),
                                                    text_list[i])
        prompt += '文章{}のタグ: タグ開始###{}###タグ終了\n'.format(str(i+1),
                                                       str(tag_list[i]))

    prompt += 'これを踏まえて以下の文章にタグ付けしてください。返り値はPythonのリスト形式でお願いします。\n'
    prompt += '文章開始###{}###文章終了\n'.format(input_text)

    return prompt


# %%
mx_text_leng = 300

qiita = pd.read_csv('qiita.csv')
text_list = [tx[:mx_text_leng] for tx in qiita['text']]

tag_list = qiita['tags']

with open('input_text.txt', 'r', encoding='utf-8') as f:
    input_text = f.read()
prompt = make_prompt(text_list[:10], tag_list, input_text)

print(prompt)

# %%
gpt = GPT()
response_message = gpt.make_completion(prompt)

print(response_message)

# %%
