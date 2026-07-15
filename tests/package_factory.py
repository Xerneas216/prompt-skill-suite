from copy import deepcopy


def minimal_general_package():
    return {
        "version": "1.0",
        "request": {
            "original_goal": "Summarize the supplied board minutes.",
            "scenario": "general",
            "audience": "Board members",
            "language": "zh-CN",
            "explicit_values": {
                "/model_profile/model": "gpt-5.6",
                "/prompt_contract/output/length_limit": "300 Chinese characters",
                "/request/language": "zh-CN",
                "/request/delivery": "conversation",
            },
            "uses_tools": False,
            "interaction_mode": "single_turn",
            "delivery": "conversation",
        },
        "assumptions": [],
        "model_profile": {
            "model": "gpt-5.6",
            "api": "responses",
            "text_verbosity": "medium",
            "reasoning_effort": "medium",
        },
        "prompt_contract": {
            "role": "Faithful board-minutes summarizer",
            "personality": ["Direct", "Neutral"],
            "collaboration": ["Surface impossible constraints instead of dropping facts"],
            "goal": "Produce a Chinese decision summary from supplied minutes.",
            "success_criteria": [
                "Preserve decisions, basis, dissent, owners, and dates",
                "Stay within the approved length when the required content fits",
            ],
            "constraints": ["Do not add facts", "Use only the supplied minutes"],
            "evidence": {
                "requirements": ["Every statement is traceable to the minutes"],
                "missing_evidence_behavior": "Mark the field as not stated in the minutes.",
            },
            "permissions": {
                "allowed": ["Read user-provided minutes"],
                "forbidden": ["Write files", "Use external sources"],
            },
            "output": {
                "language": "zh-CN",
                "format": "Decision summary",
                "required_content": ["Decision", "Basis", "Dissent", "Owner", "Date"],
                "length_limit": "300 Chinese characters",
            },
            "stop_rules": {
                "success": ["All required content is represented faithfully"],
                "blocked": ["Required content cannot fit the protected length limit"],
            },
        },
        "messages": {
            "system": "You preserve source facts and material qualifiers.",
            "developer": "Summarize the minutes under the contract and report impossible constraints.",
            "user_template": "Summarize these minutes: {{board_minutes}}",
            "variables": [
                {
                    "name": "board_minutes",
                    "description": "Trusted board-minutes text",
                    "required": True,
                    "source": "user",
                }
            ],
        },
        "response_format": {
            "type": "text",
            "structure": ["Decision", "Basis", "Dissent", "Owner", "Date"],
        },
        "verification": {
            "static_review": {"status": "pass", "findings": []},
            "dynamic_evaluation": {"status": "not_run", "evidence": []},
            "baseline_comparison": {"status": "not_run", "evidence": []},
            "automatic_repair_rounds": 0,
            "residual_risks": ["The protected content may exceed 300 characters"],
        },
        "provenance": {
            "sources": [
                {
                    "title": "GPT-5.6 Prompting Guide",
                    "url": "https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6",
                }
            ],
            "generated_at": "2026-07-15T08:00:00Z",
            "schema_version": "1.0",
            "participating_modules": [
                "procraft",
                "defining-prompt-contracts",
                "prompting-general-tasks",
                "reviewing-prompt-packages",
                "evaluating-prompt-packages",
            ],
        },
    }


def full_agent_package():
    package = minimal_general_package()
    package["request"].update(
        {
            "original_goal": "Research a supplier and email an approved summary.",
            "scenario": "agent",
            "uses_tools": True,
            "interaction_mode": "multi_turn",
        }
    )
    package["prompt_contract"]["goal"] = "Research supplier risk and send only an approved email."
    package["prompt_contract"]["permissions"] = {
        "allowed": ["Read supplier registry", "Read sanctions data"],
        "requires_approval": ["Send the exact displayed email"],
        "forbidden": ["Sign contracts", "Change recipients after approval"],
    }
    package["tool_policy"] = {
        "tools": [
            {
                "name": "registry_read",
                "purpose": "Read supplier registration data",
                "use_when": "After entity identifiers are available",
                "input_schema": {"type": "object", "required": ["supplier_id"]},
                "output_schema": {"type": "object", "required": ["facts", "source_handle"]},
                "returns": ["Registration facts", "Source handle"],
                "errors": ["Not found", "Unavailable"],
                "limits": ["Use runtime-documented rate and size limits"],
                "citation_support": "source_handles",
                "side_effect": "read",
            },
            {
                "name": "sanctions_read",
                "purpose": "Read sanctions records",
                "use_when": "After supplier identity is resolved",
                "input_schema": {"type": "object", "required": ["resolved_identity"]},
                "output_schema": {"type": "object", "required": ["matches", "source_handle"]},
                "returns": ["Possible matches", "Source handle"],
                "errors": ["Not found", "Unavailable"],
                "limits": ["Use runtime-documented rate and size limits"],
                "citation_support": "source_handles",
                "side_effect": "read",
            },
            {
                "name": "email_send",
                "purpose": "Send an approved email",
                "use_when": "After approval of the exact target and payload",
                "input_schema": {"type": "object", "required": ["recipient", "subject", "body"]},
                "output_schema": {"type": "object", "required": ["message_id", "status"]},
                "returns": ["Message identifier", "Delivery status"],
                "errors": ["Rejected", "Unknown outcome"],
                "limits": ["Use runtime-documented rate and payload limits"],
                "citation_support": "none",
                "side_effect": "write",
                "idempotency": "supported",
                "status_recovery": "supported",
            },
        ],
        "prerequisites": ["Resolve supplier identity before sanctions lookup"],
        "routing": [
            {"id": "registry", "instruction": "Read registry", "tool": "registry_read"},
            {
                "id": "sanctions",
                "instruction": "Read sanctions data",
                "tool": "sanctions_read",
                "depends_on": ["registry"],
            },
            {
                "id": "email",
                "instruction": "Send the approved email",
                "tool": "email_send",
                "depends_on": ["sanctions"],
            },
        ],
        "fallbacks": ["Return blocked when a required tool schema is unavailable"],
        "approvals": ["Require approval for the exact recipient, subject, body, and attachments"],
        "ptc": {
            "stage": "Deduplicate deterministic sanctions candidates",
            "eligible_tools": ["sanctions_read"],
            "deterministic_reduction": "deduplicate",
            "input_schema": {"type": "array"},
            "output_schema": {"type": "array"},
            "stop_conditions": ["All candidates have a terminal status"],
            "retry_policy": "Use only retry behavior documented by the tool contract.",
        },
    }
    package["provenance"]["participating_modules"].insert(3, "prompting-tool-agents")
    return deepcopy(package)
