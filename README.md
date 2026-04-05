# 王安宇主题页（静态站点）

根目录 `index.html` 为入口；素材在 `照片素材/`。

## 推送到 GitHub

1. 在 [GitHub](https://github.com/new) 新建仓库（可勾选不添加 README，避免首次推送冲突）。
2. 在本文件夹打开终端（需已安装 [Git](https://git-scm.com/download/win)），执行：

```bash
git init
git add .
git commit -m "Initial commit: static fan page"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

将 `<你的用户名>`、`<仓库名>` 换成你的实际信息。若使用 SSH，把 `origin` 换成 `git@github.com:用户名/仓库名.git`。

## 开启 GitHub Pages（手机/外网访问）

1. 仓库 **Settings** → **Pages**。
2. **Build and deployment** 里 **Source** 选 **GitHub Actions**（不要选 Deploy from a branch，本仓库用工作流部署）。
3. 推送 `main` 后，在 **Actions** 里等待 **Deploy to GitHub Pages** 跑绿。
4. 站点地址一般为：`https://<用户名>.github.io/<仓库名>/`（若仓库名为 `用户名.github.io` 则可能是根域名）。

## 本地预览

在项目目录执行 `python -m http.server 8765`，浏览器打开 `http://127.0.0.1:8765/index.html`。也可用 `serve-for-mobile.ps1` 生成局域网链接给手机访问。
