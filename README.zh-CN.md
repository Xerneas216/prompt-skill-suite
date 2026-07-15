# ProCraft 🛠️

[English](README.md) | [简体中文](README.zh-CN.md)

ProCraft 可以把一个模糊的 Prompt 想法，整理成能直接交给模型或 Agent 使用的指令。简单需求直接给成品，生产级工作流再进入任务契约、工具规则、校验和评测。

它为 Codex 设计，并围绕 GPT-5.6 调校。当前项目版本是 `v0.2.0`，产物格式继续使用 PromptPackage Schema v1.0。

## 这个项目从哪里来

ProCraft 的起点是 OpenAI 的两份文档：

- [GPT-5.6 Prompt 指南](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6)
- [GPT-5.6 模型指南](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6)

它们给出的实用思路很直接：把目标、证据、权限和完成条件说清楚，同时别把模型的每一步推理都写死。

ProCraft 提炼并落实了这些做法：

- 先写清结果、成功标准、证据、约束和停止条件。用户明确指定的值必须原样保留。
- 删掉重复指令、冲突规则、无关示例和任务用不到的工具。
- 范围内且安全的工作可以继续做。破坏性操作、外部写入、购买或实质性扩展范围，需要先获得批准。
- 行动前先取得前置资料。互不依赖的读取可以并行，有依赖的调用保持顺序，工具空结果也要有实际可用的回退方案。
- Programmatic Tool Calling 只处理边界明确的确定性缩减，例如过滤、连接、排序、去重、聚合、批处理和重复校验。审批流程和语义判断仍留在模型的直接工具调用路径中；批准本身必须由用户或其他授权方给出。
- 引用应靠近它支持的陈述。推断要明确标注，来源冲突要说出来，缺证据时不能靠猜测补齐。
- reasoning effort 和 `text.verbosity` 是要通过评测选择的控制项，不是默认越高越好。新任务从 `medium` 开始，更高设置需要实际收益证据。
- 验证用户最终拿到的东西。软件类 Prompt 应要求针对性测试，如实披露未运行的检查，视觉工作则要先渲染再验收。
- 迁移时一次只改一组 Prompt、工具或模型参数。输出质量达到基线之后，成本和延迟下降才算收益。

用户没有指定模型时，ProCraft 把 `gpt-5.6` 作为质量优先默认值；`gpt-5.6-terra` 是成本平衡候选，`gpt-5.6-luna` 是高吞吐候选。这些只是评测起点，不会自动替你升级。

当前 API 行为、限制、价格和功能可用性，仍以链接中的官方文档为准。

## 什么情况下会触发 🎯

ProCraft 看的是用户要交付什么。只有用户明确想要 Prompt、系统指令、developer 或 user message、Agent 规则、工具策略、Structured Output 契约，或其他可复用模型指令时，它才应该自动参与。

普通写作、邮件、研究、摘要、编程和代码诊断不会触发 ProCraft。只要用户要的是执行这些工作的 Prompt 或模型指令，才会触发。

| 用户请求 | 是否触发 |
|---|---|
| "帮我写一封邮件，把周五的会议改期。" | 否。交付物是邮件。 |
| "研究一下现在有哪些 API 方案。" | 否。交付物是研究结果。 |
| "修一下解析器的回归问题。" | 否。交付物是代码修改。 |
| "写一个用于生成邮件的 Prompt，输入是几条会议信息。" | 是。交付物是 Prompt。 |
| "为这个 Agent 设计 system、developer 和 user messages。" | 是。交付物是模型指令。 |
| "检查这份工具策略有没有漏掉审批边界。" | 是。交付物本身属于 Prompt 系统。 |

想明确调用时，直接在请求开头写 `$procraft`。Codex 目前不支持自定义 `@ProCraft` Skill 语法。

## 快速模式和完整模式

除非用户明确选择模式，ProCraft 会走能完成任务的最短路线。

| 模式 | 适用情况 | 交付内容 |
|---|---|---|
| 快速模式 | 单轮 Prompt，不使用工具，没有副作用，也不要求基线评测。 | 可直接使用的 Prompt、必要变量和重要假设。 |
| 完整模式 | 生产复用、多层消息、Structured Outputs、工具或审批、长期 Agent、仓库工作、Prompt 审查评测或模型迁移。 | 通过校验的 PromptPackage、渲染版 Markdown、静态审查和有证据的评测状态。 |

需求不够清楚时，ProCraft 会先给出可用的快速模式结果，并说明可以升级为完整模式。一个小 Prompt 不会被硬塞进空洞的大礼包。

## 内部怎么配合

项目采用一个公开入口和六个内部模块。多数用户只需要 `procraft`，其余模块会在流程走到对应阶段时加入。

| 模块 | 在工作流中的职责 |
|---|---|
| `procraft` | 选择快速或完整模式，路由任务，检查完成条件并交付结果。 |
| `defining-prompt-contracts` | 把需求整理成目标、成功标准、证据、权限、输出规则和停止条件。 |
| `prompting-general-tasks` | 处理研究、分析、写作、改写、摘要和提取类 Prompt。 |
| `prompting-tool-agents` | 定义工具路由、检索、引用、审批、PTC 边界、状态和回退。 |
| `prompting-software-engineering` | 覆盖诊断、代码修改、测试、审查、前端和视觉检查。 |
| `reviewing-prompt-packages` | 查找矛盾、重复、缺项、无关工具和无法验证的要求。 |
| `evaluating-prompt-packages` | 生成代表性用例，记录执行证据，并与基线比较。 |

完整模式遵循固定数据流：

```text
用户需求
  -> Prompt Contract
  -> 适用的内部模块
  -> 候选 PromptPackage JSON
  -> 静态审查
  -> JSON 校验
  -> 确定性渲染 Markdown
  -> 动态评测或 not_run
  -> 最终交付
```

`prompt-package.json` 是唯一规范来源，`prompt-package.md` 只从通过校验的 JSON 按固定顺序生成，因此两份产物不会各写各的。可选字段只在适用时出现，例如无工具任务不会塞入空的 `tool_policy`。

## 安装 🚀

下面的命令适用于 Windows PowerShell，并需要 Python 3 和 Git。

```powershell
git clone https://github.com/Xerneas216/ProCraft.git
Set-Location ProCraft
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

先预览安装动作：

```powershell
.\.venv\Scripts\python.exe install_skills.py --dry-run
```

确认后安装到 `%USERPROFILE%\.codex\skills`：

```powershell
.\.venv\Scripts\python.exe install_skills.py
```

安装器只负责全新安装。遇到现有 ProCraft 清单或任何同名 Skill 目录时会直接停止；新文件会先进入暂存区并校验 SHA-256，发布失败时只回滚仍保持原样的文件。

安装状态记录在 `.procraft-manifest.json`。安装完成后新建一个 Codex 任务，让本地 Skill 发现机制刷新。

## 开始使用

一个快速模式请求可以很短：

> `$procraft` 创建一个可复用 Prompt，把零散会议记录整理成简洁的跟进邮件，承诺和日期不能改变。

完整模式可以带上工具与审批规则：

> `$procraft` 为一个生产 Agent 构建 PromptPackage。它需要检索账户与政策证据，说明空结果回退，并在任何外部写入前请求批准。

软件工程 Prompt 也可以这样提：

> 为诊断并修复 Python 回归问题创建模型指令。诊断阶段保持只读；获得修复授权后运行针对性测试，并披露所有未能执行的检查。

快速模式会返回 Prompt、变量和假设。完整模式会返回规范 JSON，以及从该 JSON 渲染出的 Markdown。只有用户明确要求文件交付时，ProCraft 才会把 `prompt-package.json` 和 `prompt-package.md` 写入磁盘。

## 校验并渲染 PromptPackage

校验规范 JSON：

```powershell
.\.venv\Scripts\python.exe skills\procraft\scripts\validate_package.py prompt-package.json
```

校验成功后渲染 Markdown：

```powershell
.\.venv\Scripts\python.exe skills\procraft\scripts\render_package.py prompt-package.json --output prompt-package.md
```

校验器会检查 Schema 和语义引用，包括用户显式值、场景模块、消息层、工具引用、依赖环、PTC、审批、内嵌 Schema 和评测证据。

## 验证状态 🧪

确定性测试覆盖 PromptPackage 校验、Markdown 确定性渲染、与供应商无关的评测夹具、触发契约，以及包含可信迁移与回滚在内的安装器安全行为。

新鲜上下文动态评测是另一道门槛。没有实际执行证据时，其状态必须保持 `not_run`。单元测试通过不能把它变成模型质量已经验证的结论。

## 仓库结构

```text
ProCraft/
├── skills/                 # 公开入口和内部模块
├── evals/                  # 代表性用例和证据记录
├── tests/                  # 确定性 unittest 测试
├── tools/                  # 安装器和迁移信任锚
├── docs/superpowers/       # 历史设计与实施记录
├── install_skills.py       # 安装入口
├── requirements.txt        # 运行依赖
└── requirements-dev.txt    # 开发依赖
```

PromptPackage Schema 位于 `skills/procraft/references/prompt-package.schema.json`，校验器和渲染器位于 `skills/procraft/scripts/`。

## 参与贡献

一项有用的修改，应该从真实失败或缺失行为开始。请添加代表性用例，把新增指导控制在解决问题所需的最小范围，并附上能证明修改有效的检查。模型指导的变化应引用当前一手文档，同时保留用户显式选择和已有评测基线。

## 开源许可

[MIT License](LICENSE)，Copyright (c) 2026 Xerneas216。
