"""The voice wrapper's pure parts: the spoken summary and WAV decoding. (Transcription itself needs the optional
Whisper model and is not run here.)"""
import io
import math
import struct
import wave

import pytest

from airport_agent import safeguards as S
from airport_agent import voice

ANSWER = ("**Los Angeles International (LAX) is more congested than Santa Ana (SNA), but not by much.** "
          "LAX's system delay rate is 4.8% against 3.9%.\n\n"
          "| Measure | LAX | SNA |\n|---|---|---|\n| System delay rate | 4.8% | 3.9% |\n\n"
          "- **SNA is legally capped.**\n\nI can also show month-by-month trends.")


def test_spoken_summary_is_the_lead_without_markdown_or_tables():
    spoken = voice.spoken_summary(ANSWER)
    assert spoken.startswith("Los Angeles International (LAX) is more congested")
    assert "|" not in spoken and "*" not in spoken
    assert spoken.endswith("on screen.")


def test_spoken_summary_says_nothing_that_was_not_written():
    data = S.numbers_in_data(ANSWER)
    assert S.unverified_numbers(voice.spoken_summary(ANSWER), data) == []


def test_spoken_summary_is_short():
    assert len(voice.spoken_summary("A long sentence about airports. " * 100)) < 520


def test_wav_decoding_resamples_to_16k_mono():
    pytest.importorskip("numpy")
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000)
        frames = b"".join(struct.pack("<hh", int(8000 * math.sin(i / 20)), int(8000 * math.sin(i / 20))) for i in range(48000))
        w.writeframes(frames)
    x = voice._wav_to_samples(buf.getvalue())
    assert len(x) == 16000 and abs(float(x.max())) <= 1.0
