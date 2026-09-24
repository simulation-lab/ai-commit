# ai-commit
AIによる `git commit`

`commit` には，2つの方法があります．
ひとつはホームディレクトリ直下に `bin` ディレクトリを作成し，パスを通す方法です．
2つ目は，Gitエイリアスに登録する方法です．



### Pathの設定
`.bashrc` や `.zshrc` に下記のとおりパスを設定します．

```bash
# Path
export PATH="$HOME/bin:$PATH"
```

### 使用方法

```bash
git ai-commit
```

### Gitエイリアスへの登録方法

作成したPythonスクリプトをGitエイリアスとして登録します．

```bash
git config --global alias.ai-commit '!python /path/to/commit.py'
```

**例：**
```bash
git config --global alias.ai-commit '!python ~/bin/git-ai-commit'
```

### Gitエイリアスの解除（削除）方法

```bash
git config --global --unset alias.エイリアス名
```

**例：**
```bash
git config --global --unset alias.ai-commit
```

