# 连接个人 GitHub 仓库与首版上传

目标仓库：https://github.com/Lincoln-625/yunzhi-monitor

本项目已有 Git 历史，不需要重新初始化。本次保留原作者提交，个人改造从文档首版开始。

## 1. 创建空仓库与登录

在 GitHub 中选择个人账号，创建 `yunzhi-monitor`。如果尚未创建，不要勾选自动生成 README、.gitignore 或 LICENSE，避免产生与本地无关的初始提交。仓库可见性由本人选择，公开前核对原项目授权及敏感信息。

使用 Git for Windows 的凭据管理器时，推送可能打开浏览器登录。HTTPS 命令行要求密码时应使用 Personal Access Token，不是 GitHub 账号密码；也可以配置 SSH。不要把 Token 放入仓库 URL、代码或聊天消息。

## 2. 检查并提交文档

在项目根目录运行：

```powershell
git status
git remote -v
git branch --show-current
git log -1 --oneline
```

当前沿用 `master` 分支。若助手已完成下面的提交，不需要重复执行：

```powershell
git add README.md docs/GITHUB_SETUP.md
git diff --cached --stat
git commit -m "docs: define Yunzhi campus recruitment monitoring baseline"
```

## 3. 连接个人仓库并保留原项目

仅在 `origin` 仍为鱼皮仓库且不存在 `upstream` 时执行；已配置过则跳过，不要重复覆盖：

```powershell
git remote rename origin upstream
git remote add origin https://github.com/Lincoln-625/yunzhi-monitor.git
git remote -v
```

预期：`origin` 指向 Lincoln-625/yunzhi-monitor，`upstream` 指向 liyupi/yupi-hot-monitor。后续不向 `upstream` 推送个人改动。

## 4. 首次推送

先检查当前文件和即将推送的历史中是否有真实密钥、配置及数据库；`.gitignore` 不会移除已经进入历史的文件。

```powershell
git ls-remote origin
```

只有命令成功且没有分支、标签输出时，才按空仓库处理；认证和网络失败不代表仓库为空。若已有内容，先检查和决定如何合并，不使用强制推送。

```powershell
git push -u origin master
```

如实际分支不是 `master`，需相应替换。完成后刷新 GitHub，确认首版 README 和提交记录已显示。本地提交成功和 GitHub 推送成功是两个不同步骤。

## 5. ECS 拉取

```powershell
git clone https://github.com/Lincoln-625/yunzhi-monitor.git
cd yunzhi-monitor
```

私有仓库需要在 ECS 上单独授权，建议仅授予部署所需读取权限。之后按 README 配置环境、安装依赖并初始化数据库。

后续更新代码、构建、处理数据迁移和重启服务是单独部署步骤，不能只执行 `git pull` 就认为已经上线。

## 官方参考

- [将本地代码添加到 GitHub](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)
- [管理远程仓库](https://docs.github.com/en/get-started/git-basics/managing-remote-repositories)
- [GitHub 身份验证](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github)
