#オープンチャットでのBOTテスト(特定メッセージ検知,メッセージ送信,特定メッセージ削除)
import sys
import os
chrline_path = os.getenv("CHRLINE_PATCH_PATH")
sys.path.insert(0, chrline_path)
from CHRLINE import *
from CHRLINE.hooks import HooksTracer
from CHRLINE.helpers.square import SquareHelper

# クライアント初期化

# トークンを環境変数から読み込む
token = os.getenv("LINE_AUTH_TOKEN", "")
if not token:
    raise ValueError("環境変数 'LINE_AUTH_TOKEN' が設定されていません。")
cl = CHRLINE(token, device="DESKTOPWIN", useThrift=True)
#device：接続デバイスの種類（DESKTOPWIN=Windowsデスクトップ版を模倣）
#useThrift：LINEの旧プロトコルを使用するオプション

# HooksTracer設定（スクエア専用）
tracer = HooksTracer(
    cl,
    prefixes=[""],  # コマンドプレフィックスなし prefixes：コマンドの接頭辞（空文字=すべてのメッセージを処理）
)
class SquareEventHook:
    """スクエアイベント専用ハンドラー"""
    def __init__(self, cl): #自分の情報取得
        self.cl = cl
        self.square_helper = SquareHelper() #square_helper：スクエア機能専用ヘルパークラス

    @tracer.Before(tracer.HooksType["SquareEvent"])
    def __before(self, op, cl): #op：受信した操作オブジェクト cl：クライアントインスタンス
        """イベント前処理"""
        pass

    @tracer.SquareEvent(29) #29：スクエアメッセージ通知のイベントタイプ
    def NOTIFICATION_MESSAGE(self, event, cl): #eventにデータが格納
        try:
            # 必須情報の直接取得
            notification = event.payload.notificationMessage #通知メッセージの生データ
            
            # 基本情報
            sender_id = notification.squareMessage.message._from #送信者のユーザーMID
            chat_id = notification.squareChatMid #スクエアチャットのMID
            message_id = notification.squareMessage.message.id
            text = notification.squareMessage.message.text
            content_type = notification.squareMessage.message.contentType

            MySquare_Mid = cl.getMySquareMidByChatMid(chat_id)#getMySquareMidByChatMid：チャットから自身のMIDを取得
            # 追加情報
            reactions = getattr(notification.squareMessage.message, 'reactions', [])

            #CHRLINE 前バージョンのライブラリ向けデータ取得
            # notification_payload = event.val_4
            # notification_data = notification_payload.val_30
            # square_message = notification_data.val_2
            # message = square_message.val_1
            # chat_id = notification_data.val_1           # チャットMID            
            # sender_id = message.val_1                   # 送信者MID            
            # message_id = message.val_4                  # メッセージID            
            # text = getattr(message, 'val_10', '')       # メッセージテキスト (存在しない場合があるのでgetattrを使用)            
            # content_type = getattr(message, 'val_15', -1) # コンテンツタイプ (存在しない場合があるのでgetattrを使用)            
            # MySquare_Mid = cl.getMySquareMidByChatMid(chat_id) # 自身のMIDを取得
            # 追加情報（リアクションはアクセス方法が不明なため一旦保留）            
            # reactions = getattr(message, 'reactions_field_id?', [])

            # ログ出力
            print(f"""
            [メッセージログ]
            送信者: {sender_id}
            チャット: {chat_id}
            メッセージID: {message_id}
            内容: {text}
            タイプ: {['テキスト', '画像', '動画', '音声'][content_type] if content_type in [0,1,2,3] else 'その他'}
            リアクション数: {len(reactions)}
            """)
            if sender_id == MySquare_Mid: #送信者が自分の場合
                print("自分のイベントなのでスルー")
                pass
            else:
                if text.strip() == "テスト": #==:メッセージがテストの場合 #in :メッセージにテストが含まれる場合
                    print("テストメッセージ検知")
                    # メッセージ送信
                    cl.sendSquareMessage(chat_id,f"テストメッセージを検知しました",content_type) #sendSquareMessage：スクエアチャットへのメッセージ送信
                    pass

                elif text.strip() == "音声テスト":
                    cl.sendAudio(to=chat_id, path="example_audio.m4a", oType="audio")
                elif text.strip() == "削除テスト": #メッセージが削除テストの場合
                    #取得したデータをそのまま返し削除
                    cl.destroySquareMessage(
                        squareChatMid=chat_id,
                        messageId=message_id,
                        threadMid=None
                        ) #destroySquareMessage：メッセージの強制削除機能
                    print("削除完了")
                    pass

        except AttributeError as e:
            print(f"データ構造エラー: {str(e)}")
        except Exception as e:
            print(f"予期せぬエラー: {str(e)}")
            import traceback
            traceback.print_exc()  # 詳細トレースバック出力


square_hook = SquareEventHook(cl)

class EventHook:
    """システムイベントハンドラー"""
    
    @tracer.Event
    def onReady(): #onReady：BOT起動完了時に発火
        print('スクエア監視を開始しました')

    @tracer.Event
    def onInitializePushConn(): #onInitializePushConn：PUSH接続確立時に発火
        print('PUSH接続を初期化しました')

# スクエア専用サービスで起動
tracer.run(
    2,  # PUSH接続モード
    initServices=[3],  # 3=スクエアのみ 1=DM 2=グループ
    #initServices=[3, 5],  # 5=プッシュ通知が必要な場合
)



"""

起動 → HooksTracer初期化 → イベントフック登録
↓
PUSH接続確立 → onInitializePushConn発火
↓
監視開始 → onReady発火
↓
メッセージ受信 → NOTIFICATION_MESSAGE処理


スクエアデータ構造
{
    "3": 29,
    "4": {
        "1": {
            "2": {
                "1": {
                    "1": "送信者MID",
                    "2": "スクエアチャットMID",
                    "4": "メッセージID",
                    "10": "メッセージテキスト",
                    "15": 0,
                    "18": "{\"MENTIONEES\":[...]}",
                    "21": "返信メッセージID"
                },
                "3": "送信者表示名"
            },
            "6": "スクエアMID"
        }
    },
    "5": "同期トークン"
}
"""
