# やすこの冒険 v8.3.30 — GitHub Pages 更新
既存の `deploy.yml` が `python3 scripts/assemble.py` で `dist/index.html` を生成し、dist を Pages に公開する場合は変更不要です。同梱の `.github/workflows/deploy.yml` は新規リポジトリ（main ブランチ）用の例です。既存リポジトリの実ファイルは未確認です。

1. 念のため既存リポジトリをバックアップ。Pages の URL・リポジトリ名は維持してください。
2. `parts/` 内の旧版 `index.html.part*` と `index.html.sha256` を、新版の11分割ファイル（各最大16MiB）とSHA-256ファイルで置き換えます。旧版の余分な分割が残らないようにしてください。
3. `scripts/assemble.py` は従来版と同一。既存にあれば置き換え不要です。既存ワークフローを優先してください。
4. すべての分割ファイルとハッシュを同一コミットに含めるのが推奨です。GitHub ブラウザで複数コミットになる場合、一時的に検証失敗しても全ファイルが揃った後に再実行します。
5. Settings > Pages > Source = GitHub Actions。Actions で Assemble / SHA 検証 / Deploy が成功したことを確認し、公開URLを再読み込みして v8.3.30 を確認します。

ローカルでの検証（このZIPを展開したルートで）: `python3 scripts/assemble.py`。生成先は `dist/index.html`。ハッシュ不一致なら停止します。実際のGitHubへのアップロードとデプロイは行っていません。
