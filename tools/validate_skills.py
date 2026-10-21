#!/usr/bin/env python3
"""ScholarlyOps skill and documentation structure validator.

Uses the Python standard library only. Frontmatter checks are limited
string/line parsing — not a full YAML parser.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
REL_PATH_IN_SKILL_RE = re.compile(
    r"(?:`|/|\()\s*((?:references|scripts|examples|tests)/[A-Za-z0-9_./\-]+\.[A-Za-z0-9]+)"
)
ABS_PATH_RE = re.compile(
    r"(?:[A-Za-z]:\\|/Users/|/home/)[^\s`\"']+"
)


@dataclass
class Finding:
    """单条验证发现。"""

    level: str
    code: str
    message: str
    path: str = ""


@dataclass
class Report:
    """验证报告。"""

    findings: list[Finding] = field(default_factory=list)

    def add(self, level: str, code: str, message: str, path: str = "") -> None:
        """添加发现。

        Args:
            level: error 或 warning。
            code: 机器可读代码。
            message: 人类可读说明。
            path: 相关路径。
        """
        self.findings.append(Finding(level, code, message, path))

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.level == "error"]


def repo_root() -> Path:
    """返回仓库根目录。

    Returns:
        含 project.json 或 tools/ 的根路径。
    """
    return Path(__file__).resolve().parents[1]


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """有限 Frontmatter 解析（非完整 YAML）。

    Args:
        text: SKILL.md 全文。

    Returns:
        简单键值字典；若缺少 --- 围栏则返回 None。
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    block = text[3:end].strip("\n")
    data: dict[str, str] = {}
    current_key: str | None = None
    current_parts: list[str] = []

    def flush() -> None:
        nonlocal current_key, current_parts
        if current_key is not None:
            data[current_key] = " ".join(p.strip() for p in current_parts).strip()
        current_key = None
        current_parts = []

    for line in block.splitlines():
        if re.match(r"^[A-Za-z0-9_-]+\s*:", line) and not line.startswith(" "):
            flush()
            key, _, rest = line.partition(":")
            current_key = key.strip()
            rest = rest.strip()
            if rest in {">-", "|", ">"}:
                current_parts = []
            else:
                current_parts = [rest.strip("\"'")]
        else:
            if current_key is not None:
                current_parts.append(line.strip().strip("\"'"))
    flush()
    return data


def iter_skill_dirs(root: Path) -> Iterable[Path]:
    """迭代 skills 根下的一级 Skill 目录。

    Args:
        root: 仓库根。

    Yields:
        Skill 目录路径。
    """
    skills_root = root / ".agents" / "skills"
    if not skills_root.is_dir():
        return
    for path in sorted(skills_root.iterdir()):
        if path.is_dir() and not path.name.startswith("."):
            yield path


def check_skills(root: Path, report: Report) -> None:
    """验证全部 Skill 结构。

    Args:
        root: 仓库根。
        report: 报告对象。
    """
    skills_root = root / ".agents" / "skills"
    if not skills_root.is_dir():
        report.add("error", "skills_root_missing", "Missing .agents/skills/", str(skills_root))
        return

    skill_dirs = list(iter_skill_dirs(root))
    if not skill_dirs:
        report.add("error", "no_skills", "No skill directories found", str(skills_root))
        return

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            report.add("error", "missing_skill_md", "SKILL.md missing", str(skill_dir))
            continue
        try:
            text = skill_md.read_text(encoding="utf-8")
        except OSError as exc:
            report.add("error", "read_failed", str(exc), str(skill_md))
            continue

        fm = parse_frontmatter(text)
        if fm is None:
            report.add("error", "frontmatter_missing", "Missing --- frontmatter", str(skill_md))
            continue
        name = fm.get("name", "").strip()
        desc = fm.get("description", "").strip()
        if not name:
            report.add("error", "name_missing", "Frontmatter name missing", str(skill_md))
        if not desc:
            report.add("error", "description_missing", "Frontmatter description missing", str(skill_md))
        if name and name != skill_dir.name:
            report.add(
                "error",
                "name_mismatch",
                f"name '{name}' != directory '{skill_dir.name}'",
                str(skill_md),
            )
        if name and not NAME_RE.match(name):
            report.add("error", "name_invalid", f"Invalid name '{name}'", str(skill_md))

        # Relative resource links inside skill
        for match in REL_PATH_IN_SKILL_RE.finditer(text):
            rel = match.group(1)
            target = skill_dir / rel
            if not target.exists():
                report.add(
                    "error",
                    "broken_skill_path",
                    f"Referenced path missing: {rel}",
                    str(skill_md),
                )

        # Markdown links relative to skill dir
        for _, href in MD_LINK_RE.findall(text):
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = href.split("#", 1)[0]
            if not clean:
                continue
            # Disallow escaping to other skills as runtime dependency signal
            if clean.startswith("../") and ".agents/skills/" in str((skill_dir / clean).resolve()):
                resolved = (skill_dir / clean).resolve()
                try:
                    resolved.relative_to((root / ".agents" / "skills").resolve())
                    if resolved.parent != skill_dir.resolve() and resolved.parent.parent == (
                        root / ".agents" / "skills"
                    ).resolve():
                        report.add(
                            "error",
                            "cross_skill_runtime_ref",
                            f"Cross-skill reference not allowed for standalone install: {href}",
                            str(skill_md),
                        )
                        continue
                except ValueError:
                    pass
            target = (skill_dir / clean).resolve()
            if not target.exists():
                # Also allow links to repo docs only as documentation — warn
                alt = (root / clean).resolve()
                if alt.exists():
                    report.add(
                        "warning",
                        "repo_level_doc_link",
                        f"Links outside skill dir (doc-only?): {href}",
                        str(skill_md),
                    )
                else:
                    report.add(
                        "error",
                        "broken_md_link",
                        f"Broken relative link: {href}",
                        str(skill_md),
                    )

        # Absolute path literals (exclude Windows drive examples in docs carefully)
        for match in ABS_PATH_RE.finditer(text):
            snippet = match.group(0)
            # Allow illustrative placeholders in comments? Flag as warning if looks real home path
            if "path\\to" in snippet.lower() or "path/to" in snippet.lower():
                continue
            if snippet.startswith(("D:\\path", "C:\\path", "/path/to")):
                continue
            report.add(
                "warning",
                "absolute_path_literal",
                f"Possible absolute path literal: {snippet}",
                str(skill_md),
            )


def check_readme_links(root: Path, report: Report) -> None:
    """检查 README 关键内部链接。

    Args:
        root: 仓库根。
        report: 报告对象。
    """
    for name in ("README.md", "README_EN.md"):
        path = root / name
        if not path.is_file():
            report.add("error", "readme_missing", f"Missing {name}", str(path))
            continue
        text = path.read_text(encoding="utf-8")
        # language switch
        if name == "README.md" and "README_EN.md" not in text:
            report.add("error", "lang_switch_missing", "Missing link to README_EN.md", str(path))
        if name == "README_EN.md" and "README.md" not in text:
            report.add("error", "lang_switch_missing", "Missing link to README.md", str(path))

        for _, href in MD_LINK_RE.findall(text):
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = href.split("#", 1)[0]
            if not clean:
                continue
            target = (path.parent / clean).resolve()
            if not target.exists():
                report.add("error", "broken_readme_link", f"Broken link: {href}", str(path))


def check_required_docs(root: Path, report: Report) -> None:
    """检查必需文档是否存在。

    Args:
        root: 仓库根。
        report: 报告。
    """
    required = [
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CHANGELOG.md",
        "project.json",
        "docs/PRODUCT_SPEC.md",
        "docs/ROADMAP.md",
        "docs/decisions/open-questions.md",
        "docs/zh-CN/installation.md",
        "docs/zh-CN/architecture.md",
        "docs/en/installation.md",
        "docs/en/architecture.md",
        "evals/README.md",
        "docs/zh-CN/cursor-smoke-test.md",
        "docs/en/cursor-smoke-test.md",
        ".gitignore",
        ".editorconfig",
    ]
    for rel in required:
        if not (root / rel).exists():
            report.add("error", "required_missing", f"Missing required path: {rel}", rel)

    # installation docs should mention .agents/skills
    for rel in ("docs/zh-CN/installation.md", "docs/en/installation.md"):
        text = (root / rel).read_text(encoding="utf-8")
        if ".agents/skills" not in text:
            report.add(
                "error",
                "install_path_mismatch",
                "Installation doc missing .agents/skills",
                rel,
            )


def check_project_json(root: Path, report: Report) -> None:
    """校验 project.json 基本字段。

    Args:
        root: 仓库根。
        report: 报告。
    """
    path = root / "project.json"
    if not path.is_file():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        report.add("error", "project_json_invalid", str(exc), str(path))
        return
    for key in ("brand_name", "repo_name_suggested", "skills_root", "license_status"):
        if key not in data:
            report.add("error", "project_json_key", f"Missing key: {key}", str(path))
    if data.get("brand_name") != "ScholarlyOps":
        report.add("warning", "brand_mismatch", "brand_name is not ScholarlyOps", str(path))
    if data.get("license_status") == "undetermined" and (root / "LICENSE").exists():
        report.add(
            "warning",
            "license_status_conflict",
            "LICENSE exists but project.json says undetermined",
            str(path),
        )


def check_gitignore_safety(root: Path, report: Report) -> None:
    """粗检 .gitignore 是否误忽略 skills。

    Args:
        root: 仓库根。
        report: 报告。
    """
    gi = root / ".gitignore"
    if not gi.is_file():
        return
    text = gi.read_text(encoding="utf-8")
    dangerous = [".agents/", ".agents/**", ".agents/skills/", "README.md"]
    for pattern in dangerous:
        # Exact line match ignoring comments
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if stripped == pattern:
                report.add(
                    "error",
                    "gitignore_blocks_skills",
                    f".gitignore ignores critical path pattern: {pattern}",
                    str(gi),
                )


def main(argv: list[str] | None = None) -> int:
    """验证入口。

    Args:
        argv: CLI 参数。

    Returns:
        有 error 时返回 1，否则 0。
    """
    parser = argparse.ArgumentParser(description="Validate ScholarlyOps skills and docs")
    parser.add_argument("--root", type=Path, default=None, help="Repository root")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve() if args.root else repo_root()

    report = Report()
    check_required_docs(root, report)
    check_project_json(root, report)
    check_skills(root, report)
    check_readme_links(root, report)
    check_gitignore_safety(root, report)

    if args.json:
        print(
            json.dumps(
                {
                    "root": str(root),
                    "error_count": len(report.errors),
                    "findings": [f.__dict__ for f in report.findings],
                    "frontmatter_note": "Limited string parsing; not full YAML validation.",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(f"ScholarlyOps validate_skills — root={root}")
        print("Note: frontmatter checks are limited string parsing, not full YAML.")
        if not report.findings:
            print("OK: no findings")
        for finding in report.findings:
            loc = f" @ {finding.path}" if finding.path else ""
            print(f"[{finding.level.upper()}] {finding.code}: {finding.message}{loc}")
        print(f"Summary: {len(report.errors)} error(s), {len(report.findings) - len(report.errors)} warning(s)")

    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
