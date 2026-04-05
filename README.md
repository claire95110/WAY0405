# 王安宇主题页（静态站点）

根目录 `index.html` 为入口；图片等静态资源在 **`assets/`**（英文名目录，避免托管平台对中文路径解析不一致）。

## 当前默认远程仓库

`https://github.com/claire95110/WAY0405.git`

若需改正：

```bash
git remote set-url origin https://github.com/claire95110/WAY0405.git
```

## 推送到 GitHub（空仓库、未勾选 README 时）

在 **`Vibe Coding`** 目录执行：

```bash
git add .
git status
git commit -m "你的说明"   # 有改动时再执行
git push -u origin main
```

首次若远程完全是空的，一般**不需要**先 `pull`。可直接双击 **`push-to-github.bat`**（脚本会先尝试 `push`，失败再尝试合并后推送）。

## 开启 GitHub Pages

1. 仓库 **Settings** → **Pages**。
2. **Source** 选 **GitHub Actions**（与本仓库 `.github/workflows/pages.yml` 一致）。
3. 部署完成后站点约为：`https://claire95110.github.io/WAY0405/`

## Vercel 部署（务必带上 `assets`）

页面中图片路径为相对路径 **`assets/...`**，与 `index.html` 同在**仓库根目录**时，Vercel 会按静态文件原样部署。

请确认：

1. **GitHub 仓库 `Code` 页**能看到 **`assets/`** 及其中文件；本地可用 `git ls-files assets` 检查是否已被 Git 跟踪。
2. **Vercel → Project → Settings → General → Root Directory**：留空（指向包含 `index.html` 和 `assets` 的根目录）。
3. **不要**只上传单个 `index.html`；应通过 **Import Git Repository** 连接本仓库，让每次部署包含完整文件树。
4. 部署成功后自检：浏览器打开 `https://<你的域名>/assets/1.webp`，应能加载（非 404）。

若 `/assets/1.webp` 为 404，说明本次构建产物里**没有** `assets` 目录，请检查上述 1～3 步后 **Redeploy**。

## 本地预览

```bash
python -m http.server 8765
```

浏览器访问 `http://127.0.0.1:8765/index.html`。也可用 `serve-for-mobile.ps1` 生成局域网地址供手机访问。
