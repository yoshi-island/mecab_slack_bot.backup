#!/usr/bin/env python
# -*- coding:utf-8 -*-

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

import mecab_analyze
import random
import sys
import re
import mecab_dict_setting

# 別ディレクトリ呼び込む
sys.path.insert(0, './python-o365')
import test_o365_cal
o365_cal = test_o365_cal


@default_reply()
def default_func(message):

    # 後で使う変数
    ## 受け取ったメッセージ
    text = message.body['text']

    ## o365 ##
    # 何も引数なければ、本日と月累計を出力する
    # start,end,start_month,category_all,category_all_month
    if text == "outlook":
      msg = o365_cal.execution()
      start = msg[0]
      end = msg[1]
      start_month = msg[2]
      category_all = msg[3]
      category_all_month = msg[4]
      msg = 'start: ' + start + '    end: ' + end + '\n' + category_all
      msg = str(msg)
      message.reply(msg)
      msg = 'start: ' + start_month + '    end: ' + end + '\n' + category_all_month
      msg = str(msg)
      message.reply(msg)


    ## 和布蕪でメッセージ解析した結果をリストとして格納
    place_list = mecab_analyze.get_hinshi(text, "名詞-固有名詞-地域-一般")
    noun_list = mecab_analyze.get_hinshi(text, "名詞-一般")
    last_name_list = mecab_analyze.get_hinshi(text, "名詞-固有名詞-人名-姓")
    first_name_list = mecab_analyze.get_hinshi(text, "名詞-固有名詞-人名-名")
    ## 人名修飾ワード(あとに「す」が続く感じで)
    people_adj_list = ["すてきで", "やさしいで", "いけてま"]
    ## 人名登録トリガー
    pattern = "さん知ってる？"

    # この先使う変数の初期化
    word = ""
    word2 = ""


    # 人名に反応する
    if len(last_name_list) > 0:
      word  = str(random.choice(last_name_list))
      word2  = str(random.choice(people_adj_list))
      msg = "%sさん、%sすよね！" % (word, word2)
      message.reply(msg)

    elif len(first_name_list) > 0:
      word  = str(random.choice(first_name_list))
      word2  = str(random.choice(people_adj_list))
      msg = "%sさん、%sすよね！" % (word, word2)
      message.reply(msg)
    
    ## 「〇〇さん知ってる？」と聞かれた時に知らない人名を辞書登録する
    elif pattern.encode('utf-8') in text.encode('utf-8'):
      new_name = text[:-7].lstrip() # 念のため冒頭のスペースも削除
      new_last_name_list = mecab_analyze.get_hinshi(new_name, "名詞-固有名詞-人名-姓")
      new_first_name_list = mecab_analyze.get_hinshi(new_name, "名詞-固有名詞-人名-名")
      ### 知っている場合
      #### ここまでに人名拾っているので、この判定は不要かも。でも誤って登録しないように。
      if len(new_last_name_list) > 0 or len(new_first_name_list) > 0:
        msg = "%sさんですよね、もちろん知ってます。" % new_name
        message.reply(msg)
      ### 知らない場合
      else:
        msg = "%sさん、記憶します。少々お待ちを、、" % new_name
        message.reply(msg)
        try:
          mecab_dict_setting.mecab_add_dict(new_name)
          msg = "%sさん、記憶しました。" % new_name
          message.reply(msg)
        except:
          msg = "%sさん、記憶に失敗しました。" % new_name
          message.reply(msg)




    # 地名と名詞に反応する
    elif len(place_list) > 0 and len(noun_list) == 0:
      word  = str(random.choice(place_list))
      msg = "%sにいきたいですね！" % word
      message.reply(msg)

    elif len(noun_list) > 0 and len(place_list) == 0:
      word  = str(random.choice(noun_list))
      msg = "%s、私好きです！" % word
      message.reply(msg)

    elif len(noun_list) > 0 and len(place_list) > 0:
      word  = str(random.choice(noun_list))
      word2  = str(random.choice(place_list))
      msg = "%sと%sってお洒落ですね！" % (word, word2)
      message.reply(msg)



@listen_to(r'.+')
def people_func(message):
    ## 受け取ったメッセージ
    text = message.body['text']

    ## この辺繰り返しを修正する #fixme
    ## 和布蕪でメッセージ解析した結果をリストとして格納
    place_list = mecab_analyze.get_hinshi(text, "名詞-固有名詞-地域-一般")
    noun_list = mecab_analyze.get_hinshi(text, "名詞-一般")
    last_name_list = mecab_analyze.get_hinshi(text, "名詞-固有名詞-人名-姓")
    first_name_list = mecab_analyze.get_hinshi(text, "名詞-固有名詞-人名-名")
    ## 人名修飾ワード(あとに「す」が続く感じで)
    people_adj_list = ["すてきで", "やさしいで", "いけてま"]

    # この先使う変数の初期化
    word = ""
    word2 = ""

    # 人名に反応する
    if len(last_name_list) > 0:
      word  = str(random.choice(last_name_list))
      word2  = str(random.choice(people_adj_list))
      msg = "%sさん、%sすよね！" % (word, word2)
      message.reply(msg)

    elif len(first_name_list) > 0:
      word  = str(random.choice(first_name_list))
      word2  = str(random.choice(people_adj_list))
      msg = "%sさん、%sすよね！" % (word, word2)
      message.reply(msg)

    # 地名に反応する
    elif len(place_list) > 0 and len(noun_list) == 0:
      word  = str(random.choice(place_list))
      msg = "%sいいところですよね！" % word
      message.reply(msg)



### o365 ###
@respond_to(r'^outlook\s+\d\d\d\d\d\d\d\d\s+\d\d\d\d\d\d\d\d\s*$')
def o365_func(message):
    text = str(message.body['text'])
    text = re.split('\s+', text)
    msg = o365_cal.execution(text[1],text[2])
    start = msg[0]
    end = msg[1]
    start_month = msg[2]
    category_all = msg[3]
    category_all_month = msg[4]
    msg = 'start: ' + start + '    end: ' + end + '\n' + category_all
    msg = str(msg)
    message.reply(msg)
    msg = 'start: ' + start_month + '    end: ' + end + '\n' + category_all_month
    msg = str(msg)
    message.reply(msg)
