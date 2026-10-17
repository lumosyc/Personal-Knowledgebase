# 文件保存与恢复

使用工作区 `tools/kb.py`，或插件技能目录的 `scripts/kb.py`；Python 3.10+，仅标准库。命令参数中的路径使用宿主 shell 的正确引用方式。工作区根必须显式给出，避免当前聊天目录变化时写错知识库。

```text
python <脚本绝对路径> status --root <工作区绝对路径>
python <脚本绝对路径> profile --root <工作区绝对路径> --patch <本轮增量JSON绝对路径>
python <脚本绝对路径> lint --root <工作区绝对路径>
```

每个答案后，由 Codex 将本轮新增事实与 `next_question` 写为 `temp/onboarding-<会话ID>-<轮次>.json`，执行 profile 并回读生成文件。用户只回答问题，不需要编辑 JSON。运行成功会报告写入清单和备份路径。

profile 自动保存：JSON 事实源 → learner_profile.md 摘要 → core_questions.md；新课程才创建课程骨架与索引，已有 course_map、mastery_tracker、error_log、problem_bank 不覆盖。课程初始“未评估”，不能因为画像基础好便标 L3 / L4。研究问题增量合并避免丢失 Q 引用。画像日志写 `meta/profile_log.md`，教学观察的详细证据仍留原学习记录。

覆盖前备份到 `meta/backups/<唯一批次>/`，用临时文件替换；捕获写入异常时回滚受影响文件。若进程突然终止，留有 `.pkb.lock` 和备份 `transaction.json`，这是待恢复状态，不声称已经提交。先读清单、比对 before / after SHA256、确认无活动保存进程，再按清单恢复相应文件。新建文件只在确认为该未提交批次创建且用户授权后移除。恢复完再移除该锁；禁止盲目清空整个备份目录。

初始化只向空目录复制模板；重复初始化为无操作；非空陌生目录拒绝，用户旧知识库另做有授权的 shadow migration。插件 cache 和模板不是用户数据目录。

`lint` 只读，检查损坏 / 歧义链接、孤立论文概念页、未知 Q 引用和画像结构。语义检查仍由 Codex 完成：证据冲突、concept debt 是否升级、研究 Q 文献密度、日志归属、索引覆盖。报告清楚区分自动检查和未核验项。

无 Python 时可通过 Codex 的文件工具完成同样字段合并，先备份旧文件，更新唯一事实源并生成两份摘要，然后回读核对；新课程按模板建页，绝不推定掌握度。说明未使用脚本事务。读写受权限限制时保留本轮草稿，不宣称已保存，不扩大授权范围。

研究 / 课程正文由 Codex 按原版 workflow 用文件工具维护，不受 profile 脚本替代。每次入库更新索引和对应日志；课程操作到 `courses/log.md`，研究操作到 `wiki/log.md`，辅导到 `socrates/progress.md`。
