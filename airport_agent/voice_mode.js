// Voice mode: a full-screen view over the chat for spoken questions. It owns nothing about the agent - it only
// reflects what the page is doing: Listening (the recorder is on), Thinking (shows the agent's current step),
// Speaking (reads the short spoken summary), Ready (ask a follow-up or close). app.py loads this once into the page
// and calls window.__voice.speak / stop / heard / fail. The full answer, with tables, is always in the chat behind.
(() => {
  if (window.__voice && window.__voice.destroy) window.__voice.destroy();
  const synth = window.speechSynthesis;
  const $ = (sel) => document.querySelector(sel);
  const REC = '[data-testid="stChatInputCancelButton"]';      // present only while Streamlit's recorder is on
  const APPROVE = '[data-testid="stChatInputApproveButton"]';
  const MIC = '[data-testid="stChatInputMicButton"]';

  const style = document.createElement('style');
  style.textContent = `
#vm { position: fixed; inset: 0; z-index: 1000002; display: none; flex-direction: column; align-items: center;
      justify-content: center; gap: 1.1rem; padding: 2rem 1.5rem; color: #FFFFFF; text-align: center;
      background: radial-gradient(1100px 700px at 50% 32%, #172A52 0%, #0B1220 72%); }
#vm:not([data-s="off"]) { display: flex; animation: vm-in 0.25s ease; }
#vm .vm-you { min-height: 1.5rem; max-width: 640px; color: #9FB0CF; font-size: 1rem; }
#vm .vm-orb { position: relative; width: 176px; height: 176px; border-radius: 50%; margin: 0.6rem 0 2.6rem; display: flex;
              align-items: center; justify-content: center; gap: 8px; transition: background 0.4s ease, box-shadow 0.4s ease;
              background: radial-gradient(circle at 35% 30%, #8FB2FF, #2F63D6 55%, #173684);
              box-shadow: 0 0 70px rgba(70, 120, 255, 0.45); }
#vm .vm-orb i { display: block; width: 10px; border-radius: 6px; background: #FFFFFF; height: 18px; }
#vm .vm-orb i:nth-child(2), #vm .vm-orb i:nth-child(4) { height: 42px; }
#vm .vm-orb i:nth-child(3) { height: 64px; }
#vm[data-s="listening"] .vm-orb { animation: vm-breathe 1.6s ease-in-out infinite; }
#vm[data-s="listening"] .vm-orb::before, #vm[data-s="listening"] .vm-orb::after {
    content: ""; position: absolute; inset: 0; border-radius: 50%; border: 2px solid rgba(143, 178, 255, 0.6);
    animation: vm-ring 2s ease-out infinite; }
#vm[data-s="listening"] .vm-orb::after { animation-delay: 1s; }
#vm[data-s="thinking"] .vm-orb { background: radial-gradient(circle at 35% 30%, #FFE0A3, #E7A23A 55%, #99600F);
                                 box-shadow: 0 0 70px rgba(231, 162, 58, 0.40); }
#vm[data-s="thinking"] .vm-orb i { height: 14px; width: 14px; border-radius: 50%; animation: vm-dot 1.1s ease-in-out infinite; }
#vm[data-s="thinking"] .vm-orb i:nth-child(2) { animation-delay: 0.12s; }
#vm[data-s="thinking"] .vm-orb i:nth-child(3) { animation-delay: 0.24s; }
#vm[data-s="thinking"] .vm-orb i:nth-child(4) { animation-delay: 0.36s; }
#vm[data-s="thinking"] .vm-orb i:nth-child(5) { animation-delay: 0.48s; }
#vm[data-s="speaking"] .vm-orb { background: radial-gradient(circle at 35% 30%, #9FF0DC, #1FA88C 55%, #0C5F50);
                                 box-shadow: 0 0 70px rgba(31, 168, 140, 0.42); }
#vm[data-s="speaking"] .vm-orb i { animation: vm-talk 0.9s ease-in-out infinite; }
#vm[data-s="speaking"] .vm-orb i:nth-child(2) { animation-duration: 0.7s; animation-delay: 0.1s; }
#vm[data-s="speaking"] .vm-orb i:nth-child(3) { animation-duration: 1.1s; animation-delay: 0.2s; }
#vm[data-s="speaking"] .vm-orb i:nth-child(4) { animation-duration: 0.8s; animation-delay: 0.05s; }
#vm[data-s="speaking"] .vm-orb i:nth-child(5) { animation-duration: 1s; animation-delay: 0.15s; }
#vm[data-s="idle"] .vm-orb { background: radial-gradient(circle at 35% 30%, #7C8BA8, #3C4A66 55%, #1E2940); box-shadow: none; }
#vm .vm-state { font-size: 0.8rem; letter-spacing: 0.22em; text-transform: uppercase; color: #9FB0CF; }
#vm .vm-label { font-size: 1.35rem; font-weight: 600; max-width: 640px; min-height: 2rem; }
#vm .vm-cap { max-width: 660px; max-height: 12rem; overflow-y: auto; color: #C9D4EA; font-size: 1.05rem; line-height: 1.55; }
#vm .vm-btns { display: flex; gap: 1.1rem; align-items: center; margin-top: 0.8rem; min-height: 4.2rem; }
#vm button { font: inherit; cursor: pointer; border: none; color: inherit; }
#vm .vm-btn { display: none; align-items: center; justify-content: center; gap: 0.5rem; height: 4rem; min-width: 4rem;
              border-radius: 2rem; padding: 0 1.1rem; background: rgba(255, 255, 255, 0.12); transition: all 0.15s ease; }
#vm .vm-btn:hover { background: rgba(255, 255, 255, 0.22); }
#vm .vm-btn.main { background: #FFFFFF; color: #0B1220; padding: 0 1.5rem; font-weight: 600; }
#vm .vm-btn.main:hover { background: #DCE6FF; }
#vm .vm-btn svg, #vm .vm-x svg { width: 1.4rem; height: 1.4rem; fill: none; stroke: currentColor; stroke-width: 2.2;
                                 stroke-linecap: round; stroke-linejoin: round; }
#vm[data-s="listening"] [data-a="cancel"], #vm[data-s="listening"] [data-a="done"], #vm[data-s="speaking"] [data-a="stop"],
#vm[data-s="idle"] [data-a="mic"], #vm[data-s="idle"] [data-a="show"] { display: inline-flex; }
#vm .vm-hint { color: #7F90B2; font-size: 0.9rem; min-height: 1.3rem; }
#vm .vm-x { position: absolute; top: 1.1rem; right: 1.3rem; width: 2.75rem; height: 2.75rem; border-radius: 50%;
            background: rgba(255, 255, 255, 0.10); display: flex; align-items: center; justify-content: center; }
#vm .vm-x:hover { background: rgba(255, 255, 255, 0.22); }
@keyframes vm-in { from { opacity: 0; } to { opacity: 1; } }
@keyframes vm-breathe { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.06); } }
@keyframes vm-ring { from { transform: scale(1); opacity: 0.8; } to { transform: scale(1.5); opacity: 0; } }
@keyframes vm-dot { 0%, 100% { transform: translateY(0); opacity: 0.6; } 50% { transform: translateY(-12px); opacity: 1; } }
@keyframes vm-talk { 0%, 100% { transform: scaleY(0.4); } 50% { transform: scaleY(1.15); } }
@media (max-width: 640px) {
  #vm { gap: 0.8rem; padding: 4.5rem 1.25rem 1.5rem; }
  #vm .vm-orb { width: 132px; height: 132px; margin: 0.4rem 0 1.4rem; gap: 6px; }
  #vm .vm-orb i { width: 8px; height: 14px; }
  #vm .vm-orb i:nth-child(2), #vm .vm-orb i:nth-child(4) { height: 32px; }
  #vm .vm-orb i:nth-child(3) { height: 48px; }
  #vm .vm-label { font-size: 1.15rem; }
  #vm .vm-cap { font-size: 0.98rem; max-height: 34vh; }
  #vm .vm-btn { height: 3.5rem; min-width: 3.5rem; }
  #vm .vm-x { top: 0.75rem; right: 0.75rem; }
}
@keyframes vm-ring-small { from { transform: scale(1); opacity: 0.8; } to { transform: scale(1.35); opacity: 0; } }
@media (max-width: 640px) { #vm[data-s="listening"] .vm-orb::before, #vm[data-s="listening"] .vm-orb::after { animation-name: vm-ring-small; } }
@media (prefers-reduced-motion: reduce) { #vm *, #vm *::before, #vm *::after { animation: none !important; } }`;
  document.head.appendChild(style);

  const X = '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>';
  const el = document.createElement('div');
  el.id = 'vm';
  el.dataset.s = 'off';
  el.setAttribute('role', 'dialog');
  el.setAttribute('aria-label', 'Voice mode');
  el.innerHTML = `
    <button class="vm-x" data-a="close" aria-label="Close voice mode">${X}</button>
    <div class="vm-you"></div>
    <div class="vm-orb"><i></i><i></i><i></i><i></i><i></i></div>
    <div class="vm-state" aria-live="polite"></div>
    <div class="vm-label" aria-live="polite"></div>
    <div class="vm-cap"></div>
    <div class="vm-btns">
      <button class="vm-btn" data-a="cancel" aria-label="Cancel">${X}</button>
      <button class="vm-btn main" data-a="done"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>Done</button>
      <button class="vm-btn main" data-a="stop"><svg viewBox="0 0 24 24"><rect x="7" y="7" width="10" height="10" rx="1.5"/></svg>Stop</button>
      <button class="vm-btn main" data-a="mic"><svg viewBox="0 0 24 24"><path d="M5 10v4M9 7v10M12 4v16M15 7v10M19 10v4"/></svg>Ask another</button>
      <button class="vm-btn" data-a="show">Show full answer</button>
    </div>
    <div class="vm-hint"></div>`;
  document.body.appendChild(el);
  const part = (name) => el.querySelector('.vm-' + name);

  const TEXT = {
    listening: ['Listening', 'Ask your question', 'Tap Done when you have finished speaking'],
    thinking: ['Thinking', 'Transcribing your question', 'Every number is computed by code and checked before it is spoken'],
    speaking: ['Speaking', '', 'The full answer, with tables and sources, is in the chat'],
    idle: ['Ready', 'Ask a follow-up, or open the full answer', ''],
  };
  let state = 'off', token = 0;

  function set(next, label) {
    state = next;
    el.dataset.s = next;
    if (next === 'off') return;
    const [name, text, hint] = TEXT[next];
    part('state').textContent = name;
    part('label').textContent = label || text;
    part('hint').textContent = hint;
  }

  // ---- speech: one sentence at a time, so a long summary is never cut off and Stop takes effect at once ----
  function pickVoice() {
    const voices = synth.getVoices().filter((v) => /^en/i.test(v.lang));
    for (const p of [/Aria.*Natural/i, /Jenny.*Natural/i, /Natural/i, /Google US English/i, /Samantha/i]) {
      const v = voices.find((x) => p.test(x.name) && /en.US/i.test(x.lang)) || voices.find((x) => p.test(x.name));
      if (v) return v;
    }
    return null;
  }

  function stopSpeech() {
    token += 1;
    if (synth.speaking || synth.pending) synth.cancel();
  }

  function speak(text, inVoiceMode) {
    const wasBusy = synth.speaking || synth.pending;
    stopSpeech();
    const mine = token;
    const parts = text.split(/(?<=[.!?])\s+/).filter((p) => p.trim());
    if (inVoiceMode && state !== 'off') {
      part('cap').textContent = text;
      set('speaking');
    }
    let i = 0;
    const next = () => {
      if (mine !== token) return;
      if (i >= parts.length) {
        if (state === 'speaking') set('idle');
        return;
      }
      const u = new SpeechSynthesisUtterance(parts[i++]);
      const v = pickVoice();
      if (v) { u.voice = v; u.lang = v.lang; }
      u.rate = 1.0;
      u.onend = next;
      u.onerror = next;
      synth.speak(u);
    };
    // The voice list loads late on first use; and Chromium can swallow speech queued right after a cancel.
    const start = () => setTimeout(next, wasBusy ? 120 : 0);
    if (synth.getVoices().length) start();
    else {
      let started = false;
      const once = () => { if (!started) { started = true; start(); } };
      synth.addEventListener('voiceschanged', once, { once: true });
      setTimeout(once, 1000);
    }
  }

  // iPhone and iPad only speak when the first speech call comes straight from a tap. The answer arrives later, on its own,
  // so the first tap anywhere on the page says a silent word to unlock speech for the rest of the visit.
  // Safari counts a finger tap as a tap only when it ends (touchend, click), not when it starts.
  const TAP = ['touchend', 'click'];
  const unlock = () => {
    TAP.forEach((t) => document.removeEventListener(t, unlock, true));
    if (synth.speaking || synth.pending) return;
    const u = new SpeechSynthesisUtterance(' ');
    u.volume = 0;
    synth.speak(u);
  };
  TAP.forEach((t) => document.addEventListener(t, unlock, true));

  // ---- the page drives Listening and Thinking: watch the recorder and the agent's current step ----
  const timer = setInterval(() => {
    const recording = !!$(REC);
    if (recording && state !== 'listening') {
      stopSpeech();
      part('you').textContent = '';
      part('cap').textContent = '';
      set('listening');
    } else if (!recording && state === 'listening') {
      set('thinking');
    }
    if (state === 'thinking') {
      const steps = document.querySelectorAll('[class*="st-key-activity"] strong');
      const step = steps.length ? steps[steps.length - 1].textContent.trim() : '';
      if (step) part('label').textContent = step;
    }
  }, 200);

  function close() {
    const wasListening = state === 'listening';
    stopSpeech();
    set('off');
    if (wasListening && $(REC)) $(REC).click();
  }

  const actions = {
    close,
    cancel: close,
    show: close,
    done: () => { if ($(APPROVE)) $(APPROVE).click(); },
    stop: () => { stopSpeech(); set('idle'); },
    mic: () => { const b = $(MIC); if (b && !b.disabled) b.click(); },
  };
  el.addEventListener('click', (e) => {
    const b = e.target.closest('[data-a]');
    if (b) actions[b.dataset.a]();
  });
  const onKey = (e) => { if (e.key === 'Escape' && state !== 'off') close(); };
  document.addEventListener('keydown', onKey);

  window.__voice = {
    speak,
    stop: () => { stopSpeech(); if (state === 'speaking') set('idle'); },
    heard: (question) => { part('you').textContent = '“' + question + '”'; },
    fail: (message) => { if (state !== 'off') { part('cap').textContent = ''; set('idle', message); } },
    destroy: () => { clearInterval(timer); stopSpeech(); document.removeEventListener('keydown', onKey);
      TAP.forEach((t) => document.removeEventListener(t, unlock, true)); el.remove(); style.remove(); },
  };
})();
