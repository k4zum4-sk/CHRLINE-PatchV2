import sys
import os

# 環境変数からCHRLINEパスを取得
chrline_path = os.getenv("CHRLINE_PATCH_PATH")
sys.path.insert(0, chrline_path)  # モジュール検索パスに追加

# 必要なライブラリをインポート
from CHRLINE import CHRLINE
from CHRLINE.hooks import HooksTracer

# トークンを環境変数から読み込む
token = os.getenv("LINE_AUTH_TOKEN", "")
if not token:
    raise ValueError("環境変数 'LINE_AUTH_TOKEN' が設定されていません。")

# LINEクライアントの初期化
cl = CHRLINE(
    token, 
    device="DESKTOPWIN",  # デバイスタイプ（Windowsクライアントを模倣）
    useThrift=True        # Thriftプロトコルを使用
)
tracer = HooksTracer(cl)  # イベントトレーサーの初期化

def send_image(cl, to_user, image_path):
    try:
        # 画像を送信
        cl.sendImage(to_user, image_path)
        print("画像送信完了")
    except Exception as e:
        print(f"画像送信エラー: {e}")
def send_video(cl, to_user, video_path):
    try:
        # 動画を送信
        cl.sendVideo(to_user, video_path)
        print("動画送信完了")
    except Exception as e:
        print(f"動画送信エラー: {e}")
def send_audio(cl,to_user,audio_path):
    try:
        cl.sendAudio(to_user,audio_path)
        print("音声送信完了")
    except Exception as e:
        print(f"音声送信エラー: {e}")

def bot(op, cl):
    """
    メッセージイベントハンドラ
    op: Operationオブジェクト（LINEの操作情報を含む）
    cl: LINEクライアントインスタンス
    """
    # メッセージ操作か確認
    if hasattr(op, 'message'):
        msg = op.message
        
        # グループチャット判定（toType=2がグループ）
        if msg.toType == 2:
            print("[グループメッセージ検知]")
            print(f"送信者: {msg._from}")
            print(f"宛先グループID: {msg.to}")
            print(f"メッセージタイプ: {msg.contentType}")
            
            # テキストメッセージ処理
            if msg.contentType == 0:  # 0=テキスト
                print(f"テキスト内容: {msg.text}")
                
                # 特定のキーワードに反応
                if msg.text.strip() == "テスト":
                    cl.sendMessage(msg.to, "テストメッセージを検知しました！")
                    print("テスト応答メッセージ")

                elif msg.text.strip() == "画像テスト":
                    send_image(cl,msg.to,"test/example.heic")
            
            # スタンプメッセージ処理
            elif msg.contentType == 7:  # 7=スタンプ
                cl.sendMessage(msg.to, "スタンプが送信されました！")
                print("スタンプ受信を検知")
            
            # その他のメッセージタイプ
            else:
                print(f"未対応のメッセージタイプ: {msg.contentType}")

# イベントハンドラをトレーサーに登録
cl.trace(bot)
print("LINEボットが起動しました...")

# メインループの実行
try:
    tracer.run()  # イベントループを開始
except KeyboardInterrupt:
    print("ボットを安全に停止します...")



