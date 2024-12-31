# markdown-to-html-email
MarkdownをHTMLに変換し、SMTP経由でメール送信するPythonスクリプトです。カスタムCSSスタイルの追加も可能で、環境変数で機密情報を管理します。

## MarkdownをHTMLメールに変換して送信

このPythonスクリプトは、Markdown形式で書かれた内容をHTMLに変換してメールを送信する機能を提供します。HTMLコンテンツにカスタムCSSスタイルを追加することもサポートしています。

## 特徴

- SMTPサーバーの資格情報を使用してメールを送信。
- MarkdownコンテンツをHTMLに変換。
- HTMLコンテンツにカスタムCSSスタイルを追加。
- 環境変数を使用して機密情報を管理。

## 必要条件

- Python 3.x
- `smtplib` (Pythonに標準で含まれています)
- `email` (Pythonに標準で含まれています)
- `markdown` (`pip install markdown`でインストール)
- `python-dotenv` (`pip install python-dotenv`でインストール)

## セットアップ

1. このリポジトリをクローンします：
    ```bash
    git clone https://github.com/Cosmos-81/send_to_mail_by_markdown.git
    cd send_to_mail_by_markdown
    ```

2. プロジェクトディレクトリに `.env` ファイルを作成し、SMTPサーバーの設定とメールアドレスを追加します：
    ```env
    SMTP_SERVER=smtp.example.com
    SMTP_PORT=587
    SMTP_USER=your_username
    SMTP_PASSWORD=your_password
    FROM_ADDRESS=your_email@example.com
    ```

3. プロジェクトディレクトリに `styles.css` ファイルを作成し、カスタムCSSスタイルを追加します：
    ```css
    body {
        font-family: Arial, sans-serif;
    }
    h1 {
        color: #333;
    }
    p {
        font-size: 14px;
    }
    ```
    
    ※`./css/styles.css`にサンプルファイルがあります。必要に応じて変更してください。

    ```css
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        color: #333;
    }
    h1, h2, h3 {
        color: #fff;
        padding: 10px;
    }
    h1 {
        background-color: #4CAF50;
    }
    h2 {
        background-color: #2196F3;
    }
    h3 {
        background-color: #FF9800;
    }
    p {
        margin-bottom: 10px;
    }
    ul {
        margin: 0;
        padding: 0;
        list-style-type: none;
    }
    ul li {
        background: #f4f4f4;
        margin: 5px 0;
        padding: 10px;
        border-radius: 5px;
    }
    a {
        color: #1E90FF;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    blockquote {
        margin: 20px 0;
        padding: 10px 20px;
        background: #f9f9f9;
        border-left: 10px solid #ccc;
    }

4. 必要なPythonパッケージをインストールします：
    ```bash
    pip install markdown python-dotenv
    ```

## 使用方法

`send_markdown_email` 関数を使用してメールを送信します。受信者のメールアドレス、メールの件名、およびMarkdown形式のコンテンツを引数として渡す必要があります。

```python
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
