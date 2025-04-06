#個人メッセージの受信を監視し受信したメッセージ(バイナリデータ)を復号化するBOtのテストコード
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

# トークンを設定（手動入力 or 環境変数から取得）
token = "LINE_AUTH_TOKEN"  #login_getToken_test.pyで取得したトークンを入力 

# トークンをファイルや環境変数から読み込む方法も良い
#token = os.getenv("LINE_AUTH_TOKEN", "")

cl = CHRLINE(token, device="DESKTOPWIN")
print("ログイン成功")
profile = cl.getProfile() #自分のプロフィールを取得
def on_message(op, cl):
    msg = op[20]  # op[20] = メッセージのmetadata
    #print(f"データ：{op}\n{msg}")  #op,msgを確認したい場合コメントを外す
    if not msg:
        if str(op[3]) == "40":  # op[3] ,40 = 自分の既読イベント
                print("自分の既読")
        elif str(op[3]) == "55": # op[3] ,55 = 相手の既読イベント
            user = cl.getContact(msg[1])
            display_name = user[22] #user[22] = アカウント名
            print(f"{display_name} がメッセージを既読")
        elif str(op[3]) == "48": #op[3] ,48 = ログインイベント
                print(f"ログインを検知")
        else:
            print(f"受信や送信以外が検知されました{op}")
        return

    if msg[1] == profile[1]: # msg[1] = メッセージ送信者 , profile[1] = 自分のmid
        print("自分の送信メッセージです")
    else:
        if str(op[3]) == "26": #op[3] =  26  #メッセージ受信イベント
            msg_type = msg[15]  # msg[15] = メッセージタイプ
            decrypted_text = None
            try:
                decrypted_text = cl.decryptE2EETextMessage(msg, isSelf=False) #受信メッセージ(バイナリデータ)を復元
                print("復号化されたテキスト:", decrypted_text)
            except Exception as e:
                print("復号化エラー:", e)

            if msg_type == 0: #msg_type 0  = テキストメッセージ
                if "テストメッセージ" in decrypted_text:
                    print("特定メッセージの検知完了")
                else:
                    pass
            else:
                print("テキスト以外")
            return

def run():
    print("メッセージ監視を開始します...")
    cl.trace(on_message)

if __name__ == "__main__":
    run()
        
            
                    
        
