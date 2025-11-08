"""Small pluggable LLM client with fallback summarization.

This module will try to use OpenAI if available and an API key is set.
Otherwise it falls back to a simple heuristic summarizer and a structured
reasoning stub suitable for local development and testing.
"""
from __future__ import annotations

import os
import re
from typing import Dict, Any, List

_HAS_OPENAI = False
try:
    import openai
    _HAS_OPENAI = True
except Exception:
    openai = None


def _sentences(text: str) -> List[str]:
    # naive sentence splitter
    s = re.split(r"(?<=[.!?])\s+", text.strip())
    return [x.strip() for x in s if x.strip()]


def summarize(text: str, max_sentences: int = 3) -> str:
    """Return a short summary of `text`.

    If OpenAI is available and OPENAI_API_KEY is set, it will use a chat
    completion. Otherwise returns the first `max_sentences` sentences.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if _HAS_OPENAI and api_key:
        try:
            openai.api_key = api_key
            prompt = (
                "Please provide a concise summary in plain text of the following content:\n\n" + text
            )
            resp = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=200)
            return resp.choices[0].text.strip()
        except Exception:
            # fallback to heuristic
            pass

    sents = _sentences(text)
    return " ".join(sents[:max_sentences])


def structured_reasoning(text: str) -> Dict[str, Any]:
    """Return a lightweight structured reasoning result.

    The structure is a dict with keys: summary (str), claims (list), evidence (list).
    If an LLM is available it will be used; otherwise a heuristic is returned.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if _HAS_OPENAI and api_key:
        try:
            openai.api_key = api_key
            prompt = (
                "Extract a short summary, 3 main claims, and evidence bullets from the text below.\n\n" + text
            )
            resp = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=500)
            raw = resp.choices[0].text.strip()
            return {"raw": raw}
        except Exception:
            pass

    # Heuristic structured output
    sents = _sentences(text)
    summary = " ".join(sents[:2]) if sents else ""
    claims = sents[2:5] if len(sents) > 2 else []
    evidence = [s for s in sents[5:8]] if len(sents) > 5 else []
    return {
        "summary": summary,
        "claims": claims,
        "evidence": evidence,
    }
