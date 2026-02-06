# Skill Sync Script 使用说明

这个脚本用于将项目中的 skill 文件夹同步到 Claude Code 的实际 skill 安装目录。

## 功能

`sync_skill.py` 可以：

1. ✓ 自动备份现有的 skill
2. ✓ 复制修改后的 skill 文件到安装目录
3. ✓ 自动重新打包 skill (.skill 文件)
4. ✓ 更新项目中的 skill 包文件
5. ✓ 显示详细的同步过程和结果

## 使用方法

### 基本用法

在项目根目录运行：

```bash
python sync_skill.py
```

### 执行流程

脚本会提示你确认操作，然后自动完成以下步骤：

```
[STEP 1] 创建备份
  → 备份现有的 skill 到 github-pages-deploy_backup_YYYYMMDD_HHMMSS

[STEP 2] 同步文件
  → 从 github-pages-deploy-skill/ 复制到 skill 安装目录

[STEP 3] 打包
  → 创建新的 .skill 文件

[STEP 4] 更新项目
  → 更新项目中的 github-pages-deploy.skill 文件
```

### 示例输出

```
============================================================
GitHub Pages Deployment Skill - Sync Tool
============================================================

Project directory: E:\DeepLearning\AIChildGame
Source skill:      E:\DeepLearning\AIChildGame\github-pages-deploy-skill
Destination:       C:\Users\14679\.claude\plugins\cache\anthropic-agent-skills\...

[WARNING] This will overwrite the installed skill with your project version.
[INFO] A backup will be created automatically.

Continue? (y/n): y

[STEP 1] Creating backup...
[OK] Created backup: ...github-pages-deploy_backup_20250206_215000

[STEP 2] Syncing skill files...
[OK] Synced skill files from E:\DeepLearning\AIChildGame\github-pages-deploy-skill
[OK] To C:\Users\14679\.claude\...

[STEP 3] Packaging skill...
[OK] Packaged skill to: ...github-pages-deploy.skill
[OK] Package size: 30.5 KB

[STEP 4] Updating project package...
[OK] Updated project package: E:\DeepLearning\AIChildGame\github-pages-deploy.skill

============================================================
SYNC SUMMARY
============================================================
Source:      E:\DeepLearning\AIChildGame\github-pages-deploy-skill
Destination: C:\Users\14679\.claude\...\github-pages-deploy
Status:      SUCCESS
Packaged:    YES
Project:     UPDATED
============================================================

[NEXT STEPS]
1. Restart Claude Code to reload the skill
2. Test the skill by asking: 'deploy to GitHub Pages'
3. If something is wrong, restore from backup
```

## 工作流程

### 开发工作流

当你想修改 skill 时：

1. **修改项目中的 skill 文件**
   ```bash
   # 编辑 github-pages-deploy-skill/SKILL.md
   # 或修改 scripts/, references/, assets/ 中的文件
   ```

2. **同步到 Claude Code**
   ```bash
   python sync_skill.py
   ```

3. **重启 Claude Code**
   - 关闭并重新打开 Claude Code
   - 或者重新加载技能（如果支持）

4. **测试修改**
   - 使用 skill 部署一个项目
   - 验证修改是否生效

### 如果出错

脚本会自动创建备份，如果同步后出现问题：

1. 找到备份目录（显示在输出中）
2. 手动恢复文件
3. 或者重新运行 sync_skill.py

## 文件结构

```
AIChildGame/
├── github-pages-deploy-skill/    # 你修改的 skill 源文件
│   ├── SKILL.md
│   ├── scripts/
│   ├── references/
│   └── assets/
│
├── github-pages-deploy.skill      # skill 安装包
├── sync_skill.py                  # 同步脚本 ← 这个脚本
├── README-skill.md                # skill 使用说明
└── README-sync.md                 # 这份文档
```

## 注意事项

### ⚠️ 重要提示

1. **会覆盖现有文件**
   - 脚本会完全替换目标目录
   - 但会自动创建备份

2. **需要重启 Claude Code**
   - 同步后必须重启才能生效
   - 因为技能是在启动时加载的

3. **路径自动检测**
   - 脚本自动找到你的 Claude Code 安装目录
   - 基于 Windows 用户目录

4. **权限要求**
   - 需要有写入 Claude Code 安装目录的权限
   - 通常默认就有权限

## 高级用法

### 仅同步文件（不打包）

如果只想同步文件，不想重新打包：

编辑 `sync_skill.py`，注释掉打包部分：
```python
# packaged = package_skill(skills_dir, dest_skill)
```

### 自定义备份位置

修改 `backup_skill()` 函数中的备份路径。

### 批量同步多个 skill

修改脚本以支持多个 skill 的同步。

## 故障排除

### 问题 1: "Permission denied"

**原因**: 文件被占用或权限不足

**解决**:
- 关闭 Claude Code
- 以管理员身份运行脚本
- 检查文件是否被其他程序占用

### 问题 2: "Source skill directory not found"

**原因**: 项目中没有 skill 文件夹

**解决**:
- 确保 `github-pages-deploy-skill/` 文件夹存在
- 检查是否在正确的项目目录

### 问题 3: 同步后 skill 没有生效

**原因**: Claude Code 缓存或未重启

**解决**:
- 完全关闭 Claude Code（不仅仅是关闭窗口）
- 重新打开 Claude Code
- 清除缓存（如果问题持续）

## 安全性

- ✓ 自动创建备份
- ✓ 需要用户确认才执行
- ✓ 显示详细的操作日志
- ✓ 可以 Ctrl+C 随时取消

## 版本历史

- **v1.0** (2025-02-06)
  - 初始版本
  - 支持文件同步、打包、备份

## 贡献

如果发现问题或有改进建议，请修改 `sync_skill.py` 并同步更新。

## 许可

与主项目相同。
