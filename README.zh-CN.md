# GPT-5.6 Prompt Skill Suite

[English](README.md) | [简体中文](README.zh-CN.md)

## 项目概览

GPT-5.6 Prompt Skill Suite 是一套由七个 Codex skills 组成的 Prompt 工程工具集，用于把自然语言形式的 Prompt 需求转换为经过审查、符合 Schema 且可以评测的 **PromptPackage v1**。

这套工具不只是生成一段 Prompt。它会先定义任务契约，再将需求路由给通用任务、工具 Agent 或软件工程等适用模块，随后进行语义审查、校验规范 JSON、确定性渲染 Markdown，并如实记录动态评测已经执行、失败或尚未运行。

这是一个独立维护的非官方开源项目，与 OpenAI 不存在隶属关系，也未获得 OpenAI 背书。

## 项目来源与设计原则

这个项目最初希望把以下两份 OpenAI 文档中的实践建议转化为可以复用的 Codex 工作流：

- [GPT-5.6 Prompt 指南](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6)
- [GPT-5.6 模型指南](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6)

本项目对这些指导的理解可以概括为：

- **先定义结果。** 明确用户最终要获得什么、有哪些约束和证据、怎样才算成功，以及何时应该停止；不强行规定每一步推理过程。
- **保持 Prompt 精简。** 删除重复规则、无效示例、相互矛盾的约束和与任务无关的工具，只保留确实会改变行为的要求。
- **建立清晰的 Prompt Contract。** 分开描述角色、个性、协作方式、目标、成功标准、约束、证据、权限、输出和停止条件，并完整保留用户显式指定的值。
- **集中定义自主权边界。** 允许模型继续执行安全且范围内的本地工作；外部写入、破坏性操作、购买以及实质性扩大范围必须先获得确认。
- **有意识地路由工具。** 只暴露相关工具，行动前先完成必要检索；独立读取可以并行，有依赖关系的调用保持顺序，并为无结果或不完整结果设计有效回退。
- **限制 Programmatic Tool Calling 的边界。** PTC 适合过滤、连接、排序、去重、聚合、批处理和重复校验等确定性缩减；审批、语义判断、引用处理和最终验证仍交给模型直接完成。
- **让研究建立在证据上。** 将引用放在所支持的陈述附近，区分来源事实和推断，指出来源冲突；证据不足时缩小结论或说明缺口，不进行猜测。
- **按阶段管理长任务。** 开始工具调用前给出简短说明，只在主要阶段变化时更新具体结果和下一步；在有意义的里程碑进行压缩，避免旧推理锚定已经变化的目标。
- **根据工作负载选择模型参数。** 这套工具把 `gpt-5.6`（Sol 路由）作为质量优先基线，把 `gpt-5.6-terra` 视为成本平衡候选，把 `gpt-5.6-luna` 视为高吞吐候选。新任务从 `medium` reasoning 开始评测，只有代表性评测证明有收益时才采用更高设置。
- **区分默认详细度和任务要求。** 使用 `text.verbosity` 控制请求级默认详细程度，把必须保留的事实、结构、长度、限制和警告写入 Prompt Contract。
- **验证真正交付的产物。** 软件修改后执行针对性检查，无法运行的检查必须披露；前端任务保留现有设计系统，视觉产物在完成前必须渲染并检查。
- **用评测推动迁移。** 每次只改变一组 Prompt、工具或 reasoning 参数。只有输出质量仍达到基线时，Token、延迟、成本或调用次数下降才算收益。

以上内容是本项目的精炼理解，不能替代官方文档。当前 API 细节、限制、价格和功能可用性应以链接中的官方指南为准。

## 这套 Skills 会生成什么

一次完整运行可以交付：

- `prompt-package.json`：PromptPackage v1 的唯一规范来源。
- `prompt-package.md`：只从通过校验的 JSON 确定性生成的人类可读版本。
- 静态验证：语义审查、JSON Schema 校验和跨字段引用检查。
- 评测记录：代表性用例、基线比较以及如实记录的 `pass`、`fail` 或 `not_run` 状态。

可选配置只在适用时出现。例如，只有使用工具的任务才会包含 `tool_policy`；只有存在有边界的确定性处理阶段才会包含 PTC 配置；单轮任务不会输出持久化 reasoning 配置。

## Skills 组成

| Skill | 职责 |
|---|---|
| `building-prompt-packages` | 唯一面向用户的通用入口；负责路由需求、组合适用模块、校验 PromptPackage、渲染 Markdown 并组织交付。 |
| `defining-prompt-contracts` | 把原始需求归一化为目标、成功标准、证据要求、权限、输出规则和停止条件。 |
| `prompting-general-tasks` | 处理研究、分析、写作、改写、摘要、提取等通用知识工作模式。 |
| `prompting-tool-agents` | 定义工具路由、检索、引用、审批、PTC 边界、长任务状态和失败回退。 |
| `prompting-software-engineering` | 覆盖诊断、实现、测试、审查、前端开发和视觉验证。 |
| `reviewing-prompt-packages` | 检查重复、矛盾、过度约束、缺项、无关工具和不可验证的要求。 |
| `evaluating-prompt-packages` | 生成代表性用例，记录实际执行证据，并将候选 Prompt 与基线比较。 |

## 工作流

```text
自然语言需求
  -> Prompt Contract
  -> 场景模块
  -> 候选 Prompt
  -> 静态审查
  -> JSON 校验
  -> Markdown 渲染
  -> 动态评测
  -> 最终交付
```

`prompt-package.json` 是唯一规范来源。`prompt-package.md` 不会被独立维护：渲染器只读取已经通过校验的 PromptPackage，并按照固定顺序生成内容。

## 环境要求

- Windows 和 PowerShell，用于运行本文档中的命令。
- 支持 `venv` 的 Python 3。
- 支持本地 skills 的 Codex。
- Git，用于克隆项目和参与贡献。

运行时校验依赖 `jsonschema>=4.23,<5`；开发和元数据检查还使用 `PyYAML>=6,<7`。

## 初始化仓库

```powershell
git clone https://github.com/Xerneas216/prompt-skill-suite.git
Set-Location prompt-skill-suite
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

最后一条命令会在安装或修改 Skills 之前建立本地确定性测试基线。

## 安装 Skills

先预览安装内容，不写入任何文件：

```powershell
.\.venv\Scripts\python.exe install_skills.py --dry-run
```

将七个 Skills 安装到默认 Codex skills 目录：

```powershell
.\.venv\Scripts\python.exe install_skills.py
```

默认目标是 `<home>/.codex/skills`，在 Windows 上对应 `%USERPROFILE%\.codex\skills`。安装器会：

- 只发现同时包含 `SKILL.md` 和 `agents/openai.yaml` 的 skill 目录；
- 在发布任何文件之前拒绝全部同名冲突；
- 通过唯一暂存目录复制清单中列出的源文件；
- 在发布前后检查完整文件集合和 SHA-256 哈希；
- 仅在安装副本验证通过后写入 `.prompt-skill-suite-manifest.json`；
- 不覆盖已有 Skill 或已有清单。

如果检测到冲突，请先检查并有意识地处理现有安装；安装器不会自动覆盖。安装完成后新建一个 Codex 任务，让 Skill 发现机制刷新。

## 使用方法

在新的 Codex 任务中，用自然语言描述你希望构建的 PromptPackage。`building-prompt-packages` 会作为入口，并自动选择适用的专家模块。

通用来源型任务：

> 为政策文档摘要构建一个高质量 PromptPackage。保留所有事实限定，引用所提供的来源，并在不丢失重要警告的前提下保持最终回答简洁。

工具 Agent 任务：

> 为一个检索账户与政策证据的 Agent 构建 PromptPackage。说明空结果回退，并要求任何外部写入都先获得批准。

软件工程任务：

> 为诊断并修复 Python 回归问题构建 PromptPackage。仅诊断时不得修改文件；授权修复后必须运行针对性测试，并披露所有无法完成的验证。

研究与实现混合任务：

> 为一项混合任务构建 PromptPackage：先研究当前 API 要求并引用一手来源，再更新范围内的集成代码并验证行为，不得扩大项目范围。

默认对话交付包含两层：

1. 简洁的路由、模型设置、验证状态和遗留风险摘要。
2. 规范 JSON 内容，以及从该 JSON 渲染得到的 Markdown。

只有用户明确要求文件交付时，这套工具才会把 `prompt-package.json` 和 `prompt-package.md` 写入磁盘。

## 校验并渲染 PromptPackage

校验候选 PromptPackage：

```powershell
.\.venv\Scripts\python.exe skills\building-prompt-packages\scripts\validate_package.py prompt-package.json
```

只有校验成功后才渲染 Markdown：

```powershell
.\.venv\Scripts\python.exe skills\building-prompt-packages\scripts\render_package.py prompt-package.json --output prompt-package.md
```

校验器不仅检查 JSON Schema，还会检查显式值保留、场景模块覆盖、消息层分离、工具引用、依赖环、PTC 引用、审批规则、内嵌 Schema 和评测证据等语义不变量。

## 验证状态

确定性测试覆盖：

- PromptPackage Schema 和语义校验；
- 工具、依赖、PTC 和模块引用；
- Markdown 确定性渲染和安全代码围栏；
- 与供应商无关的评测夹具结构；
- 安装冲突、暂存失败、发布竞争、精确文件集合以及源码到副本的哈希。

新鲜上下文动态评测是独立的质量门槛。如果没有合适的运行环境，其状态会保持为 `not_run`；确定性测试通过不等于模型质量已经得到动态验证。

## 仓库结构

```text
prompt-skill-suite/
├── skills/                 # 七个源 Skills
├── evals/                  # 代表性用例和 RED/GREEN 记录
├── tests/                  # 确定性 unittest 测试
├── tools/                  # 安装器实现
├── docs/superpowers/       # 已批准的设计和实施记录
├── install_skills.py       # 根目录安装入口
├── requirements.txt        # 运行时依赖
└── requirements-dev.txt    # 开发依赖
```

规范 Schema 位于 `skills/building-prompt-packages/references/prompt-package.schema.json`。校验器和渲染器位于入口 Skill 的 `scripts/` 目录。

## 项目状态

初始版本具有以下边界：

- 面向 Codex skills；
- 以 GPT-5.6 为优先目标，后续 GPT-5.x 必须重新评测后才能采用；
- 使用 Windows 和 PowerShell 编写并验证使用文档；
- 提供与供应商无关的评测夹具，不要求 OpenAI API Key；
- 不包含插件、Web UI、托管服务、包注册表发布或其他模型供应商适配器。

## 参与贡献

欢迎提交范围明确的 Issue 和 Pull Request。请说明观察到的 Prompt 失败或缺失行为，提供代表性用例，保持指导精简，并附上证明修改合理的验证证据。涉及模型指导的修改应链接当前一手文档，不得静默覆盖用户显式值或已有评测基线。

## 开源许可

本项目采用 [MIT License](LICENSE) 开源。Copyright (c) 2026 Xerneas216。
