# LangSmith チュートリアル

## LangSmithとは
LangSmith（ラングスミス）は、大規模言語モデル（LLM）を活用したアプリケーション開発全工程を支援するオールインワンのプラットフォームです。以下の機能を統合的に提供します：

- **デバッグ・トレース管理**: 実行履歴の詳細な記録と可視化
- **評価・テスト機能**: モデルの応答品質の定量的・定性的評価
- **プロンプトエンジニアリング支援**: バージョン管理とコメント共有
- **モニタリングとアラート**: リアルタイムな監視と通知

## 環境構築

1. 必要なパッケージのインストール
```bash
pip install -U langsmith python-dotenv
```

2. .envファイルの作成と設定
```bash
cp .env.template .env
```

3. .envファイルに以下のAPIキーを設定
```
LANGSMITH_API_KEY=ls_your_key_here  # https://smith.langchain.com から取得
OPENAI_API_KEY=sk_your_key_here     # https://platform.openai.com/api-keys から取得
LANGSMITH_TRACING=true
```

## サンプルコードの実行

このリポジトリには以下の2つのサンプルが実装されています：

1. LangChainとの統合例
```python
prompt = PromptTemplate(input_variables=["name"], template="Hello, {name}!")
llm = OpenAI(model_name="gpt-4o", temperature=0.7)
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run({"name": "LangSmith"})
```

2. OpenAI APIの直接利用例（トレース機能付き）
```python
@traceable
def openai_example(user_input: str):
    client = wrap_openai(openai.ChatCompletion)
    response = client.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message.content
```

実行方法：
```bash
python langsmith_tutorial.py
```

## トレースの確認方法

1. https://smith.langchain.com にアクセス（APIキーで認証）
2. 「Traces」タブを選択
3. プロジェクト「tutorial-project」のトレースが表示されます

各トレースには以下の情報が含まれます：
- 実行時間
- 入力/出力の内容
- トークン使用量とコスト
- エラー（発生した場合）

## 機能カスタマイズ

### プロジェクト名の設定
```python
os.environ["LANGCHAIN_PROJECT"] = "tutorial-project"
```

### タグの追加
```python
with trace("run-name", tags=["tutorial", "test"]):
    # コードの実行
```

### フィードバックの確認
1. 特定のトレースをクリック
2. 「Feedback」タブを選択
3. システム評価やユーザーフィードバックを確認

## 詳細情報

LangSmithの詳細な機能や使用方法については、以下を参照してください：

- [LangSmith公式サイト](https://www.langchain.com/langsmith)
- [ドキュメント](https://docs.smith.langchain.com/)
- [LangSmith Hub](https://www.langchain.com/langsmith#hub)
