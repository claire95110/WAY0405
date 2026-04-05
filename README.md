# 王安宇主题页（静态站点）

根目录 `index.html` 为入口；图片等静态资源在 `assets/`（原 `照片素材` 已改为英文名，避免 GitHub Pages 中文路径加载失败）。

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

将 `<你的用户名>`、`<仓库名>` 换成你的实际信息（须与 GitHub 上仓库名**完全一致**）。若使用 SSH，把 `origin` 换成 `git@github.com:用户名/仓库名.git`。

当前项目默认远程：`https://github.com/claire95110/WAY_Wanganyu.git`。若曾配错，可执行：`git remote set-url origin https://github.com/claire95110/WAY_Wanganyu.git`

## 开启 GitHub Pages（手机/外网访问）

1. 仓库 **Settings** → **Pages**。
2. **Build and deployment** 里 **Source** 选 **GitHub Actions**（不要选 Deploy from a branch，本仓库用工作流部署）。
3. 推送 `main` 后，在 **Actions** 里等待 **Deploy to GitHub Pages** 跑绿。
4. 站点地址一般为：`https://claire95110.github.io/WAY_Wanganyu/`（或 `https://<用户名>.github.io/<仓库名>/`；若仓库名为 `用户名.github.io` 则可能是根域名）。

## Vercel 部署后图片不显示

已核对：若打开 `https://<你的域名>/assets/1.webp` 返回 **404**，说明线上**没有部署 `assets` 目录**（页面里的 `index.html` 在，但图片未上传）。

请逐项检查：

1. **GitHub 网页**：仓库 **Code** 里是否能看到 **`assets/`** 文件夹及其中图片。若没有，在本机执行 `git add assets`、`git commit`、`git push`，再在 Vercel **Deployments** 里 **Redeploy**。
2. **Vercel 项目设置**：**Settings → General → Root Directory** 须为**空**（或指向包含 `index.html` 与 `assets/` 的仓库根目录），不要指到子文件夹导致漏掉 `assets`。
3. **不要用「只拖了单个 html」**：若用 CLI 或面板只上传了 `index.html`，必须把整个项目（含 **`assets/`**）一并部署。

本地可执行 `git ls-files assets` 确认 `assets` 已被 Git 跟踪后再推送。

## 本地预览

在项目目录执行 `python -m http.server 8765`，浏览器打开 `http://127.0.0.1:8765/index.html`。也可用 `serve-for-mobile.ps1` 生成局域网链接给手机访问。
