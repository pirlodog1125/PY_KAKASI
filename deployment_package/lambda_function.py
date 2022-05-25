import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'site-packages'))
import json
from pprint import pprint
from pykakasi import kakasi as pykakasi

def lambda_handler(event, context):
  pprint(event)

  method = event.get('requestContext', {}).get('http', {}).get('method')
  path = event.get('requestContext', {}).get('http', {}).get('path')
  result = {}

  # オブジェクトをインスタンス化
  kakasi = pykakasi()
  # モードの設定：J(Kanji) to H(Hiragana)
  kakasi.setMode('J', 'H')

  # 変換して出力
  conv = kakasi.getConverter()

  if method == 'POST':
    body = event.get('body', '')
    json_body = None
    try:
      # stringから、dictに変換
      json_body = json.loads(body)
    except Exception as e:
      json_body = {}

    if path == '/':

      input_list = json_body.get('inputs', [])
      result_list = []

      if input_list:
        for i in input_list:
          text = i

          _result = conv.do(text)
          #pprint(result)

          result_list.append(_result)

      result['result'] = result_list

  return {
    'statusCode': 200,
    'body': json.dumps(result, ensure_ascii=False),
    "headers": {
      "Content-Type": "application/json;charset=UTF-8",
    },
  }

def _lambda_handler(event, context):
  pprint(event)

  input_list = event.get('inputs', [])
  result_list = []

  # オブジェクトをインスタンス化
  kakasi = pykakasi()
  # モードの設定：J(Kanji) to H(Hiragana)
  kakasi.setMode('J', 'H')

  # 変換して出力
  conv = kakasi.getConverter()

  if input_list:
    for i in input_list:
      text = i

      result = conv.do(text)
      #pprint(result)

      result_list.append(result.encode('utf-8'))

  return result_list