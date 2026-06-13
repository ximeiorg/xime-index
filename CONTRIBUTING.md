# 贡献指南

通过 PR 添加或更新文件即可上架方案或插件。

## 目录结构

```
rimes/                    # 输入方案
├── index.yaml            # 方案子索引（由 scripts/generate_index.py 自动生成，请勿手动编辑）
├── wubi86.yaml           # 每个方案一个独立文件
└── ...

plugins/                  # 插件
├── index.yaml            # 插件子索引（由 scripts/generate_index.py 自动生成，请勿手动编辑）
├── xime.kaomoji.yaml     # 每个插件一个独立文件
└── ...
```

## 上架新方案

### 步骤 1：创建方案文件

在 `rimes/` 下新建 `<id>.yaml` 文件：

```yaml
# rimes/my_schema.yaml
id: "my_schema"                  # 方案 ID，与 schema_id 一致
name: "我的方案"                  # 显示名称
author: "你的名字"                # 作者
description: "方案说明"           # 简短描述
type: "remote"
tags: ["五笔"]                    # 搜索标签
homepage: "https://..."          # 项目主页（可选）
license: "GPL-3.0"               # 许可证（可选）
dependencies: []                  # 依赖的其他方案 ID
appVersion: ">=2.2.0"            # 兼容的 App 版本
warning: ""                       # 安装前警告（可选）
currentVersion: "1.0.0"          # 当前版本
versions:                         # 版本历史
  - version: "1.0.0"
    date: "2026-06-01"           # 发布日期
    changelog: "初始发布"          # 更新说明
    downloadUrl:                  # 下载地址
      - url: "https://..."       # 单个文件时只写一条
        sha256: ""               # SHA256 校验值（可选）
        size: "1.5 MB"           # 文件大小（可选）
```

### 步骤 2：生成索引

```bash
python scripts/generate_index.py
```

`rimes/index.yaml` 会自动更新，包含新方案的完整信息。

## 上架新插件

### 步骤 1：创建插件文件

在 `plugins/` 下新建 `<id>.yaml` 文件：

```yaml
# plugins/my-plugin.yaml
id: "xime.my-plugin"             # 插件唯一 ID
name: "我的插件"                  # 显示名称
author: "你的名字"                # 作者
description: "插件说明"           # 简短描述
type: "remote"
tags: ["表情"]                    # 搜索标签
pluginType: "emoji"              # 插件类型
homepage: "https://..."          # 项目主页（可选）
license: "MIT"                   # 许可证（可选）
appVersion: ">=2.3.0"            # 兼容的 App 版本
currentVersion: "1.0.0"
versions:
  - version: "1.0.0"
    date: "2026-06-01"
    changelog: "初始发布"
    downloadUrl:                  # 下载地址
      - url: "https://..."       # 单个文件时只写一条
        sha256: ""               # SHA256 校验值（可选）
        size: ""                 # 文件大小（可选）
```

### 步骤 2：生成索引

```bash
python scripts/generate_index.py
```

`plugins/index.yaml` 会自动更新。

## 更新版本

已有方案/插件发布新版本时：

1. 在对应 `.yaml` 文件的 `versions` 列表顶部新增一条版本记录
2. 更新 `currentVersion` 为最新版本号
3. 运行 `python scripts/generate_index.py` 同步索引

## 打包要求

| 类型 | 格式 | 要求 |
|------|------|------|
| 方案 | .zip / .tar.gz | 包含 .schema.yaml + .dict.yaml |
| 插件 | .apk | 实现 EmojiPlugin 接口 |

## 下载地址

`downloadUrl` 统一使用对象列表格式，每个文件独立携带 `sha256` 和 `size`。

**单个文件：**
```yaml
downloadUrl:
  - url: "https://example.com/releases/v1.0.0/file.zip"
    sha256: "abc123..."            # 可选
    size: "10 MB"                  # 可选
```

**多个文件全部必装：**
```yaml
downloadUrl:
  - url: "https://example.com/releases/v1.0.0/schema.zip"
    sha256: "abc123..."
    size: "10 MB"
  - url: "https://example.com/releases/v1.0.0/model.gram"
    sha256: "def456..."
    size: "50 MB"
```

**多个文件让用户二选一（带 `name` 标签）：**
```yaml
downloadUrl:
  - name: "基础版"
    url: "https://example.com/releases/v1.0.0/base.zip"
    sha256: "abc123..."
    size: "10 MB"
  - name: "完整版"
    url: "https://example.com/releases/v1.0.0/full.zip"
    sha256: "def456..."
    size: "50 MB"
```



## 注意事项

- 下载地址推荐使用 GitHub Releases，确保长期有效
- 方案若依赖其他方案，在 `dependencies` 中声明，安装时会自动处理
- 子索引由脚本自动生成，不要手动编辑 `rimes/index.yaml` 或 `plugins/index.yaml`
- 每个版本独立填写 `downloadUrl`，建议指向具体 Release Tag 而非 `latest`
