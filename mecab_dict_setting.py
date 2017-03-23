#!/usr/bin/env python
# -*- coding:utf-8 -*-

# mecabで分析する機能

import sys
import MeCab
import password_list
import os


# ホームディレクトリ定義
home = password_list.home

# ユーザー辞書（人名）に追記する
## 新規作成は未対応
def mecab_add_dict(text=None):
  ## テキストの読み方を取得
  yomi = mecab_perse_yomi(text)
  ## 作業用辞書のパス定義 
  #### 人それぞれ違うところ。でも都度変更は面倒なのでここで定義。
  dict_work_path = home + "/python_work/mecab_work/dic_work/people.csv"
  ## ユーザー辞書のパス定義
  dict_path = "/usr/local/lib/mecab/dic/userdic"

  ## リスト追記処理
  new_word_line = "%s,,,1,名詞,固有名詞,人名,名,*,*,%s,%s,%s,people_dic\n" % (text,text,yomi,yomi)
  f = open(dict_work_path,'a')
  f.write(new_word_line)
  f.close()

  ## フォーマット処理
  #### ここばかりはシェルのコマンドを打ってしまう。
  #### ここでコケたら辞書にゴミが残ってしまうので要改修。
  command_line = "/usr/local/Cellar/mecab/0.996/libexec/mecab/mecab-dict-index -d /usr/local/lib/mecab/dic/ipadic -u %s -f utf-8 -t utf-8 %s" % (dict_path, dict_work_path)
  check = os.system(command_line)

  return check




# よみを返す
def mecab_perse_yomi(text=None):
  m = MeCab.Tagger ("-Oyomi")
  if text != None:
    yomi = m.parse (text).rstrip() # 改行コードも削除
    return yomi



# 実行
if __name__ == "__main__":
  mecab_add_dict("ニコラス")
