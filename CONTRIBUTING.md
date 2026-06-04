# 贡献指南

通过 PR 修改 `index.yaml` 即可上架方案或插件。

## 方案条目

```yaml
- id: "my_schema"                  # 方案 ID，与 schema_id 一致
  name: "我的方案"                  # 显示名称
  version: "1.0.0"                 # 版本号
  author: "你的名字"                # 作者
  description: "方案说明"           # 简短描述
  type: "remote"                   # built-in 或 remote
  tags: ["五笔"]                    # 搜索标签
  downloadUrl: "https://..."       # 下载地址（仅 remote 类型）
  homepage: "https://..."          # 项目主页（可选）
  license: "GPL-3.0"               # 许可证（可选）
  dependencies: []                  # 依赖的其他方案 ID
  appVersion: ">=2.2.0"            # 兼容的 App 版本
  warning: ""                       # 安装前警告（可选）
```

## 插件条目

```yaml
- id: "xime.my-plugin"             # 插件唯一 ID
  name: "我的插件"                  # 显示名称
  version: "1.0.0"                 # 版本号
  author: "你的名字"                # 作者
  description: "插件说明"           # 简短描述
  type: "remote"                   # built-in 或 remote
  tags: ["表情"]                    # 搜索标签
  pluginType: "emoji"              # 插件类型
  downloadUrl: "https://..."       # APK 下载地址
  appVersion: ">=2.3.0"            # 兼容的 App 版本
```

## 打包要求

| 类型 | 格式 | 要求 |
|------|------|------|
| 方案 | .zip / .tar.gz | 包含 .schema.yaml + .dict.yaml |
| 插件 | .apk | 实现 EmojiPlugin 接口 |

## 注意事项

- 下载地址推荐使用 GitHub Releases，确保长期有效
- 方案若依赖其他方案，在 `dependencies` 中声明，安装时会自动处理
