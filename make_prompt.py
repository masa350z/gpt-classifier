# %%
import os
import openai
import pandas as pd
# %%
qiita = pd.read_csv('qiita.csv')
# %%
mx_text_leng = 300
text_list = [tx[:mx_text_leng] for tx in qiita['text']]

tag_list = qiita['tags']

# %%
text_list
# %%
with open('input_text.txt', 'r', encoding='utf-8') as f:
    input_text = f.read()

prompt = '今から文章を読んでタグ付けをしてもらいます。いくつか例を上げます\n'
for i in range(len(text_list)):
    prompt += '文章{}: 文章開始###{}###文章終了\n'.format(str(i+1),
                                                text_list[i])
    prompt += '文章{}のタグ: タグ開始###{}###タグ終了\n'.format(str(i+1),
                                                   str(tag_list[i]))

prompt += 'これを踏まえて以下の文章にタグ付けしてください。返り値はPythonのリスト形式でお願いします。\n'
prompt += '文章開始###{}###文章終了\n'.format(input_text)
# %%
print(prompt)

# %%

# %%
openai.api_key = os.getenv('CHATGPT_KEY', None)
# %%
print(os.getenv('CHATGPT_KEY', None))
