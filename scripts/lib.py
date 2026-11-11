"""
共享工具库 — 供各构建子脚本调用。
"""

import glob
import hashlib
import os
import tempfile
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_VERSIONS = {"master", "main"}
USER_AGENT = "Xime-Index-Checksum/1.0"


def human_size(bytes_val: int) -> str:
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.1f} KB"
    elif bytes_val < 1024 * 1024 * 1024:
        return f"{bytes_val / (1024 * 1024):.1f} MB"
    else:
        return f"{bytes_val / (1024 * 1024 * 1024):.2f} GB"


def download_checksum(url: str):
    """下载文件，返回 (sha256_hex, size_bytes, size_human)。"""
    tmp_path = None
    try:
        fd, tmp_path = tempfile.mkstemp()
        os.close(fd)
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=300) as resp:
            sha256 = hashlib.sha256()
            size_bytes = 0
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                sha256.update(chunk)
                size_bytes += len(chunk)
        return sha256.hexdigest(), size_bytes, human_size(size_bytes)
    except Exception as exc:
        print(f"    ⚠ 下载失败: {exc}")
        return None, None, None
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


def head_size(url: str):
    """HEAD 探测远端文件体积（不下载内容），返回 (size_bytes, size_human)；失败返回 (None, None)。

    用于体积必须保持准确、但又不适合整文件下载的场景：如 .gram 语法模型（几百 MB，
    且 URL 指向滚动 tag，sha256 无法固定）或只需补 sizeBytes 的已校验条目。
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
        with urllib.request.urlopen(req, timeout=60) as resp:
            ctype = (resp.headers.get("Content-Type") or "").lower()
            if "text/html" in ctype:
                return None, None  # 被重定向到登录/错误页，长度不可信
            length = resp.headers.get("Content-Length")
            if not length or not length.isdigit() or int(length) <= 0:
                return None, None
            size_bytes = int(length)
            return size_bytes, human_size(size_bytes)
    except Exception as exc:
        print(f"    ⚠ 体积探测失败: {exc}")
        return None, None


def should_skip_version(version: str) -> bool:
    return version.strip().strip('"').strip("'") in SKIP_VERSIONS


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def dump_yaml(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def fill_download_urls(data: dict) -> dict:
    """
    补全 data 中 downloadUrl 列表内缺失的 sha256/size/sizeBytes。
    跳过 version 为 master/main 的版本。
    返回新的 dict（深拷贝），不修改入参。

    体积（sizeBytes）是 App 下载进度的分母，必须贴近真实文件：
      - .gram 语法模型：上游用滚动 tag，文件几百 MB 故不生成 sha256，但每次都用 HEAD
        刷新体积——否则会长期停留在旧值（万象 .gram 曾记录 117 MiB、实际 399 MiB，
        App 进度会算到 298%）。
      - 已有 sha256/size 但缺 sizeBytes 的条目：同样用 HEAD 补齐，不再重复下载。
    """
    import copy
    result = copy.deepcopy(data)

    for v in result.get("versions", []):
        ver = v.get("version", "?")
        if should_skip_version(ver):
            continue

        for dl in v.get("downloadUrl", []):
            url = dl.get("url", "")
            if not url:
                continue
            if url.endswith(".gram"):
                size_bytes, size_h = head_size(url)
                if size_bytes:
                    if dl.get("sizeBytes") != size_bytes:
                        print(f"  📏 {url}: {dl.get('sizeBytes')} → {size_bytes} ({size_h})")
                    dl["sizeBytes"] = size_bytes
                    dl["size"] = size_h
                else:
                    print(f"  ⏭ {url} (.gram 文件，跳过 sha256，体积探测失败保留原值)")
                continue
            if dl.get("sha256") and dl.get("size") and dl.get("sizeBytes"):
                continue
            if dl.get("sha256") and dl.get("size"):
                size_bytes, size_h = head_size(url)
                if size_bytes:
                    print(f"  📏 {url}: sizeBytes → {size_bytes} ({size_h})")
                    dl["sizeBytes"] = size_bytes
                    dl["size"] = size_h
                continue
            print(f"  ↓ {url}")
            sha256, size_bytes, size_h = download_checksum(url)
            if sha256:
                dl["sha256"] = sha256
                dl["size"] = size_h
                dl["sizeBytes"] = size_bytes
                print(f"    ✓ sha256={sha256[:16]}...  size={size_h}  bytes={size_bytes}")

    return result


def fill_archive(data: dict) -> dict:
    """
    补全 data 中 archive 块缺失的 sha256/size/sizeBytes。
    跳过 version 为 master/main 的版本。
    """
    import copy
    result = copy.deepcopy(data)

    for v in result.get("versions", []):
        ver = v.get("version", "?")
        if should_skip_version(ver):
            continue

        if "archive" in v:
            a = v["archive"]
            url = a.get("url", "")
            if url and (not a.get("sha256") or not a.get("size")):
                print(f"  ↓ {url}")
                sha256, size_bytes, size_h = download_checksum(url)
                if sha256:
                    a["sha256"] = sha256
                    a["size"] = size_h
                    a["sizeBytes"] = size_bytes
                    print(f"    ✓ sha256={sha256[:16]}...  size={size_h}  bytes={size_bytes}")

    return result


def fill_files_checksums(data: dict) -> dict:
    """
    补全 data 中 files 列表内缺失的 sha256/size/sizeBytes。
    跳过 version 为 master/main 的版本。
    """
    import copy
    result = copy.deepcopy(data)

    for v in result.get("versions", []):
        ver = v.get("version", "?")
        if should_skip_version(ver):
            continue

        for f_item in v.get("files", []):
            url = f_item.get("url", "")
            if not url or (f_item.get("sha256") and f_item.get("size")):
                continue
            print(f"  ↓ {url}")
            sha256, size_bytes, size_h = download_checksum(url)
            if sha256:
                f_item["sha256"] = sha256
                f_item["size"] = size_h
                f_item["sizeBytes"] = size_bytes
                print(f"    ✓ sha256={sha256[:16]}...  size={size_h}  bytes={size_bytes}")

    return result


# ─── 按记录值校验远端文件（检测内容被替换/篡改）──────────────


def collect_remote_items(data: dict):
    """收集 data 中所有带 url 的下载项。

    返回 [(version_index, version, kind, item)]：
      - kind: "downloadUrl[i]" / "archive" / "files[i]"
      - version_index 为 versions 列表中的原始下标，便于整版剔除
    跳过 version 为 master/main 的版本。
    """
    items = []
    for vi, v in enumerate(data.get("versions", []) or []):
        ver = v.get("version", "?")
        if should_skip_version(ver):
            continue
        for i, dl in enumerate(v.get("downloadUrl", []) or []):
            if dl.get("url"):
                items.append((vi, ver, f"downloadUrl[{i}]", dl))
        archive = v.get("archive") or {}
        if archive.get("url"):
            items.append((vi, ver, "archive", archive))
        for i, f_item in enumerate(v.get("files", []) or []):
            if f_item.get("url"):
                items.append((vi, ver, f"files[{i}]", f_item))
    return items


def check_checksums(data: dict) -> dict:
    """下载远端文件，与索引中记录的 sha256 逐一比对（不修改任何数据）。

    只校验记录了 sha256 的下载项；未记录 sha256 的无法校验，单独列出。
    返回 dict：
      checked      已校验（有 sha256）的项数
      mismatch     [(vi, version, kind, url, expected, actual, size_h)] sha256 不一致
      error        [(vi, version, kind, url, reason)] 下载失败，无法校验
      unverifiable [(vi, version, kind, url)] 未记录 sha256，无法校验
      size_warn    [(vi, version, kind, url, expected_bytes, actual_bytes)] sizeBytes 记录不一致
      bad_versions {vi: [原因]} sha256 不一致的版本（应下架）
    """
    result = {
        "checked": 0,
        "mismatch": [],
        "error": [],
        "unverifiable": [],
        "size_warn": [],
        "bad_versions": {},
    }

    for vi, ver, kind, item in collect_remote_items(data):
        url = item["url"]
        expected = (item.get("sha256") or "").strip()
        if not expected:
            result["unverifiable"].append((vi, ver, kind, url))
            continue

        actual, nbytes, size_h = download_checksum(url)
        if actual is None:
            result["error"].append((vi, ver, kind, url, "下载失败"))
            continue

        result["checked"] += 1
        if actual.lower() != expected.lower():
            result["mismatch"].append((vi, ver, kind, url, expected, actual, size_h))
            result["bad_versions"].setdefault(vi, []).append(f"{kind}: sha256 不一致")
            continue

        recorded_bytes = item.get("sizeBytes")
        if recorded_bytes and int(recorded_bytes) != nbytes:
            result["size_warn"].append((vi, ver, kind, url, recorded_bytes, nbytes))

    return result


def apply_size_bytes(data: dict, url: str, size_bytes: int) -> bool:
    """按实际文件大小修正 data 中 URL 匹配的下载项（sizeBytes + size 文本）。

    供更新流程把 sha256 校验时算出的真实体积写回输出索引，避免手工填写的
    sizeBytes 长期偏离实际（偏差会让 App 的下载进度超过 100%）。
    """
    changed = False
    for _, _, _, item in collect_remote_items(data):
        if item.get("url") == url and item.get("sizeBytes") != size_bytes:
            item["sizeBytes"] = size_bytes
            item["size"] = human_size(size_bytes)
            changed = True
    return changed


def prune_bad_versions(data: dict, label: str = ""):
    """剔除 sha256 不匹配的版本，避免被替换的内容进入索引。

    返回 (new_data, report)；report 为 check_checksums 的结果。
    currentVersion 若指向被剔除的版本，则回退到剩余最新的版本。
    """
    report = check_checksums(data)
    if not report["bad_versions"]:
        return data, report

    versions = data.get("versions", []) or []
    kept = [v for i, v in enumerate(versions) if i not in report["bad_versions"]]
    prefix = f"{label} " if label else ""
    for i in sorted(report["bad_versions"]):
        print(f"  🚫 {prefix}v{versions[i].get('version')}: sha256 不匹配，已剔除")
        for reason in report["bad_versions"][i]:
            print(f"       └ {reason}")

    new_data = dict(data)
    new_data["versions"] = kept
    kept_versions = [v.get("version") for v in kept]
    if new_data.get("currentVersion") not in kept_versions:
        if kept:
            print(f"     ↳ currentVersion 回退到 {kept[0].get('version')}")
            new_data["currentVersion"] = kept[0].get("version")
    return new_data, report


def recalc_model_size(data: dict) -> dict:
    """
    重新计算模型级 size = 所有版本中所有文件 sizeBytes 的总和。
    仅在 sizeBytes 齐全时生效。
    """
    import copy
    result = copy.deepcopy(data)

    total_bytes = 0
    has_all = True
    for v in result.get("versions", []):
        for f in v.get("files", []):
            sb = f.get("sizeBytes")
            if sb is None:
                has_all = False
            else:
                total_bytes += sb

    if has_all and total_bytes > 0:
        old = result.get("size")
        new = human_size(total_bytes)
        result["size"] = new
        if old != new:
            print(f"    📐 模型大小: {old} → {new}")

    return result
