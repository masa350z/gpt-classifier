# %%
from openai import OpenAI
import pandas as pd
import os


class GPT:
    def __init__(self):
        # OpenAI APIキーを環境変数から取得し、クライアントを初期化
        # os.environ.get("CHATGPT_KEY") を　"XXXXXXXX"の形でAPIキーベタ打ちしても使える
        self.client = OpenAI(api_key=os.environ.get("CHATGPT_KEY"))

    def make_completion(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )

        # 応答メッセージの取得
        response_message = response.choices[0].message.content

        return response_message


def make_prompt(text_list, tag_list, input_text):
    # プロンプトの基本形式を定義
    prompt = '今から文章を読んでタグ付けをしてもらいます。いくつか例を上げます\n'

    # 既存のテキストとタグの例をプロンプトに追加
    for i in range(len(text_list)):
        prompt += '文章{}: 文章開始###{}###文章終了\n'.format(str(i+1),
                                                    text_list[i])
        prompt += '文章{}のタグ: タグ開始###{}###タグ終了\n'.format(str(i+1),
                                                       str(tag_list[i]))

    # 新しいテキストに対するタグ付けを要求
    prompt += 'これを踏まえて以下の文章にタグ付けしてください。返り値はPythonのリスト形式でお願いします。\n'
    prompt += '文章開始###{}###文章終了\n'.format(input_text)

    return prompt


# 最大テキスト長の設定(長すぎるとエラーになるので)
mx_text_leng = 300

# Qiitaデータセットの読み込み
qiita = pd.read_csv('qiita.csv')
text_list = [tx[:mx_text_leng] for tx in qiita['text']]
tag_list = qiita['tags']

# 入力テキストの読み込み（この文章にタグ付けさせる）
with open('input_text.txt', 'r', encoding='utf-8') as f:
    input_text = f.read()

# input_text = XXXXXXXXXX でベタ打ちしても良い

# 文章長すぎるのでtext_list[:10]で10個に切ってる
prompt = make_prompt(text_list[:10], tag_list, input_text)

# プロンプトの表示
print(prompt)


# GPTインスタンスの生成とタグ付け後メッセージの取得
gpt = GPT()
response_message = gpt.make_completion(prompt)

print(response_message)
