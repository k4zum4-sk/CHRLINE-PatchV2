#指定した友達のuidからプロフィールを取得するテストコード

import sys
import os

# 環境変数からパスを取得
chrline_path = os.getenv("CHRLINE_PATCH_PATH")

if chrline_path:
    sys.path.insert(0, chrline_path)
else:
    print("環境変数 CHRLINE_PATCH_PATH が設定されていません\nREADME.mdを確認してください")
#パスを取得してからimprot
from CHRLINE import *
from CHRLINE.hooks import HooksTracer

# トークンを環境変数から読み込む
#token = os.getenv("LINE_AUTH_TOKEN", "")
if not token:
    raise ValueError("環境変数 'LINE_AUTH_TOKEN' が設定されていません。")

target_Id = input("ターゲットのmidを入力: ")#例:get_friendsmid_test.pyなどで取得したuidを入力

cl = CHRLINE(token, device="DESKTOPWIN")#ログイン処理
print("ログイン成功")

target = cl.getContact(target_Id)#ターゲットの情報を取得
print(target)
"""
target[1] = uid
target[2] = createId アカウント作成時期
target[22] = displayName  アカウント名......
"""
