"""The model layer: the only file that knows which LLM provider is used. Swapping the model is a change here
(or just the AIRPORT_AGENT_MODEL environment variable).

The model's job is small: pick a tool, then explain the numbers the tool returned. It never computes.
"""
import os
from dataclasses import dataclass, field

import anthropic
from dotenv import load_dotenv

from .paths import ROOT

DEFAULT_MODEL = "claude-opus-5-5"
MAX_TOKENS = 16000          # thinking counts toward this limit, so a low cap would truncate answers
EFFORT = "medium"           # set explicitly: the task is routing plus a faithful explanation
FALLBACK_BETA = "server-side-fallback-2026-07-01"


class ConfigError(RuntimeError):
    """Something the user has to fix (for example a missing API key)."""


class ModelError(RuntimeError):
    """The model service failed after the SDK's own retries."""


@dataclass
class Reply:
    content: list                      # the model's reply exactly as received; sent back unchanged next turn
    text: str
    tool_calls: list = field(default_factory=list)   # [{"id", "name", "input"}]
    stop_reason: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    model: str = ""


def model_name() -> str:
    load_dotenv(ROOT / ".env")
    return os.environ.get("AIRPORT_AGENT_MODEL") or DEFAULT_MODEL


def _api_key() -> str:
    load_dotenv(ROOT / ".env")
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        try:  # hosted on Streamlit Cloud: the key lives in its secrets
            import streamlit as st
            key = str(st.secrets.get("ANTHROPIC_API_KEY", "")).strip()
        except Exception:
            key = ""
    if not key or not key.startswith("sk-"):
        raise ConfigError("No Anthropic API key found. Create one at console.anthropic.com, then put it in the file "
                          "`.env` in the project folder as:  ANTHROPIC_API_KEY=sk-ant-...")
    return key


_client = None


def client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=_api_key(), max_retries=3, timeout=180.0)
    return _client


def complete(messages: list, system: str, tools: list, model: str | None = None) -> Reply:
    """One model call. Tool choice is automatic, thinking is adaptive (the model's default), no temperature."""
    try:
        resp = client().beta.messages.create(
            model=model or model_name(),
            max_tokens=MAX_TOKENS,
            system=system,
            tools=tools,
            messages=messages,
            output_config={"effort": EFFORT},
            cache_control={"type": "ephemeral"},   # the system prompt, tools and earlier turns are reused each call
            betas=[FALLBACK_BETA],
            fallbacks="default",                   # if the model declines, the API re-runs on a fallback model
        )
    except anthropic.AuthenticationError as err:
        raise ConfigError("The Anthropic API key was rejected. Check the key in `.env`.") from err
    except anthropic.PermissionDeniedError as err:
        raise ConfigError(f"The API key is not allowed to use this model: {err.message}") from err
    except anthropic.NotFoundError as err:
        raise ConfigError(f"Model not found: {model or model_name()}.") from err
    except anthropic.RateLimitError as err:
        raise ModelError("The model is rate-limited right now. Wait a moment and try again.") from err
    except anthropic.APIStatusError as err:
        raise ModelError(f"The model service returned an error ({err.status_code}): {err.message}") from err
    except anthropic.APIConnectionError as err:
        raise ModelError("Could not reach the model service. Check the internet connection and try again.") from err

    text = "\n".join(b.text for b in resp.content if b.type == "text").strip()
    calls = [dict(id=b.id, name=b.name, input=b.input) for b in resp.content if b.type == "tool_use"]
    return Reply(content=resp.content, text=text, tool_calls=calls, stop_reason=resp.stop_reason or "",
                 input_tokens=resp.usage.input_tokens + (resp.usage.cache_read_input_tokens or 0) + (resp.usage.cache_creation_input_tokens or 0),
                 output_tokens=resp.usage.output_tokens, model=resp.model)


def tool_results_message(results: list[dict]) -> dict:
    """All results of one round go back in a single user message, one result per tool call."""
    return {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": r["id"], "content": r["content"], "is_error": bool(r.get("is_error"))}
        for r in results]}


def assistant_message(reply: Reply) -> dict:
    return {"role": "assistant", "content": reply.content}
