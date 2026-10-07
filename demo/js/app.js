/**
 * NetGuard: Live Cognitive AI Application Controller
 * Connects to live Python backend (/api/...) running real Random Forest
 * model and persistent memory, with real-time terminal streaming.
 * Includes Interactive Step-by-Step Defense Presentation Stepper.
 */

class SoundEffects {
  constructor() {
    this.enabled = true;
    this.ctx = null;
  }

  init() {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) this.ctx = new AudioContext();
    }
  }

  playTone(freq = 440, type = "sine", duration = 0.1, gainVal = 0.05) {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx || this.ctx.state === "suspended") this.ctx && this.ctx.resume();
    try {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      gain.gain.setValueAtTime(gainVal, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + duration);
    } catch (e) {}
  }

  step() { this.playTone(600, "triangle", 0.06, 0.04); }
  route() { this.playTone(480, "sine", 0.08, 0.04); }
  escalate() {
    this.playTone(880, "square", 0.12, 0.06);
    setTimeout(() => this.playTone(1174, "sine", 0.25, 0.08), 100);
  }
}

class NetGuardApp {
  constructor() {
    this.sound = new SoundEffects();
    this.localEngine = new CognitivePipeline();
    this.isStreaming = false;
    this.streamTimer = null;
    this.backendOnline = false;

    // Defense Stepper State
    this.currentData = null;
    this.currentHop = 1;
    this.isAutoPlay = false;
    this.autoPlayTimer = null;

    this.initDOM();
    this.bindEvents();
    this.checkBackend();

    // Ensure cables connect accurately as layout completes
    setTimeout(() => this.updateTopologyWires(), 80);
    setTimeout(() => this.updateTopologyWires(), 350);
    setTimeout(() => this.updateTopologyWires(), 800);
  }

  initDOM() {
    // Controls
    this.btnStreamToggle = document.getElementById("btn-stream-toggle");
    this.btnStreamStep = document.getElementById("btn-stream-step");
    this.btnAudio = document.getElementById("btn-audio");

    // Attack triggers
    this.btnInjNormal = document.getElementById("btn-inj-normal");
    this.btnInjNeptune = document.getElementById("btn-inj-neptune");
    this.btnInjBack = document.getElementById("btn-inj-back");
    this.btnInjSweep = document.getElementById("btn-inj-sweep");
    this.btnResetMemoryTop = document.getElementById("btn-reset-memory-top");

    // Defense Stepper Controller
    this.btnHopPrev = document.getElementById("btn-hop-prev");
    this.btnHopNext = document.getElementById("btn-hop-next");
    this.btnHopAuto = document.getElementById("btn-hop-auto");
    this.stepperModeLabel = document.getElementById("stepper-mode-label");
    this.stepNodes = {
      1: document.getElementById("step-node-1"),
      2: document.getElementById("step-node-2"),
      3: document.getElementById("step-node-3"),
      4: document.getElementById("step-node-4"),
      5: document.getElementById("step-node-5")
    };

    // Live Flash Alert Banner (Instant Above-The-Fold Verdict)
    this.liveFlashBanner = document.getElementById("live-flash-banner");
    this.flashHeadline = document.getElementById("flash-headline");
    this.flashDetails = document.getElementById("flash-details");
    this.flashVerdictBadge = document.getElementById("flash-verdict-badge");
    this.flashIcon = document.getElementById("flash-icon");

    // Canvas, Packet Token & Label
    this.topologyCanvas = document.getElementById("topology-canvas");
    this.packetToken = document.getElementById("packet-token");
    this.tokenLabel = document.getElementById("token-label");

    // Network Multi-PC Canvas Nodes
    this.sourceNodes = {
      pc1: document.getElementById("node-pc1"),
      pc2: document.getElementById("node-pc2"),
      pc3: document.getElementById("node-pc3"),
      attacker: document.getElementById("node-attacker")
    };
    this.targetNodes = {
      web: document.getElementById("node-target"),
      ftp: document.getElementById("node-srv-ftp"),
      db: document.getElementById("node-srv-db"),
      soc: document.getElementById("node-soc")
    };
    this.nodes = {
      router: document.getElementById("node-router"),
      cognitive: document.getElementById("node-cognitive"),
      firewall: document.getElementById("node-firewall")
    };

    // 10 Permanent Network Cables (Cisco Packet Tracer Style)
    this.cables = {
      pc1: document.getElementById("cable-pc1"),
      pc2: document.getElementById("cable-pc2"),
      pc3: document.getElementById("cable-pc3"),
      attacker: document.getElementById("cable-attacker"),
      routerCog: document.getElementById("cable-router-cog"),
      cogFw: document.getElementById("cable-cog-fw"),
      fwWeb: document.getElementById("cable-fw-web"),
      fwFtp: document.getElementById("cable-fw-ftp"),
      fwDb: document.getElementById("cable-fw-db"),
      fwSoc: document.getElementById("cable-fw-soc")
    };

    // Telemetry
    this.telProto = document.getElementById("tel-proto");
    this.telService = document.getElementById("tel-service");
    this.telFlag = document.getElementById("tel-flag");
    this.telSrcBytes = document.getElementById("tel-srcbytes");
    this.telDstBytes = document.getElementById("tel-dstbytes");
    this.telProb = document.getElementById("tel-prob");
    this.telRisk = document.getElementById("tel-risk");
    this.stageStatus = document.getElementById("stage-status-text");
    this.packetTelemetryBar = document.querySelector(".packet-telemetry-bar");

    // Verdict Box
    this.baseRiskPill = document.getElementById("base-risk-pill");
    this.finalRiskPill = document.getElementById("final-risk-pill");
    this.escalationIndicator = document.getElementById("escalation-indicator");
    this.reasoningText = document.getElementById("reasoning-text");
    this.reasoningTitle = document.getElementById("reasoning-title");
    this.actionTriggerVal = document.getElementById("action-trigger-val");
    this.groundTruthBadge = document.getElementById("ground-truth-badge");

    // Dashboard Cards for Focus Highlighting
    this.cardVerdictShowcase = document.getElementById("card-verdict-showcase");
    this.cardPerceptionAttention = document.getElementById("card-perception-attention");
    this.cardContextualMemory = document.getElementById("card-contextual-memory");
    this.cardTerminalConsole = document.getElementById("card-terminal-console");

    // Panels
    this.attentionBarsContainer = document.getElementById("attention-bars");
    this.dequeSlotsContainer = document.getElementById("deque-slots");
    this.ltmMatchesList = document.getElementById("ltm-matches-list");
    this.ltmMatchBadge = document.getElementById("ltm-match-badge");
    this.terminalBody = document.getElementById("terminal-logs");
    this.btnClearTerminal = document.getElementById("btn-clear-terminal");
    this.backendStatusLabel = document.getElementById("backend-status-label");
  }

  bindEvents() {
    if (this.btnStreamToggle) this.btnStreamToggle.addEventListener("click", () => this.toggleStream());
    if (this.btnStreamStep) this.btnStreamStep.addEventListener("click", () => this.fetchNextPacket());

    if (this.btnInjNormal) this.btnInjNormal.addEventListener("click", () => this.injectAttack("normal"));
    if (this.btnInjNeptune) this.btnInjNeptune.addEventListener("click", () => this.injectAttack("neptune"));
    if (this.btnInjBack) this.btnInjBack.addEventListener("click", () => this.injectAttack("apache_back"));
    if (this.btnInjSweep) this.btnInjSweep.addEventListener("click", () => this.injectAttack("portsweep"));

    if (this.btnResetMemoryTop) {
      this.btnResetMemoryTop.addEventListener("click", () => this.resetMemory());
    }

    if (this.btnClearTerminal) {
      this.btnClearTerminal.addEventListener("click", () => {
        this.terminalBody.innerHTML = "";
        this.appendLog("terminal", "Logs cleared.");
      });
    }

    if (this.btnAudio) {
      this.btnAudio.addEventListener("click", () => {
        this.sound.enabled = !this.sound.enabled;
        this.btnAudio.classList.toggle("active", this.sound.enabled);
        this.btnAudio.innerHTML = this.sound.enabled ? "🔊" : "🔇";
      });
    }

    // Defense Stepper Actions
    if (this.btnHopPrev) this.btnHopPrev.addEventListener("click", () => this.prevHop());
    if (this.btnHopNext) this.btnHopNext.addEventListener("click", () => this.nextHop());
    if (this.btnHopAuto) this.btnHopAuto.addEventListener("click", () => this.toggleAutoPlay());

    // Direct Clicking on any of the 5 Stepper Pills
    Object.entries(this.stepNodes).forEach(([hopNum, el]) => {
      if (el) {
        el.addEventListener("click", () => {
          this.setHop(parseInt(hopNum, 10));
        });
      }
    });

    // Keyboard Shortcuts: Spacebar / ArrowRight = Next Hop, ArrowLeft = Prev Hop
    window.addEventListener("keydown", (e) => {
      if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
      if (e.code === "Space" || e.code === "ArrowRight") {
        e.preventDefault();
        this.nextHop();
      } else if (e.code === "ArrowLeft") {
        e.preventDefault();
        this.prevHop();
      }
    });

    // Direct Interactive Node Clicks (Packet Tracer Style)
    if (this.sourceNodes.pc1) this.sourceNodes.pc1.addEventListener("click", () => this.injectAttack("normal"));
    if (this.sourceNodes.pc2) this.sourceNodes.pc2.addEventListener("click", () => this.injectAttack("normal"));
    if (this.sourceNodes.pc3) this.sourceNodes.pc3.addEventListener("click", () => this.fetchNextPacket());
    if (this.sourceNodes.attacker) this.sourceNodes.attacker.addEventListener("click", () => this.injectAttack("apache_back"));

    window.addEventListener("resize", () => this.updateTopologyWires());
    window.addEventListener("load", () => this.updateTopologyWires());
  }

  async checkBackend() {
    try {
      const res = await fetch("/api/memory");
      if (res.ok) {
        this.backendOnline = true;
        if (this.backendStatusLabel) this.backendStatusLabel.textContent = "BACKEND: PYTHON MODEL ONLINE";
        this.appendLog("system", "Connected to live Python backend server.");
        // Initial run: show the star Apache Back scenario on load!
        this.injectAttack("apache_back");
      } else {
        throw new Error();
      }
    } catch (e) {
      this.backendOnline = false;
      if (this.backendStatusLabel) this.backendStatusLabel.textContent = "BROWSER SIMULATION ENGINE";
      this.appendLog("system", "Running browser simulation engine.");
      this.injectAttack("apache_back");
    }
  }

  async fetchNextPacket() {
    if (this.backendOnline) {
      try {
        const res = await fetch("/api/stream/next");
        if (!res.ok) throw new Error();
        const data = await res.json();
        this.renderResult(data);
      } catch (e) {
        this.fallbackNextPacket();
      }
    } else {
      this.fallbackNextPacket();
    }
  }

  fallbackNextPacket() {
    const scens = NETGUARD_DATA.scenarios;
    const randomScen = scens[Math.floor(Math.random() * scens.length)];
    const result = this.localEngine.process(randomScen.rawInput, {
      customProbability: randomScen.modelPrediction.probability
    });

    const data = {
      event_id: result.eventId,
      timestamp: new Date().toLocaleTimeString(),
      raw_record: randomScen.rawInput,
      attention: result.attention.topFeatures.map(f => ({
        feature: f.feature,
        importance: f.importance,
        val: f.rawValue
      })),
      probability: result.aiModel.probability,
      prediction: result.aiModel.prediction,
      previous_similar_count: result.memory.similarCount,
      previous_similar_events: result.memory.similarAnomalies,
      base_risk: result.inference.baseRisk,
      final_risk: result.inference.finalRisk,
      escalated: result.inference.escalated,
      fired_rules: result.inference.firedRules,
      recommendation: result.inference.recommendation,
      security_action: result.inference.securityAction,
      logs: [
        `[INGRESS] Ingress packet: ${randomScen.rawInput.protocol_type.toUpperCase()}/${randomScen.rawInput.service} (Flag: ${randomScen.rawInput.flag})`,
        `[PERCEPTION] Standardized 41 features into continuous vector space.`,
        `[ATTENTION] Top focus: src_bytes, dst_bytes, flag. Suppressed noise.`,
        `[ML MODEL] Random Forest predicted: ${result.aiModel.prediction} (Prob: ${result.aiModel.probability.toFixed(4)})`,
        `[MEMORY QUERY] Searched Long-Term store: Found ${result.memory.similarCount} previous matching anomalies.`,
        result.inference.escalated
          ? `[RULE K4 TRIGGERED] Verified Anomaly + History >= 2: Escalating ${result.inference.baseRisk} ➔ ${result.inference.finalRisk}!`
          : `[RULE ${result.inference.firedRules.join(", ")}] Evaluated risk: ${result.inference.finalRisk}`,
        `[ACTION ENFORCED] ${result.inference.securityAction}`
      ]
    };
    this.renderResult(data);
  }

  async injectAttack(attackId) {
    if (this.backendOnline) {
      try {
        const res = await fetch(`/api/inject/${attackId}`, { method: "POST" });
        if (!res.ok) throw new Error();
        const data = await res.json();
        this.renderResult(data);
      } catch (e) {
        this.fallbackInjectAttack(attackId);
      }
    } else {
      this.fallbackInjectAttack(attackId);
    }
  }

  fallbackInjectAttack(attackId) {
    let scen = NETGUARD_DATA.scenarios[2];
    if (attackId === "normal") scen = NETGUARD_DATA.scenarios[0];
    else if (attackId === "neptune") scen = NETGUARD_DATA.scenarios[1];
    else if (attackId === "portsweep") scen = NETGUARD_DATA.scenarios[3];

    if (scen.seedMemoryRequired) this.localEngine.longTermMemory.seedDefaults();

    const result = this.localEngine.process(scen.rawInput, {
      customProbability: scen.modelPrediction.probability
    });

    this.renderResult({
      event_id: result.eventId,
      timestamp: new Date().toLocaleTimeString(),
      raw_record: scen.rawInput,
      attention: result.attention.topFeatures.map(f => ({
        feature: f.feature,
        importance: f.importance,
        val: f.rawValue
      })),
      probability: result.aiModel.probability,
      prediction: result.aiModel.prediction,
      previous_similar_count: result.memory.similarCount,
      previous_similar_events: result.memory.similarAnomalies,
      base_risk: result.inference.baseRisk,
      final_risk: result.inference.finalRisk,
      escalated: result.inference.escalated,
      fired_rules: result.inference.firedRules,
      recommendation: result.inference.recommendation,
      security_action: result.inference.securityAction,
      logs: [
        `[INGRESS] Injected attack: ${scen.title} (${scen.rawInput.protocol_type.toUpperCase()}/${scen.rawInput.service})`,
        `[PERCEPTION] Encoded & scaled NSL-KDD 41-dim vector.`,
        `[ATTENTION] Top feature ranking computed.`,
        `[ML MODEL] Random Forest probability = ${result.aiModel.probability.toFixed(4)}`,
        `[MEMORY QUERY] Matched ${result.memory.similarCount} prior incidents in Long-Term Memory.`,
        result.inference.escalated
          ? `[RULE K4 TRIGGERED] Repetition detected! Risk upgraded: ${result.inference.baseRisk} ➔ ${result.inference.finalRisk}`
          : `[RULE ${result.inference.firedRules.join(", ")}] Final Risk: ${result.inference.finalRisk}`,
        `[ACTION ENFORCED] ${result.inference.securityAction}`
      ]
    });
  }

  async resetMemory() {
    if (this.backendOnline) {
      try {
        await fetch("/api/memory/reset", { method: "POST" });
        this.appendLog("memory", "Long-Term Memory reset on server.");
        this.showToast("Memory cleared.");
      } catch (e) {}
    } else {
      this.localEngine.longTermMemory.clear();
      this.showToast("Memory cleared.");
    }
    if (this.ltmMatchesList) this.ltmMatchesList.innerHTML = "<div style='font-size:0.7rem; color:var(--text-dim); padding:6px;'>Memory is empty.</div>";
    if (this.ltmMatchBadge) this.ltmMatchBadge.textContent = "0 Matches";
  }

  toggleStream() {
    this.isStreaming = !this.isStreaming;
    if (this.isStreaming) {
      this.btnStreamToggle.innerHTML = "<span>⏸️</span> Pause Stream";
      this.btnStreamToggle.classList.add("running");
      this.runStream();
    } else {
      this.btnStreamToggle.innerHTML = "<span>▶️</span> Start Live Stream";
      this.btnStreamToggle.classList.remove("running");
      if (this.streamTimer) clearTimeout(this.streamTimer);
    }
  }

  runStream() {
    if (!this.isStreaming) return;
    this.fetchNextPacket();
    this.streamTimer = setTimeout(() => {
      this.runStream();
    }, 2800);
  }

  renderResult(data) {
    this.currentData = data;
    const raw = data.raw_record;

    // 1. Instant Above-The-Fold Flash Alert Card
    if (this.liveFlashBanner) {
      const isThreat = data.final_risk === "HIGH" || data.final_risk === "CRITICAL";
      const cardType = data.escalated ? "escalation" : (data.final_risk === "LOW" ? "normal" : "threat");
      this.liveFlashBanner.className = `live-flash-card ${cardType}`;

      if (data.escalated) {
        if (this.flashIcon) this.flashIcon.textContent = "⚡";
        if (this.flashHeadline) {
          this.flashHeadline.innerHTML = `[COGNITIVE MEMORY ESCALATION ACTIVE] &bull; ${raw.service.toUpperCase()} Traffic (${raw.protocol_type.toUpperCase()}, Flag: ${raw.flag})`;
        }
        if (this.flashDetails) {
          this.flashDetails.innerHTML = `ML Model output: <b>P=${(data.probability * 100).toFixed(1)}% (${data.base_risk})</b> &bull; Long-Term Memory matched <b>${data.previous_similar_count} prior incidents</b> &bull; Rule K4 Escalated: <b style="color:#d8b4fe;">${data.base_risk} ➔ ${data.final_risk}</b> &bull; Action: <b>${data.security_action}</b>`;
        }
        if (this.flashVerdictBadge) {
          this.flashVerdictBadge.textContent = "HIGH THREAT (ESCALATED)";
          this.flashVerdictBadge.className = "flash-verdict-badge high";
        }
      } else if (data.final_risk === "LOW") {
        if (this.flashIcon) this.flashIcon.textContent = "🛡️";
        if (this.flashHeadline) {
          this.flashHeadline.innerHTML = `[AUTHORIZED NETWORK TRAFFIC] &bull; ${raw.service.toUpperCase()} (${raw.protocol_type.toUpperCase()}, Flag: ${raw.flag})`;
        }
        if (this.flashDetails) {
          this.flashDetails.innerHTML = `ML Confidence: <b>P=${(data.probability * 100).toFixed(1)}% (NORMAL)</b> &bull; Memory Context: Benign flow verified &bull; Action: <b>${data.security_action}</b>`;
        }
        if (this.flashVerdictBadge) {
          this.flashVerdictBadge.textContent = "BENIGN / NORMAL (PASSED)";
          this.flashVerdictBadge.className = "flash-verdict-badge low";
        }
      } else {
        if (this.flashIcon) this.flashIcon.textContent = "🚨";
        if (this.flashHeadline) {
          this.flashHeadline.innerHTML = `[HIGH THREAT DETECTED] &bull; ${raw.service.toUpperCase()} (${raw.protocol_type.toUpperCase()}, Flag: ${raw.flag})`;
        }
        if (this.flashDetails) {
          this.flashDetails.innerHTML = `ML Probability: <b>P=${(data.probability * 100).toFixed(1)}% (${data.prediction})</b> &bull; Rule: <b>${data.fired_rules.join(", ")}</b> &bull; Action: <b>${data.security_action}</b>`;
        }
        if (this.flashVerdictBadge) {
          this.flashVerdictBadge.textContent = `${data.final_risk} THREAT DETECTED`;
          this.flashVerdictBadge.className = `flash-verdict-badge ${data.final_risk.toLowerCase()}`;
        }
      }

      this.liveFlashBanner.style.animation = "none";
      void this.liveFlashBanner.offsetHeight;
      this.liveFlashBanner.style.animation = "flashPulse 0.4s ease";
    }

    // 2. Telemetry Bar
    if (this.telProto) this.telProto.textContent = raw.protocol_type.toUpperCase();
    if (this.telService) this.telService.textContent = raw.service;
    if (this.telFlag) this.telFlag.textContent = raw.flag;
    if (this.telSrcBytes) this.telSrcBytes.textContent = Number(raw.src_bytes).toLocaleString();
    if (this.telDstBytes) this.telDstBytes.textContent = Number(raw.dst_bytes).toLocaleString();
    if (this.telProb) this.telProb.textContent = `${(data.probability * 100).toFixed(1)}%`;
    if (this.telRisk) {
      this.telRisk.textContent = data.final_risk;
      this.telRisk.className = `telemetry-value ${data.final_risk.toLowerCase()}`;
    }

    // 3. Verdict Box
    if (this.baseRiskPill) {
      this.baseRiskPill.textContent = data.base_risk;
      this.baseRiskPill.className = `risk-pill ${data.base_risk.toLowerCase()}`;
    }
    if (this.finalRiskPill) {
      this.finalRiskPill.textContent = data.final_risk;
      this.finalRiskPill.className = `risk-pill ${data.final_risk.toLowerCase()}`;
    }
    if (this.escalationIndicator) {
      this.escalationIndicator.style.display = data.escalated ? "flex" : "none";
    }
    if (this.groundTruthBadge) {
      this.groundTruthBadge.textContent = `Truth: ${raw.label || data.prediction}`;
    }

    if (data.escalated) {
      if (this.reasoningTitle) this.reasoningTitle.textContent = "⚡ Cognitive Memory Escalation Active (Rule K4)";
      if (this.reasoningText) {
        this.reasoningText.textContent = `The standalone Random Forest model produced a borderline probability of ${(data.probability * 100).toFixed(1)}% (Medium). Long-term memory identified ${data.previous_similar_count} previous identical anomalies on (${raw.protocol_type}/${raw.service}). Rule K4 dynamically escalated the risk priority to HIGH!`;
      }
    } else {
      if (this.reasoningTitle) this.reasoningTitle.textContent = "Standard Cognitive Evaluation";
      if (this.reasoningText) {
        this.reasoningText.textContent = `Random Forest model evaluated packet with probability ${(data.probability * 100).toFixed(1)}%. Rule ${data.fired_rules.join(", ")} matched. Memory check returned ${data.previous_similar_count} prior incidents (no escalation needed).`;
      }
    }

    if (this.actionTriggerVal) this.actionTriggerVal.textContent = data.security_action;

    // 4. Attention Bars
    if (this.attentionBarsContainer) {
      this.attentionBarsContainer.innerHTML = "";
      (data.attention || []).forEach((feat) => {
        const item = document.createElement("div");
        item.className = "att-item";
        item.innerHTML = `
          <div class="att-labels">
            <span class="att-feat-name">${feat.feature} (Val: ${feat.val})</span>
            <span class="att-val-pct">Weight: ${(feat.importance * 100).toFixed(1)}%</span>
          </div>
          <div class="att-progress-track">
            <div class="att-progress-fill" style="width: ${Math.min(100, feat.importance * 450)}%"></div>
          </div>
        `;
        this.attentionBarsContainer.appendChild(item);
      });
    }

    // 5. Memory status
    if (this.ltmMatchBadge) {
      this.ltmMatchBadge.textContent = `${data.previous_similar_count} Matches in History`;
    }
    if (this.ltmMatchesList) {
      this.ltmMatchesList.innerHTML = "";
      if (data.previous_similar_count === 0) {
        this.ltmMatchesList.innerHTML = "<div style='font-size:0.7rem; color:var(--text-dim); padding:4px;'>No historical threat matches.</div>";
      } else {
        (data.previous_similar_events || []).forEach(evt => {
          const row = document.createElement("div");
          row.className = "event-card-mini match-found";
          row.innerHTML = `
            <span><b>${evt.event_id}</b> (${evt.protocol_type}/${evt.service})</span>
            <span style="color:#d8b4fe;">P: ${(evt.probability * 100).toFixed(0)}% | ${evt.final_risk}</span>
          `;
          this.ltmMatchesList.appendChild(row);
        });
      }
    }

    // 6. Short-term deque slots
    if (this.dequeSlotsContainer) {
      this.dequeSlotsContainer.innerHTML = "";
      for (let i = 0; i < 5; i++) {
        const slot = document.createElement("div");
        if (i === 0) {
          slot.className = "deque-slot occupied newest";
          slot.textContent = `${raw.protocol_type}/${raw.service}`;
        } else {
          slot.className = "deque-slot";
          slot.textContent = `Slot ${i + 1}`;
        }
        this.dequeSlotsContainer.appendChild(slot);
      }
    }

    // 7. Initialize Defense Stepper
    if (this.isAutoPlay) {
      this.setHop(1);
      if (this.autoPlayTimer) clearTimeout(this.autoPlayTimer);
      this.autoPlayTimer = setTimeout(() => this.runAutoPlayHop(), 900);
    } else {
      // Manual Mode: Start at Hop 1 and wait for professor defense stepping!
      this.setHop(1);
    }
  }

  setHop(hopNum) {
    if (!this.currentData) return;
    this.currentHop = Math.max(1, Math.min(5, hopNum));
    const data = this.currentData;
    const raw = data.raw_record;
    const isThreat = data.final_risk === "HIGH" || data.final_risk === "CRITICAL";

    // 1. Update Stepper Pills UI
    Object.entries(this.stepNodes).forEach(([numStr, el]) => {
      const num = parseInt(numStr, 10);
      if (!el) return;
      el.classList.remove("active", "completed");
      if (num === this.currentHop) {
        el.classList.add("active");
      } else if (num < this.currentHop) {
        el.classList.add("completed");
      }
    });

    // 2. Clear Card Focus Highlights
    [
      this.cardVerdictShowcase,
      this.cardPerceptionAttention,
      this.cardContextualMemory,
      this.cardTerminalConsole,
      this.packetTelemetryBar
    ].forEach(c => c && c.classList.remove("layer-card-focus", "threat", "cognitive"));

    // 3. Clear active states on nodes and cables
    Object.values(this.sourceNodes).forEach(n => n && n.classList.remove("active", "threat"));
    Object.values(this.targetNodes).forEach(n => n && n.classList.remove("active", "threat"));
    Object.values(this.nodes).forEach(n => n && n.classList.remove("active", "threat"));
    Object.values(this.cables).forEach(c => c && c.classList.remove("active", "threat-active"));

    // Determine Source & Target Nodes
    let srcNode = this.sourceNodes.pc1;
    let srcCable = this.cables.pc1;
    let srcName = "PC-01 (Finance)";

    if (isThreat) {
      srcNode = this.sourceNodes.attacker;
      srcCable = this.cables.attacker;
      srcName = "Attacker (WAN)";
    } else if (raw.service === "ftp" || raw.service === "ftp_data") {
      srcNode = this.sourceNodes.pc2;
      srcCable = this.cables.pc2;
      srcName = "PC-02 (Dev Eng)";
    } else if (raw.src_bytes > 5000) {
      srcNode = this.sourceNodes.pc3;
      srcCable = this.cables.pc3;
      srcName = "PC-03 (Branch)";
    }

    let tgtNode = this.targetNodes.web;
    let tgtCable = this.cables.fwWeb;
    let tgtName = "SRV-Web (HTTP)";

    if (isThreat) {
      tgtNode = this.targetNodes.soc;
      tgtCable = this.cables.fwSoc;
      tgtName = "SOC Quarantine Room";
    } else if (raw.service === "ftp" || raw.service === "ftp_data") {
      tgtNode = this.targetNodes.ftp;
      tgtCable = this.cables.fwFtp;
      tgtName = "SRV-Storage (FTP)";
    } else if (raw.service === "private" || raw.service === "sql") {
      tgtNode = this.targetNodes.db;
      tgtCable = this.cables.fwDb;
      tgtName = "SRV-Database";
    }

    this.updateTopologyWires();
    if (this.packetToken) this.packetToken.classList.toggle("threat", isThreat);

    // 4. Handle Each Specific Hop
    if (this.currentHop === 1) {
      // HOP 1: Ingress Source (LAN / Attacker)
      srcNode.classList.add("active");
      if (isThreat) srcNode.classList.add("threat");
      if (srcCable) srcCable.classList.add(isThreat ? "threat-active" : "active");
      this.moveTokenToNode(srcNode);

      if (this.tokenLabel) {
        this.tokenLabel.textContent = isThreat ? `🚨 ${raw.label || "Threat Source"}` : `📦 ${raw.service}`;
      }
      if (this.stageStatus) {
        this.stageStatus.innerHTML = `👉 [HOP 1/5: INGRESS SOURCE] Ingress packet generated at <b>${srcName}</b> (${raw.protocol_type.toUpperCase()}/${raw.service}, Flag: ${raw.flag}). Click "STEP NEXT HOP" or press Spacebar.`;
      }
      if (this.packetTelemetryBar) {
        this.packetTelemetryBar.classList.add("layer-card-focus");
      }
      this.appendLog("ingress", `[INGRESS] Transmitting from ${srcName}: ${raw.protocol_type.toUpperCase()}/${raw.service} (Flag: ${raw.flag})`);
      this.sound.step();

    } else if (this.currentHop === 2) {
      // HOP 2: Ingress Edge Router (Perception & Attention)
      this.nodes.router.classList.add("active");
      if (srcCable) srcCable.classList.add(isThreat ? "threat-active" : "active");
      if (this.cables.routerCog) this.cables.routerCog.classList.add(isThreat ? "threat-active" : "active");
      this.moveTokenToNode(this.nodes.router);

      if (this.tokenLabel) this.tokenLabel.textContent = "📡 Router (Perception)";
      if (this.stageStatus) {
        this.stageStatus.innerHTML = `👉 [HOP 2/5: PERCEPTION & ATTENTION] Core Router standardizes 41 features into dense vector (StandardScaler) & Attention filters top signals.`;
      }
      if (this.cardPerceptionAttention) {
        this.cardPerceptionAttention.classList.add("layer-card-focus");
      }
      this.appendLog("perception", `[PERCEPTION] Encoded 41 categorical & continuous features -> Dense Vector (1, 41)`);
      this.appendLog("attention", `[ATTENTION] Top focus: src_bytes, dst_bytes, flag. Suppressed 36 noisy attributes.`);
      this.sound.route();

    } else if (this.currentHop === 3) {
      // HOP 3: NetGuard Core (Cognitive Brain, ML Model, Memory)
      this.nodes.cognitive.classList.add("active");
      if (data.escalated) this.nodes.cognitive.classList.add("threat");
      if (this.cables.routerCog) this.cables.routerCog.classList.add(isThreat ? "threat-active" : "active");
      if (this.cables.cogFw) this.cables.cogFw.classList.add(isThreat ? "threat-active" : "active");
      this.moveTokenToNode(this.nodes.cognitive);

      if (this.tokenLabel) {
        this.tokenLabel.textContent = data.escalated
          ? `⚡ K4: P=${(data.probability * 100).toFixed(0)}% ➔ HIGH!`
          : `🧠 RF: ${(data.probability * 100).toFixed(0)}% (${data.base_risk})`;
      }
      if (this.stageStatus) {
        this.stageStatus.innerHTML = data.escalated
          ? `⚡ [HOP 3/5: COGNITIVE BRAIN] ML predicts P=65% (Medium). Long-Term Memory found <b>2 previous incidents</b>! Rule K4 ESCALATES: <b>MEDIUM ➔ HIGH</b>!`
          : `🧠 [HOP 3/5: COGNITIVE BRAIN] Random Forest evaluated packet with P=${(data.probability * 100).toFixed(1)}%. Rule <b>${data.fired_rules.join(", ")}</b> evaluated.`;
      }
      if (this.cardContextualMemory) {
        this.cardContextualMemory.classList.add(data.escalated ? "layer-card-focus cognitive" : "layer-card-focus");
      }
      if (this.cardVerdictShowcase) {
        this.cardVerdictShowcase.classList.add(data.escalated ? "layer-card-focus cognitive" : "layer-card-focus");
      }

      this.appendLog("model", `[ML MODEL] Random Forest predicted: ${data.prediction} (Probability: ${data.probability.toFixed(4)})`);
      this.appendLog("memory", `[MEMORY QUERY] Queried Long-Term Memory: Found ${data.previous_similar_count} prior verified incidents for (${raw.protocol_type}/${raw.service})`);

      if (data.escalated) {
        this.appendLog("escalation", `[RULE K4 TRIGGERED] Anomaly verified AND >= 2 history matches! Escalating: MEDIUM ➔ HIGH!`);
        this.sound.escalate();
      } else {
        this.sound.step();
      }

    } else if (this.currentHop === 4) {
      // HOP 4: Next-Gen Firewall (Policy Enforcement)
      this.nodes.firewall.classList.add("active");
      if (this.cables.cogFw) this.cables.cogFw.classList.add(isThreat ? "threat-active" : "active");
      if (tgtCable) tgtCable.classList.add(isThreat ? "threat-active" : "active");
      this.moveTokenToNode(this.nodes.firewall);

      if (this.tokenLabel) {
        this.tokenLabel.textContent = isThreat ? "🛑 Firewall DROP" : "⚡ Firewall PASS";
      }
      if (this.stageStatus) {
        this.stageStatus.innerHTML = `🛡️ [HOP 4/5: POLICY ENFORCEMENT] Firewall translating cognitive risk (${data.final_risk}) into enforcement action: <b>${data.security_action}</b>.`;
      }
      if (this.cardVerdictShowcase) {
        this.cardVerdictShowcase.classList.add(isThreat ? "layer-card-focus threat" : "layer-card-focus");
      }
      this.appendLog("action", `[FIREWALL POLICY] Enforcing security rule: ${data.security_action}`);
      this.sound.route();

    } else if (this.currentHop === 5) {
      // HOP 5: Target Destination or SOC Quarantine
      tgtNode.classList.add("active");
      if (isThreat) tgtNode.classList.add("threat");
      if (tgtCable) tgtCable.classList.add(isThreat ? "threat-active" : "active");
      this.moveTokenToNode(tgtNode);

      if (this.tokenLabel) {
        this.tokenLabel.textContent = isThreat ? "🚨 QUARANTINED IN SOC" : "✅ DELIVERED";
      }
      if (this.stageStatus) {
        this.stageStatus.innerHTML = isThreat
          ? `🛑 [HOP 5/5: ACTION EXECUTED] Threat safely contained and isolated in <b>SOC Quarantine Room</b>! Connection dropped.`
          : `✅ [HOP 5/5: ACTION EXECUTED] Legitimate traffic successfully delivered to <b>${tgtName}</b>. Session logged.`;
      }
      if (this.cardTerminalConsole) {
        this.cardTerminalConsole.classList.add(isThreat ? "layer-card-focus threat" : "layer-card-focus");
      }
      this.appendLog("action", `[ACTION ENFORCED] ${data.security_action} completed successfully.`);
      this.sound.step();
    }
  }

  nextHop() {
    if (!this.currentData) {
      this.injectAttack("apache_back");
      return;
    }
    if (this.currentHop < 5) {
      this.setHop(this.currentHop + 1);
    } else {
      if (this.isStreaming) {
        this.fetchNextPacket();
      } else {
        this.setHop(1);
        this.showToast("Packet flow replaying from Hop 1.");
      }
    }
  }

  prevHop() {
    if (!this.currentData) return;
    if (this.currentHop > 1) {
      this.setHop(this.currentHop - 1);
    }
  }

  toggleAutoPlay() {
    this.isAutoPlay = !this.isAutoPlay;
    if (this.btnHopAuto) {
      this.btnHopAuto.classList.toggle("running", this.isAutoPlay);
      this.btnHopAuto.innerHTML = this.isAutoPlay ? "⏸️ Pause Auto" : "⚡ Auto-Play";
    }
    if (this.stepperModeLabel) {
      this.stepperModeLabel.textContent = this.isAutoPlay ? "AUTO-FLOW ACTIVE" : "DEFENSE STEPPER";
    }
    if (this.isAutoPlay) {
      this.runAutoPlayHop();
    } else {
      if (this.autoPlayTimer) clearTimeout(this.autoPlayTimer);
    }
  }

  runAutoPlayHop() {
    if (!this.isAutoPlay) return;
    if (this.currentHop < 5) {
      this.nextHop();
      this.autoPlayTimer = setTimeout(() => this.runAutoPlayHop(), 1100);
    } else {
      this.autoPlayTimer = setTimeout(() => {
        if (!this.isAutoPlay) return;
        if (this.isStreaming) {
          this.fetchNextPacket();
        } else {
          this.setHop(1);
          this.autoPlayTimer = setTimeout(() => this.runAutoPlayHop(), 1100);
        }
      }, 2000);
    }
  }

  moveTokenToNode(node) {
    if (!node || !this.topologyCanvas || !this.packetToken) return;
    const cRect = this.topologyCanvas.getBoundingClientRect();
    const nRect = node.getBoundingClientRect();
    const left = Math.round(nRect.left - cRect.left + nRect.width / 2);
    const top = Math.round(nRect.top - cRect.top + nRect.height / 2);
    this.packetToken.style.left = `${left}px`;
    this.packetToken.style.top = `${top}px`;
    this.packetToken.style.opacity = "1";
    this.packetToken.style.display = "flex";
  }

  updateWire(wire, el1, el2) {
    if (!wire || !el1 || !el2 || !this.topologyCanvas) return;
    const c = this.topologyCanvas.getBoundingClientRect();
    const r1 = el1.getBoundingClientRect();
    const r2 = el2.getBoundingClientRect();
    const p1 = { x: Math.round(r1.left - c.left + r1.width / 2), y: Math.round(r1.top - c.top + r1.height / 2) };
    const p2 = { x: Math.round(r2.left - c.left + r2.width / 2), y: Math.round(r2.top - c.top + r2.height / 2) };
    wire.setAttribute("d", `M ${p1.x} ${p1.y} L ${p2.x} ${p2.y}`);
  }

  updateTopologyWires() {
    if (!this.topologyCanvas || !this.cables) return;
    try {
      this.updateWire(this.cables.pc1, this.sourceNodes.pc1, this.nodes.router);
      this.updateWire(this.cables.pc2, this.sourceNodes.pc2, this.nodes.router);
      this.updateWire(this.cables.pc3, this.sourceNodes.pc3, this.nodes.router);
      this.updateWire(this.cables.attacker, this.sourceNodes.attacker, this.nodes.router);
      this.updateWire(this.cables.routerCog, this.nodes.router, this.nodes.cognitive);
      this.updateWire(this.cables.cogFw, this.nodes.cognitive, this.nodes.firewall);
      this.updateWire(this.cables.fwWeb, this.nodes.firewall, this.targetNodes.web);
      this.updateWire(this.cables.fwFtp, this.nodes.firewall, this.targetNodes.ftp);
      this.updateWire(this.cables.fwDb, this.nodes.firewall, this.targetNodes.db);
      this.updateWire(this.cables.fwSoc, this.nodes.firewall, this.targetNodes.soc);
    } catch (e) {
      console.error("updateTopologyWires error:", e);
    }
  }

  parseAndAppendLog(logStr) {
    let tag = "INGRESS";
    let tagClass = "ingress";

    if (logStr.includes("[PERCEPTION]")) { tag = "PERCEPTION"; tagClass = "perception"; }
    else if (logStr.includes("[ATTENTION]")) { tag = "ATTENTION"; tagClass = "attention"; }
    else if (logStr.includes("[ML MODEL]")) { tag = "ML MODEL"; tagClass = "model"; }
    else if (logStr.includes("[MEMORY") || logStr.includes("[MEMORY QUERY]")) { tag = "MEMORY"; tagClass = "memory"; }
    else if (logStr.includes("ESCALAT") || logStr.includes("K4")) { tag = "ESCALATION"; tagClass = "escalation"; }
    else if (logStr.includes("[ACTION")) { tag = "ACTION"; tagClass = "action"; }

    const cleanMsg = logStr.replace(/\[.*?\]\s*/g, "");
    this.appendLog(tagClass, `[${tag}] ${cleanMsg || logStr}`);
  }

  appendLog(tagClass, message) {
    if (!this.terminalBody) return;
    const line = document.createElement("div");
    line.className = "log-line";
    const time = new Date().toLocaleTimeString();

    const parts = message.split("] ");
    const tag = parts.length > 1 ? parts[0] + "]" : `[${tagClass.toUpperCase()}]`;
    const text = parts.length > 1 ? parts.slice(1).join("] ") : message;

    line.innerHTML = `
      <span style="color:#64748b; font-size:0.7rem;">[${time}]</span>
      <span class="log-tag ${tagClass}">${tag}</span>
      <span>${text}</span>
    `;

    this.terminalBody.appendChild(line);
    this.terminalBody.scrollTop = this.terminalBody.scrollHeight;
  }

  showToast(msg) {
    const c = document.getElementById("toast-container");
    if (!c) return;
    const t = document.createElement("div");
    t.className = "toast";
    t.innerHTML = `<span>ℹ️</span> <span>${msg}</span>`;
    c.appendChild(t);
    setTimeout(() => { t.style.opacity = "0"; setTimeout(() => t.remove(), 300); }, 3000);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  window.NetGuard = new NetGuardApp();
});
