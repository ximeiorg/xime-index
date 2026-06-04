# Xime Index

Xime 输入法的插件与方案市场索引。

## 目录结构

```
├── index.yaml        # 市场索引文件
├── rimes/            # 自研方案包（.zip / .tar.gz）
├── plugins/          # 自研插件 APK
├── CONTRIBUTING.md   # 上架指南
└── .github/
    └── workflows/    # CI 校验
```

## 工作原理

```
App ──HTTP──→ index.yaml ──→ 展示列表 ──→ 用户选择安装
                                        │
                                        ├── 方案：下载 → 解压 → 部署
                                        └── 插件：下载 → 安装 APK
```

## 上架

见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可

MIT
