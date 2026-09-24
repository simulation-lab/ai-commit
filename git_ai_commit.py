#!/usr/bin/env python
# ==============================================================================
# タイトル: Git AI Commit (Gemini API コミットメッセージ自動生成ツール)
# 概要   : git diff --staged の変更点を解析し、Gemini APIを用いてコミットメッセージを自動作成・適用するスクリプト
# 主な機能:
#   - ステージングされたコード差分（git diff --staged）の取得
#   - Gemini API (google-genai) の System Instruction (スキル定義) を用いたメッセージ生成
#   - ターミナル上でのメッセージ確認とユーザー承認（Enterキーでコミット実行、Ctrl+Cでキャンセル）
# ==============================================================================

import os
import subprocess
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

# .env ファイルから環境変数を読み込む（dotenvを使用する場合）
load_dotenv()

# AIモデルの役割・スキル（System Instruction）を定義
SYSTEM_INSTRUCTION = """
[1行目] 変更の概要を50文字以内で記述（要約）
[2行目] （空行）
[3行目以降] 箇条書きで簡潔に，1行あたり50文字以内で記述

記述の心得：
- System Instructionでは文章は「である調」を使用します
- 句読点は，読点を「，」，句点を「．」とします
- 箇条書きは，文章の最後に句点「．」をつけません
"""

def main():
    # 1. APIキーの確認
    api_key = os.environ.get("GEMINI_AI_COMMIT_KEY")
    if not api_key:
        print("エラー: GEMINI_AI_COMMIT_KEY 環境変数が設定されていません．")
        sys.exit(1)

    # 2. git diff --staged の実行
    try:
        diff_output = subprocess.check_output(
            ["git", "diff", "--staged"], text=True
        )
    except subprocess.CalledProcessError:
        print("エラー: Gitコマンドの実行に失敗しました．")
        sys.exit(1)

    if not diff_output.strip():
        print("ステージングされた変更（git add）がありません．")
        sys.exit(1)

    # 3. Gemini APIの呼び出し (System Instruction によりスキルを事前定義)
    try:
        client = genai.Client(api_key=api_key)
        
        # モデルのスキル（system_instruction）を config で設定
        chat = client.chats.create(
            model="gemini-3.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )
        
        # 指示文を含めた prompt 変数は作らず、純粋な diff_output だけを送信
        response = chat.send_message(diff_output)
        commit_msg = response.text.strip() if response.text else ""
    except Exception as e:
        print(f"Gemini API呼び出しエラー: {e}")
        sys.exit(1)

    if not commit_msg:
        print("メッセージの生成に失敗しました．")
        sys.exit(1)

    # 4. 生成されたメッセージの確認とコミット実行
    
    print("```")
    print(f"{commit_msg}")
    print("```")
    
    try:
        # ユーザーの入力を待機（Enterキーで次へ進む）
        input("Do you want to commit with this message? > ")  #2026.09.23
    except KeyboardInterrupt:
        # Ctrl+C が押された場合はコミットせずに終了
        print("\n\nThe commit has been cancelled.")
        sys.exit(0)

    # Enterが押された場合のみ、git commit を実行
    subprocess.run(["git", "commit", "-m", commit_msg])
    print("The commit is complete!")


if __name__ == "__main__":
    main()

