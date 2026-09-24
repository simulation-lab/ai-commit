# ai-commit
AI による `git commit`



### Pathの設定
`.bashrc` や `.zshrc` に下記のとおりパスを設定します．

```bash, zsh
# Path
export PATH="$HOME/bin:$PATH"
```

### 使用方法

```bash, zsh
git ai-commit
```

### Gitエイリアスへの登録方法

作成したPythonスクリプトをGitエイリアスとして登録します．

```bash, zsh
git config --global alias.ai-commit '!python /path/to/commit.py'
```

**例：**
```bash, zsh
git config --global alias.ai-commit '!python ~/bin/git-ai-commit'
```

### Gitエイリアスの解除（削除）方法

```bash, zsh
git config --global --unset alias.エイリアス名
```

**例：**
```bash, zsh
git config --global --unset alias.ai-commit
```

