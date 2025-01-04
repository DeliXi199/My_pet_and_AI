import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse, urlencode
import ssl
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time

import websocket  # 使用 websocket-client

answer = ""  # 用于存储结果


# 以下密钥信息从控制台中获取
appid = "a6ce1da9"  # 填写控制台中获取的 APPID 信息
api_secret = "NTlhMjMzM2ExOTI5MmRhZTc3Njk3NGZl"  # 填写控制台中获取的 APISecret 信息
api_key = "4e046fe5728dc6fdba7f80d11ac4f075"  # 填写控制台中获取的 APIKey 信息

# 用于配置大模型版本，默认“general/generalv2”
# domain = "general"  # v1.5版本
domain = "4.0Ultra"  # v2.0版本

# 云端环境的服务地址
# Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
Spark_url = "wss://spark-api.xf-yun.com/v4.0/chat"  # v2.0环境的地址

text = []
