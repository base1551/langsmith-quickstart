# LangSmith: LLM開発支援プラットフォーム

## 概要

LangSmith（ラングスミス）は、大規模言語モデル（LLM）を活用したアプリケーション開発全工程を支援するオールインワンのプラットフォームです。LLMを使ったアプリケーションでは、従来のソフトウェア開発とは異なり、モデル出力の非決定性やユーザー入力の多様性によって予期しない結果や品質のばらつきが生じることがあります。

これに対応するため、LangSmithは以下の機能を統合的に提供しています：

- **デバッグ・トレース管理**: 実行履歴の詳細な記録と可視化
- **評価・テスト機能**: モデルの応答品質の定量的・定性的評価
- **プロンプトエンジニアリング支援**: バージョン管理とコメント共有
- **モニタリングとアラート**: リアルタイムな監視と通知

## 環境構築

### 1. 必要なパッケージのインストール

```bash
pip install -U langsmith python-dotenv langchain-openai
```

### 2. 環境変数の設定

.envファイルを作成し、以下の環境変数を設定：

```env
LANGSMITH_API_KEY=ls_your_key_here  # https://smith.langchain.com から取得
OPENAI_API_KEY=sk_your_key_here     # https://platform.openai.com/api-keys から取得
LANGSMITH_TRACING=true
```

## プロジェクト構成

```
.
├── .env                  # 環境変数設定
├── .env.template         # 環境変数テンプレート
├── README.md            # プロジェクト説明
└── langsmith_tutorial.py # メイン実装
```

## 実装例

### 1. LangChainとの統合

最新のLangChainでは、パイプライン形式でチェーンを構築します：

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# プロンプトの定義
prompt = PromptTemplate.from_template("Hello, {name}!")

# LLMの設定
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)

# チェーンの構築
chain = prompt | llm | StrOutputParser()

# 実行
result = chain.invoke({"name": "LangSmith"})
print("LangChain Example Result:", result)
```

### 2. OpenAI APIの直接利用

トレース機能を使用してOpenAI APIを直接呼び出す例：

```python
import openai
from langsmith import traceable

@traceable
def openai_example(user_input: str):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message.content

result = openai_example("こんにちは、LangSmithとは何ですか？")
print("OpenAI Example Result:", result)
```

### 3. プロジェクト名とタグの設定

```python
import os
from langsmith import trace

# プロジェクト名の設定
os.environ["LANGCHAIN_PROJECT"] = "tutorial-project"

# タグを付けた実行
with trace("tutorial-run", tags=["tutorial", "test"]):
    # コードの実行
    pass
```

## トレースの確認

1. https://smith.langchain.com にアクセス（APIキーで認証）
2. 「Traces」タブを選択
3. プロジェクト「tutorial-project」のトレースが表示

各トレースで確認できる情報：
- 実行時間
- 入力/出力の内容
- トークン使用量とコスト
- エラー（発生した場合）

## 実行方法

```bash
python langsmith_tutorial.py
```

上記コマンドを実行すると、以下の処理が行われます：
1. 環境変数の読み込みと検証
2. LangChainを使用した例の実行
3. OpenAI APIを直接使用した例の実行
4. トレース情報のLangSmithへの送信
