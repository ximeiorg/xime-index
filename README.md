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

