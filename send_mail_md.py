import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown
from dotenv import load_dotenv
import os

def send_markdown_email(to_address, subject, markdown_content):
    # 環境変数を読み込む
    load_dotenv()

    # SMTPサーバーの設定を環境変数から取得
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')

    # メールの送信者のアドレスを環境変数から取得
    from_address = os.getenv('FROM_ADDRESS')

    # CSSスタイルを外部ファイルから読み込む
    with open('./css/styles.css', 'r') as css_file:
        css_style = css_file.read()

    # マークダウンをHTMLに変換
    html_content = markdown.markdown(markdown_content)

    # CSSスタイルをHTMLに追加
    html_content_with_style = f"<html><head><style>{css_style}</style></head><body>{html_content}</body></html>"

    # MIMEマルチパートオブジェクトを作成
    msg = MIMEMultipart('alternative')
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    # HTML部分を作成し、添付
    html_part = MIMEText(html_content_with_style, 'html')
    msg.attach(html_part)

    # SMTPサーバーに接続してメールを送信
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # TLSを使用して接続を安全にする
            server.login(smtp_user, smtp_password)
            server.sendmail(from_address, to_address, msg.as_string())
        print("メールが送信されました。")
    except Exception as e:
        print(f"メールの送信中にエラーが発生しました: {e}")

# 使用例
to_address = "to_address@example.com"
subject = "MarkdownからHTMLメールへ"
markdown_content = """
# こんにちは

これは**Markdown**メールのサンプルです。

## セクション2

### セクション3

- リストアイテム1
- リストアイテム2
- リストアイテム3

[リンクテキスト](http://example.com)

> これは引用のサンプルです。
>
> 複数行にわたる引用です。
"""

send_markdown_email(to_address, subject, markdown_content)
