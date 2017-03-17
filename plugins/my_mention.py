#!/usr/bin/env python
# -*- coding:utf-8 -*-

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

import mecab_analyze
import random
import sys



@default_reply()
def default_func(message):
    text = message.body['text']

    place_list = mecab_analyze.get_hinshi(text, "名詞-固有名詞-地域-一般")
    noun_list = mecab_analyze.get_hinshi(text, "名詞-一般")

    word = ""
    word2 = ""
    if len(place_list) > 0 and len(noun_list) == 0:
      word  = str(random.choice(place_list))
      msg = word + "にいきたいですね！"
      message.reply(msg)

    elif len(noun_list) > 0 and len(place_list) == 0:
      word  = str(random.choice(noun_list))
      msg = word + "、私好きです！"
      message.reply(msg)

    elif len(noun_list) > 0 and len(place_list) > 0:
      word  = str(random.choice(noun_list))
      word2  = str(random.choice(place_list))
      msg = word + "と" + word2 + "ってお洒落ですね！"
      message.reply(msg)

    elif word == "":
      msg = "はぁ、、"
      message.reply(msg)

