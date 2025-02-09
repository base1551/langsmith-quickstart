import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import openai
from langsmith import traceable, trace

# .envファイルから環境変数を読み込む
load_dotenv()

# LangSmithプロジェクト名を設定
os.environ["LANGCHAIN_PROJECT"] = "tutorial-project"

# 必要な環境変数の確認
required_env_vars = {
    "LANGSMITH_API_KEY": "LangSmith APIキー",
    "OPENAI_API_KEY": "OpenAI APIキー",
}

missing_vars = [var for var, name in required_env_vars.items() if not os.getenv(var)]
if missing_vars:
    print("以下の環境変数が設定されていません:")
    for var in missing_vars:
        print(f"- {var} ({required_env_vars[var]})")
    print("\n.envファイルを作成し、必要なAPIキーを設定してください。")
    print("参考: .env.templateファイル")
    exit(1)

# LangChainとの統合サンプル
def langchain_example():
    prompt = PromptTemplate.from_template("Hello, {name}!")
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({"name": "LangSmith"})
    print("LangChain Example Result:", result)

# OpenAIクライアントを直接使用するサンプル
@traceable
def openai_example(user_input: str):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message.content

def main():
    print("LangSmith Tutorial")
    print("-----------------")
    print("プロジェクト名:", os.getenv("LANGCHAIN_PROJECT"))

    # APIキーが設定されているか確認
    if "LANGSMITH_API_KEY" not in os.environ:
        print("Warning: LANGSMITH_API_KEY is not set")
        return

    try:
        with trace("tutorial-run", tags=["tutorial", "test"]):
            # LangChainサンプルの実行
            print("\nRunning LangChain example...")
            langchain_example()

            # OpenAIサンプルの実行
            print("\nRunning OpenAI example...")
            result = openai_example("こんにちは、LangSmithとは何ですか？")
            print("OpenAI Example Result:", result)

    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
