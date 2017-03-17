#!/usr/bin/env python
# -*- coding:utf-8 -*-

# mecabで分析する機能

import sys
import MeCab
import json
import random


# 受け取った文章をMecabで解析する
def mecab_perse(text=None):
  m = MeCab.Tagger ("-Ochasen")
  if text != None:
    #print(m.parse (text))
    return m.parse (text)
  else:
    #print(m.parse ("すもももももももものうち"))
    return m.parse ("すもももももももものうち")



# 会話のリストからランダムに指定した品詞を取り出す
# ex) get_hinshi(cl, "動詞-自立", ["する", "なさる", "なる", "ある"])
# ex) get_hinshi(cl, "名詞-一般")
# ex) get_hinshi(cl, "名詞-固有名詞-地域-一般")
def get_hinshi(text=None, hinshi=None, nglist=[]):
  ## 受け取ったテキストをmecab_perse関数を使って解析
  persed_text = mecab_perse(text)
  #print(persed_text)

  ## 解析した結果をリスト形式にする
  text_list_temp = persed_text.split("\n")
  text_list = []
  for l in text_list_temp:
    text_list.append(l.split("\t"))
  #print(text_list)

  ## 指定した品詞を取り出す
  results_list = []
  for l in text_list:
    if len(l) > 1: #EOSとか空行を省く
      if l[3] == hinshi:
        check_flag = 0
        for nl in nglist: #nglistのワードを省く
          if str(l[2]) == str(nl):
            check_flag += 1
        if check_flag == 0:
          results_list.append(l[2])
  #print(results_list)
  return results_list



## 実行
#if __name__ == "__main__":
#  gh = get_hinshi("東京とか渋谷とか", "名詞-固有名詞-地域-一般")
#  print(gh)
#  if len(gh) > 0:
#    word  = str(random.choice(gh))
#    print(type(word))
