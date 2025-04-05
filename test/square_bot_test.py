#オープンチャットでのBOTテスト(特定メッセージ検知,メッセージ送信,特定メッセージ削除)
import sys
import os
from CHRLINE import *
from CHRLINE.hooks import HooksTracer

# 環境変数チェック
chrline_path = os.getenv("CHRLINE_PATCH_PATH")
if not chrline_path:
    sys.exit("CHRLINE_PATCH_PATH が未設定です")
sys.path.insert(0, chrline_path)

# クライアント初期化
token = ""  # 実際のトークンに置き換え
cl = CHRLINE(token, device="DESKTOPWIN", useThrift=True)

# HooksTracer設定（スクエア専用）
tracer = HooksTracer(
    cl,
    prefixes=[""],  # コマンドプレフィックスなし
)

class SquareEventHook:
    """スクエアイベント専用ハンドラー"""
    
    @tracer.Before(tracer.HooksType["SquareEvent"])
    def __before(self, op, cl):
        """イベント前処理"""
        pass

    @tracer.SquareEvent(29)
    def NOTIFICATION_MESSAGE(self, event, cl):
        try:
            # 必須情報の直接取得
            notification = event.payload.notificationMessage
            
            # 基本情報
            sender_id = notification.squareMessage.message._from
            chat_id = notification.squareChatMid
            message_id = notification.squareMessage.message.id
            text = notification.squareMessage.message.text
            content_type = notification.squareMessage.message.contentType
            
            # 追加情報
            reactions = getattr(notification.squareMessage.message, 'reactions', [])

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

            if text.strip() == "テスト": #==:メッセージがテストの場合 #in :メッセージにテストが含まれる場合
                print("テストメッセージ検知")
                # メッセージ送信
                cl.sendSquareMessage(chat_id,f"テストメッセージを検知しました",content_type)
                pass

            elif text.strip() == "削除テスト": #メッセージが削除テストの場合
                #取得したデータをそのまま返し削除
                cl.destroySquareMessage(
                    squareChatMid=chat_id,
                    messageId=message_id,
                    threadMid=None
                    )
                print("削除完了")
                pass
            else:
                pass

        except AttributeError as e:
            print(f"データ構造エラー: {str(e)}")
        except Exception as e:
            print(f"予期せぬエラー: {str(e)}")
            import traceback
            traceback.print_exc()  # 詳細トレースバック出力




class EventHook:
    """システムイベントハンドラー"""
    
    @tracer.Event
    def onReady():
        print('スクエア監視を開始しました')

    @tracer.Event
    def onInitializePushConn():
        print('PUSH接続を初期化しました')

# スクエア専用サービスで起動
tracer.run(
    2,  # PUSH接続モード
    initServices=[3],  # 3=スクエアのみ 1=DM 2=グループ
    #initServices=[3, 5],  # 5=プッシュ通知が必要な場合
)


"""
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