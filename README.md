# Xime Index

Xime 输入法的插件、方案、模型与键盘布局市场索引。

所有条目以 `src/` 下的独立 YAML 维护，由脚本生成子索引；CI 负责校验结构、补全
`sha256`/`size`、检查下载链接可达性，并部署到 Cloudflare Pages。

## 目录结构

```
├── index.yaml                 # 市场主索引（引用各子索引）
├── src/                       # 源文件（每个条目一个 YAML，CI 只读）
│   ├── index.js               #   Worker 入口：代理索引 YAML，补充 CORS/Content-Type
│   ├── rimes/                 #   输入方案源文件
│   ├── plugins/v1/            #   旧版插件源文件归档（Lua/DEX）
│   ├── plugins/v2/            #   v2 插件源文件（JS/QuickJS，宿主 >=3.0.0）
│   ├── models/                #   模型源文件
│   └── layouts/               #   键盘布局源文件（内容托管在作者仓库，仅存引用）
├── rimes/
│   └── index.yaml             # 方案子索引（自动生成）
├── plugins/
│   ├── index.yaml             # 旧版插件子索引（源在 src/plugins/v1/）
│   └── v2/
│       └── index.yaml         # v2 插件子索引（源在 src/plugins/v2/，index_version: 2）
├── models/
│   └── index.yaml             # 模型子索引（自动生成）
├── layouts/
│   └── index.yaml             # 键盘布局子索引（自动生成）
├── scripts/
│   ├── ci-update.py           #   校验 sha256 并生成子索引
│   ├── lib.py                 #   共享工具库（下载、校验、YAML 读写）
│   ├── build_dist.py          #   组装 Cloudflare Pages 发布目录 dist/
│   └── generate_index.py      #   旧版生成器（已弃用，请用 ci-update.py）
├── .github/workflows/
│   ├── validate.yml           #   PR/push 校验结构与下载链接
│   ├── update-checksums.yml   #   自动补全 sha256/size 并回写子索引
│   └── deploy.yml             #   部署 Cloudflare Pages
├── dist/                      # Pages 发布产物（build_dist.py 生成，不入库）
├── CONTRIBUTING.md            # 上架指南
├── LAYOUT_SPEC.md             # 键盘布局上架规范
├── pyproject.toml             # Python 依赖（uv 管理）
└── wrangler.toml              # Worker 配置
```

## 支持情况

### 模型 (Models)

| ID | 名称 | 作者 | 分类 | 大小 | 最低 App 版本 |
|---|---|---|---|---|---|
| `ochwpro` | 手写模型 | Kor1 | handwriting | 7.00 MB | >=2.5.0 |
| `predictive-text-base` | 智能联想模型 base 版本 | Kor1 | prediction | 36.35 MB | >=2.6.0 |
| `predictive-text-small` | 智能联想模型 small 版本 | Kor1 | prediction | 18.8 MB | >=2.3.0 |
| `punctuation_int8` | 标点预测模型 int8 | Kor1 | punctuation | 2.2 MB | >=2.3.0 |
| `x-asr-480ms-zh-en-punct-int8` | X-ASR 中英文语音识别（带标点） | X-ASR Team | asr | 133.90 MB | >=3.0.0-beta6 |
| `zipformer-zh-int8` | 中文 Zipformer int8 | kaldi | asr | 132.63 MB | >=2.3.0 |

### 插件 (Plugins，旧版 Lua/DEX)

| ID | 名称 | 作者 | 类型 | 大小 | 最低 App 版本 |
|---|---|---|---|---|---|
| `com.kingzcheung.xime.plugin.funasr_asr` | 阿里百炼 FunAsr | Xime | speech | 10.2 KB | >=2.6.0 |
| `com.kingzcheung.xime.plugin.kaomoji` | 颜文字表情包 | Xime | emoji | 3.2 KB | >=2.6.0 |
| `com.kingzcheung.xime.plugin.meme_bunny` | 恶搞兔表情包 | Xime | emoji | 65.0 KB | >=2.6.0 |
| `com.kingzcheung.xime.plugin.typing_stats` | 输入统计 | Xime | tool | 4.0 KB | >=2.8.0 |
| `com.kingzcheung.xime.plugin.volc_asr` | 火山引擎流式语音识别 | Xime | speech | 10.6 KB | >=2.6.0 |
| `com.kingzcheung.xime.plugin.webdav_clipboard_sync` | WebDAV 剪贴板同步 | Xime | clipboard_sync | 4.5 KB | >=2.6.0 |
| `com.kingzcheung.xime.plugin.ximed_sync` | ximed 剪贴板同步 | Xime | clipboard_sync | 3.0 KB | >=2.6.0 |
| `com.kingzcheung.xime_fluent_emoji` | Fluent Emoji 3D | Xime | emoji | 5.5 MB | >=2.6.0-beta7 |

### 插件 v2 (Plugins v2，JS/QuickJS，宿主 >=3.0.0)

新版插件系统（TypeScript/QuickJS，`.xipk` 内含 `manifest.json` + 编译产物 `main.js`）使用独立索引
`plugins/v2/index.yaml`（`index_version: 2`），源文件放在 `src/plugins/v2/`；旧版插件的源文件归档在
`src/plugins/v1/`，继续发布到旧版稳定 URL `plugins/index.yaml`。索引条目在旧扁平结构上追加了新插件系统的
元数据（`icon` / `activation` / `minHostVersion` / `platforms` / `capabilities` / `network`），
旧版 App 读取 `plugins/index.yaml`，互不影响。

| ID | 名称 | 类型 | 大小 | 最低 App 版本 |
|---|---|---|---|---|
| `com.kingzcheung.xime.plugin.ai_reply` | AI 智能回复 | tool | 3.4 KB | >=3.0.0 |
| `com.kingzcheung.xime.plugin.ai_write` | AI 帮写 | tool | 2.6 KB | >=3.0.0 |
| `com.kingzcheung.xime.plugin.funasr_asr` | 阿里百炼 FunAsr | speech | 9.6 KB | >=3.0.0 |
| `com.kingzcheung.xime.plugin.kaomoji` | 颜文字表情包 | emoji | 3.0 KB | >=3.0.0 |
| `com.kingzcheung.xime.plugin.meme_bunny` | 恶搞兔表情包 | emoji | 65.0 KB | >=3.0.0 |
| `com.kingzcheung.xime.plugin.quick_phrase` | 常用语 | tool | 1.5 KB | >=3.0.0 |
| `com.kingzcheung.xime.plugin.qwen_translate` | 千问翻译 | tool | 2.6 KB | >=3.0.0 |
| `com.kingzcheung.xime.plugin.typing_stats` | 输入统计 | tool | 2.5 KB | >=3.0.0 |
| `com.kingzcheung.xime.plugin.volc_asr` | 火山引擎流式语音识别 | speech | 8.8 KB | >=3.0.0 |
| `com.kingzcheung.xime.plugin.webdav_backup` | WebDAV 云备份 | backup | 3.7 KB | >=3.1.0 |
| `com.kingzcheung.xime.plugin.webdav_clipboard_sync` | WebDAV 剪贴板同步 | clipboard_sync | 4.07 KB | >=3.0.0 |

### 输入方案 (Rimes)

| ID | 名称 | 作者 | 类型 | 标签 | 最低 App 版本 |
|---|---|---|---|---|---|
| `builtin` | 默认方案 | 王永民 | built-in | 五笔, 拼音 | >=2.6.0 |
| `cangjie` | 倉頡輸入法 | rime | remote | 倉頡 | >=2.3.0 |
| `luna_pinyin` | 朙月拼音 | rime | remote | 拼音, 反查 | >=2.3.0 |
| `quick` | 速成輸入法 | rime | remote | 速成 | >=2.3.0 |
| `rime-cantonese` | 粵語拼音方案 | CanCLID | remote | 粵語, 拼音, 反查 | >=3.2.3 |
| `rime-frost` | 白霜拼音 | gaboolic | remote | 拼音, 双拼 | >=2.3.0 |
| `rime-ice` | 雾凇拼音 | iDvel | remote | 拼音, 双拼 | >=2.3.0 |
| `rime-wanxiang` | 万象拼音标准版 | amzxyz | remote | 拼音, 双拼 | >=2.4.0 |
| `stroke` | 笔画 | rime | remote | 笔画 | >=2.5.0 |
| `wubi98` | 五笔98 | rime | remote | 五笔, 形码, 繁体 | >=2.3.0 |
| `wubixsj` | 新世纪五笔 | 空山明月（Xime 适配：aizigao） | remote | 五笔, 形码, 拼音 | >=2.8.0 |
| `xqzm` | 风入松郑码方案 | 风入松 | remote | 郑码, 拼音, 简繁 | >=2.6.0 |
| `zhengma` | 郑码方案 | chen32768 | remote | 郑码, 拼音, 简繁 | >=2.3.0 |

### 键盘布局 (Layouts)

布局是「一套 `xime.custom.yaml` 键盘配置」，本索引只保存**引用**，包与资源托管在作者自有仓库。
交付物（单文件 `xime.custom.yaml` 或含 `themes/`、`fonts/` 的 zip）**必须上传为 GitHub Release 附件**，
详见 [LAYOUT_SPEC.md](LAYOUT_SPEC.md)。

| ID | 名称 | 作者 | 标签 | 最低 App 版本 |
|---|---|---|---|---|
| `comma_period` | 逗号句号分开布局 | Kor1 | 布局, 全键盘 | >=3.0.0 |
| `flypy` | 小鹤双拼带韵母 | Kor1 | 布局, 全键盘 | >=3.0.0 |
| `msdouble` | 双拼布局（微软双拼） | Kor1 | 布局, 全键盘 | >=3.0.0 |
| `no_bubble` | 无气泡布局 | Kor1 | 布局, 全键盘 | >=3.0.0 |
| `number_rows` | 数字行 | Kor1 | 布局, 全键盘 | >=3.0.0 |
| `wubi_compact` | 五笔86紧凑布局 | Kor1 | 布局, 全键盘 | >=3.0.0 |
| `xime_26key_enhance` | 26键多功能布局 | C.C. | 资源加速, 全键盘, 全功能键盘 | >=3.0.0 |
| `xime_custom_themes` | xime 多主题 | tiengming | 配色 | >=3.0.0 |
| `xime_flypy_proxy` | 小鹤双拼多功能配置 | tiengming | 加速商店资源, 全功能键盘, 多主题 | >=3.0.0 |
| `xime_index_net` | 扩展商店资源加速 | tiengming | 资源加速, xime_index | >=2.5.0 |
| `xime_layout_romaji` | 日语罗马音键盘 | 抹露茶柒 | 布局, 全键盘, 输入法适配 | >=3.0.0 |
| `xime_theme_pack` | xime 主题包 | tiengming | 配色 | >=3.0.0 |

## 工作原理

- `src/` 下的 YAML 是唯一事实来源，CI 只读取、不回写源文件。
- `scripts/ci-update.py` 下载每个远程文件，补全 `sha256`、`size`（人类可读）和 `sizeBytes`（精确字节数），
  再生成各子索引，便于 App 展示文件大小与计算下载进度。
- `version` 为 `master`/`main` 的分支引用不参与校验（内容不固定）。
- 索引中记录的 `sha256` 是可信指纹：远端内容被替换时校验失败，该版本会被整版剔除，不进入生成的索引。
- 旧版插件（`plugins/index.yaml`）与 v2 插件（`plugins/v2/index.yaml`）分别维护，兼容不同宿主版本。

## 本地更新

依赖由 [uv](https://docs.astral.sh/uv/) 管理：

```bash
# 补全 sha256/size 并重新生成索引
uv run python scripts/ci-update.py

# 仅检查是否有缺失的 sha256/size
uv run python scripts/ci-update.py --check

# 仅校验远端文件是否被替换（不写文件）
uv run python scripts/ci-update.py --verify

# 本地预览 Pages 发布内容（生成 dist/）
uv run python scripts/build_dist.py
```

## CI 与部署

- **Validate Index**：PR 与 `main` 推送时校验子索引结构、主索引引用及所有远程下载链接可达性。
- **Auto-fill checksums**：`src/` 有变更时自动补全 `sha256`/`size`，提交更新后的子索引。
- **Deploy to Cloudflare Pages**：`main` 更新后重新生成索引、组装 `dist/` 并部署。

> **首次启用 Pages** 需在 Cloudflare 创建项目 `xime-index`：
> `npx wrangler@3.90.0 pages project create xime-index --production-branch=main`。
> 然后把对外域名（如 `index.ximei.me`）绑定到该 Pages 项目；若该域名此前绑定在 Worker 上，需先解除 Worker 的路由，避免冲突。

详见 [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)。
`src/index.js` 是 Worker 代理入口，用于给索引 YAML 补充 `Content-Type`、CORS 与缓存头。

## 上架

- 方案 / 插件 / 模型：见 [CONTRIBUTING.md](CONTRIBUTING.md)。
- 键盘布局：见 [LAYOUT_SPEC.md](LAYOUT_SPEC.md)（交付物必须为 Release 附件）。

## 许可

[CC BY-NC-SA 4.0](LICENSE) — 署名-非商业性使用-相同方式共享
