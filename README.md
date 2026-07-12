# Xime Index

Xime 输入法的插件与方案市场索引。

## 目录结构

```
├── index.yaml                 # 市场主索引（引用子索引）
├── rimes/                     # 输入方案源文件
│   ├── index.yaml             #   方案子索引（自动生成）
│   ├── rime-ice.yaml          #   各方案独立配置
│   └── ...
├── plugins/                   # 插件源文件
│   ├── index.yaml             #   插件子索引（自动生成）
│   ├── xime.kaomoji.yaml
│   └── ...
├── models/                    # 模型源文件
│   ├── index.yaml             #   模型子索引（自动生成）
│   └── ...
├── scripts/
│   ├── ci-update.py           #   CI 自动补全 sha256/size
│   ├── lib.py                 #   共享工具库
│   └── generate_index.py      #   旧版生成器（保留）
├── CONTRIBUTING.md            # 上架指南
└── .github/workflows/         # CI 校验
```

## 支持情况

### 模型 (Models)

| ID | 名称 | 分类 | 大小 | 最低 App 版本 |
|---|---|---|---|---|
| `ochwpro` | 手写模型 | handwriting | 6.7 MB | >=2.5.0 |
| `predictive-text-small` | 智能联想模型 | prediction | 18.9 MB | >=2.3.0 |
| `punctuation_int8` | 标点预测模型 int8 | punctuation | 2.3 MB | >=2.3.0 |
| `zipformer-zh-int8` | 中文 Zipformer int8 | asr | 126.5 MB | >=2.3.0 |

### 插件 (Plugins)

| ID | 名称 | 作者 | 类型 | 大小 | 最低 App 版本 |
|---|---|---|---|---|---|
| `xime.kaomoji` | 颜文字 | Xime | emoji | 2.08 MB | >=2.0.0 |
| `xime.meme-bunny` | 表情兔 | Xime | emoji | 12.7 MB | >=2.0.0 |

### 输入方案 (Rimes)

| ID | 名称 | 作者 | 类型 | 标签 | 最低 App 版本 |
|---|---|---|---|---|---|
| `cangjie` | 倉頡輸入法 | rime | remote | 倉頡 | >=2.3.0 |
| `luna_pinyin` | 朙月拼音 | rime | remote | 拼音, 反查 | >=2.3.0 |
| `quick` | 速成輸入法 | rime | remote | 速成 | >=2.3.0 |
| `rime-ice` | 雾凇拼音 | iDvel | remote | 拼音, 双拼 | >=2.3.0 |
| `rime-wanxiang` | 万象拼音标准版 | amzxyz | remote | 拼音, 双拼 | >=2.4.0 |
| `stroke` | 笔画 | rime | remote | 笔画 | >=2.5.0 |
| `wubi86` | 五笔86 | rime | built-in | 五笔, 拼音 | >=2.3.0 |
| `wubi98` | 五笔98 | rime | remote | 五笔, 形码, 繁体 | >=2.3.0 |
| `zhengma` | 郑码方案 | chen32768 | remote | 郑码, 拼音, 简繁 | >=2.3.0 |

## 工作原理

CI 自动为每个下载链接补全 `sha256`、`size`（人类可读）和 `sizeBytes`（精确字节数），
方便 App 展示文件大小和计算下载进度。`version` 为 `master`/`main` 的分支引用会被跳过（内容不固定）。

## 本地更新

```bash
# 补全 sha256/size 并重新生成索引
python scripts/ci-update.py

# 仅检查是否有缺失
python scripts/ci-update.py --check
```

推送到 `main` 分支时 CI 会自动构建并部署，无需手动操作。

详见 [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)。

## 上架

见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可

[CC BY-NC-SA 4.0](LICENSE) — 署名-非商业性使用-相同方式共享

