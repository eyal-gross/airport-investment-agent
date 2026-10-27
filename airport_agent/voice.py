"""Voice layer. It wraps the agent and never touches it: speech -> text -> the same agent -> text -> speech.

- Speech to text runs locally with an open Whisper model (the `faster-whisper` package), so no second provider or key.
- Text to speech is done by the browser (the Web Speech API), reading a short spoken summary.
- If `faster-whisper` is not installed the chat simply shows no microphone.

Install:  it is part of requirements.txt
"""
import io
import re
from functools import lru_cache

MODEL_SIZE = "base.en"      # about 140 MB, downloaded once on first use; runs on CPU
# Words the recognizer should expect, so "Santa Ana" or "SFO" are not misheard.
VOCABULARY = ("Airport questions: terminal expansion, congestion, long-haul flights, unmet flight demand, load factor, "
              "New England, Los Angeles, LAX, Santa Ana, Anchorage, SFO, San Francisco, Oakland, Boston, Burlington, Memphis, "
              "LaGuardia, JFK, Newark, Denver, Portland, Providence.")


def available() -> bool:
    try:
        import faster_whisper  # noqa: F401
        return True
    except Exception:
        return False


@lru_cache(maxsize=1)
def _model():
    from faster_whisper import WhisperModel
    return WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")


def _wav_to_samples(audio_bytes: bytes):
    """WAV bytes -> mono float samples at 16 kHz (what the model expects). Decoded here with the standard
    library, so no audio codec package is needed."""
    import wave

    import numpy as np
    with wave.open(io.BytesIO(audio_bytes), "rb") as w:
        rate, channels, width = w.getframerate(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(w.getnframes())
    if width not in (1, 2, 4):
        raise ValueError(f"unsupported WAV sample width: {width} bytes")
    dtype = {1: np.uint8, 2: np.int16, 4: np.int32}[width]
    x = np.frombuffer(raw, dtype=dtype).astype(np.float32)
    x = (x - 128) / 128 if width == 1 else x / float(2 ** (8 * width - 1))
    if channels > 1:
        x = x.reshape(-1, channels).mean(axis=1)
    if rate != 16000 and len(x):
        n = int(len(x) * 16000 / rate)
        x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
    return x


def transcribe(audio_bytes: bytes) -> str:
    """Recorded audio (WAV bytes from the browser) -> the question as text."""
    segments, _ = _model().transcribe(_wav_to_samples(audio_bytes), language="en", initial_prompt=VOCABULARY,
                                      vad_filter=True, beam_size=5)
    return " ".join(s.text.strip() for s in segments).strip()


def spoken_summary(answer_text: str, max_chars: int = 420) -> str:
    """What gets read aloud: the lead of the answer (the model is told to answer first), with markdown removed.
    Built by code from the checked answer, so nothing new is said that was not written."""
    text = re.sub(r"\|.*\|", " ", answer_text)                 # tables are for the eyes
    text = re.sub(r"[*_`#>]", "", text)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip() and not p.strip().startswith("-")]
    out = ""
    for sentence in re.split(r"(?<=[.!?])\s+", " ".join(paragraphs[:2])):
        if len(out) + len(sentence) > max_chars:
            break
        out += sentence + " "
    out = out.strip() or text.strip()[:max_chars]
    return re.sub(r"\s+", " ", out) + " The details, warnings and confidence are on screen."
