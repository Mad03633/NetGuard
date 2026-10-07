/**
 * NetGuard: Cognitive Engine Core Implementation
 * Matches Python implementation in `notebook/cognitive.ipynb`
 * 
 * Modules:
 * 1. Perception (LabelEncoding + StandardScaler)
 * 2. Attention (Feature Relevance Filter)
 * 3. ShortTermMemory (deque maxlen=5)
 * 4. LongTermMemory (Persistent JSON/Storage Engine)
 * 5. KnowledgeEngine (Ontology Graph & K1-K4 Rule Matrix)
 * 6. CognitivePipeline Orchestrator
 */

class PerceptionModule {
  constructor() {
    this.protocols = { "tcp": 1, "udp": 2, "icmp": 3 };
    this.services = {
      "http": 25, "ftp_data": 20, "private": 50, "smtp": 55, "ftp": 19,
      "telnet": 60, "domain_u": 15, "eco_i": 18, "other": 99
    };
    this.flags = {
      "SF": 9, "REJ": 1, "S2": 7, "S0": 5, "RSTO": 2, "RSTR": 3, "SH": 4
    };

    // Mean and Std deviations from NSL-KDD for key continuous features
    this.scalers = {
      "src_bytes": { mean: 45566.7, std: 5870319.0 },
      "dst_bytes": { mean: 18889.9, std: 4021269.0 },
      "count": { mean: 84.1, std: 114.5 },
      "srv_count": { mean: 27.7, std: 72.6 },
      "same_srv_rate": { mean: 0.66, std: 0.44 },
      "dst_host_srv_count": { mean: 115.6, std: 110.7 }
    };
  }

  encode(rawRecord) {
    const protoEnc = this.protocols[rawRecord.protocol_type] || 1;
    const servEnc = this.services[rawRecord.service] || 25;
    const flagEnc = this.flags[rawRecord.flag] || 9;

    const scaledSrcBytes = (rawRecord.src_bytes - this.scalers.src_bytes.mean) / this.scalers.src_bytes.std;
    const scaledDstBytes = (rawRecord.dst_bytes - this.scalers.dst_bytes.mean) / this.scalers.dst_bytes.std;
    const scaledCount = (rawRecord.count - this.scalers.count.mean) / this.scalers.count.std;
    const scaledSrvCount = (rawRecord.srv_count - this.scalers.srv_count.mean) / this.scalers.srv_count.std;
    const scaledSameSrvRate = (rawRecord.same_srv_rate - this.scalers.same_srv_rate.mean) / this.scalers.same_srv_rate.std;
    const scaledDstHostSrvCount = (rawRecord.dst_host_srv_count - this.scalers.dst_host_srv_count.mean) / this.scalers.dst_host_srv_count.std;

    // 41-dimensional standardized dense vector
    const vector = new Array(41).fill(0.0);
    vector[0] = 0.0; // duration
    vector[1] = protoEnc;
    vector[2] = servEnc;
    vector[3] = flagEnc;
    vector[4] = scaledSrcBytes;
    vector[5] = scaledDstBytes;
    vector[22] = scaledCount;
    vector[23] = scaledSrvCount;
    vector[28] = scaledSameSrvRate;
    vector[32] = scaledDstHostSrvCount;

    return {
      vectorShape: [1, 41],
      denseVector: vector,
      keyEncoded: {
        protocol: { raw: rawRecord.protocol_type, encoded: protoEnc },
        service: { raw: rawRecord.service, encoded: servEnc },
        flag: { raw: rawRecord.flag, encoded: flagEnc },
        src_bytes: { raw: rawRecord.src_bytes, scaled: scaledSrcBytes.toFixed(4) },
        dst_bytes: { raw: rawRecord.dst_bytes, scaled: scaledDstBytes.toFixed(4) },
        same_srv_rate: { raw: rawRecord.same_srv_rate, scaled: scaledSameSrvRate.toFixed(4) },
        dst_host_srv_count: { raw: rawRecord.dst_host_srv_count, scaled: scaledDstHostSrvCount.toFixed(4) }
      }
    };
  }
}

class AttentionModule {
  constructor(rankings) {
    this.rankings = rankings || NETGUARD_DATA.attentionRanking;
  }

  filter(rawRecord, encodedData, topN = 5) {
    const topFeatures = this.rankings.slice(0, topN).map(item => {
      let rawVal = rawRecord[item.feature];
      let procVal = encodedData.keyEncoded[item.feature] ? encodedData.keyEncoded[item.feature].scaled : (rawVal !== undefined ? rawVal : "0.0");
      if (rawVal === undefined) rawVal = 0;
      return {
        rank: item.rank,
        feature: item.feature,
        importance: item.importance,
        rawValue: rawVal,
        processedValue: procVal,
        role: item.role
      };
    });

    const noiseDropped = this.rankings.filter(item => item.group.includes("LOW")).map(item => ({
      feature: item.feature,
      importance: item.importance,
      reason: item.role
    }));

    return {
      topFeatures,
      noiseDropped,
      topNCount: topN,
      cumulativeImportance: topFeatures.reduce((acc, curr) => acc + curr.importance, 0)
    };
  }
}

/**
 * Short-Term Memory: Implemented as a FIFO bounded deque (maxlen=5)
 * Matches Python `deque(maxlen=max_events)`
 */
class ShortTermMemory {
  constructor(maxEvents = 5) {
    this.maxEvents = maxEvents;
    this.events = [];
  }

  remember(event) {
    if (this.events.length >= this.maxEvents) {
      this.events.shift(); // FIFO eviction
    }
    this.events.push(event);
  }

  retrieveRecent(n = 5) {
    return [...this.events].reverse().slice(0, n);
  }

  clear() {
    this.events = [];
  }

  size() {
    return this.events.length;
  }

  getAll() {
    return [...this.events];
  }
}

/**
 * Long-Term Memory: Persistent store for historical threat events
 * Corresponds to `assignment3_netguard_memory.json`
 */
class LongTermMemory {
  constructor(storageKey = "netguard_ltm_store") {
    this.storageKey = storageKey;
    this.init();
  }

  init() {
    try {
      const data = localStorage.getItem(this.storageKey);
      if (!data) {
        this.save(NETGUARD_DATA.defaultLongTermMemory);
      }
    } catch (e) {
      this.memoryFallback = [...NETGUARD_DATA.defaultLongTermMemory];
    }
  }

  load() {
    try {
      const raw = localStorage.getItem(this.storageKey);
      return raw ? JSON.parse(raw) : (this.memoryFallback || []);
    } catch (e) {
      return this.memoryFallback || [];
    }
  }

  save(data) {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(data));
    } catch (e) {
      this.memoryFallback = data;
    }
  }

  writeEvent(event) {
    const list = this.load().filter(x => x.event_id !== event.event_id);
    list.push(event);
    this.save(list);
    return list;
  }

  retrieveAll() {
    return this.load();
  }

  retrieveRecent(n = 5) {
    const list = this.load();
    return list.slice(-n).reverse();
  }

  findSimilarAnomalies(protocolType, service, excludeEventId = null) {
    const list = this.load();
    return list.filter(item => {
      if (excludeEventId && item.event_id === excludeEventId) return false;
      return (
        item.protocol_type === protocolType &&
        item.service === service &&
        item.prediction === "Anomaly"
      );
    });
  }

  seedDefaults() {
    this.save(NETGUARD_DATA.defaultLongTermMemory);
  }

  seedScenario(events) {
    const current = this.load();
    const eventIds = new Set(events.map(e => e.event_id));
    const merged = current.filter(e => !eventIds.has(e.event_id)).concat(events);
    this.save(merged);
  }

  clear() {
    this.save([]);
  }
}

/**
 * Knowledge Engine & Rules Matrix
 * Implements K1, K2, K3, and K4 (Memory-Aware Escalation)
 */
class KnowledgeEngine {
  constructor() {
    this.ontology = NETGUARD_DATA.ontology;
  }

  infer(probability, previousSimilarCount) {
    const firedRules = [];
    let baseRisk = "LOW";
    let recommendation = "Continue monitoring";

    // Rule K1, K2, K3 evaluation
    if (probability >= 0.80) {
      baseRisk = "HIGH";
      recommendation = "Immediate analyst review";
      firedRules.push("K1");
    } else if (probability >= 0.50) {
      baseRisk = "MEDIUM";
      recommendation = "Inspect suspicious connection";
      firedRules.push("K2");
    } else {
      baseRisk = "LOW";
      recommendation = "Continue monitoring";
      firedRules.push("K3");
    }

    let finalRisk = baseRisk;
    let escalated = false;

    // Cognitive Leap: Rule K4 (Memory Escalation for Ambiguous/Medium Risk)
    // When ML prediction is borderline (MEDIUM), memory resolves uncertainty by escalating to HIGH
    if (baseRisk === "MEDIUM" && previousSimilarCount >= 2) {
      firedRules.push("K4");
      escalated = true;
      finalRisk = "HIGH";
      recommendation = "Escalate to analyst: repeated anomalous protocol/service pattern confirmed in long-term memory (Rule K4)";
    }

    // Determine automated security action
    let securityAction = "ALLOW_AND_LOG";
    if (finalRisk === "LOW") {
      securityAction = "CONTINUE_MONITORING";
    } else if (finalRisk === "MEDIUM") {
      securityAction = "ENHANCED_TELEMETRY_LOG";
    } else if (finalRisk === "HIGH") {
      securityAction = "QUARANTINE_AND_SOC_ALERT";
    } else if (finalRisk === "CRITICAL") {
      securityAction = "BLOCK_IP_AND_FIREWALL_DROP";
    }

    return {
      baseRisk,
      finalRisk,
      escalated,
      firedRules,
      recommendation,
      securityAction,
      ruleDefinitions: firedRules.map(rId => this.ontology.rules.find(r => r.id === rId))
    };
  }
}

/**
 * Complete NetGuard Cognitive Pipeline
 */
class CognitivePipeline {
  constructor() {
    this.perception = new PerceptionModule();
    this.attention = new AttentionModule();
    this.shortTermMemory = new ShortTermMemory(5);
    this.longTermMemory = new LongTermMemory();
    this.knowledge = new KnowledgeEngine();
  }

  process(rawRecord, options = {}) {
    const eventId = options.eventId || `evt_${Date.now().toString(36)}`;
    const topN = options.topN || 5;
    const persist = options.persist !== false;

    // 1. Perception Module
    const perceptionResult = this.perception.encode(rawRecord);

    // 2. Attention Module
    const attentionResult = this.attention.filter(rawRecord, perceptionResult, topN);

    // 3. AI Predictive Model (Probability estimation)
    let probability = options.customProbability;
    if (probability === undefined) {
      probability = rawRecord.modelProbability !== undefined ? rawRecord.modelProbability : 0.65;
    }
    const predictionName = probability >= 0.50 ? "Anomaly" : "Normal";

    // 4. Memory Retrieval (Historical matching in LTM)
    const similarAnomalies = this.longTermMemory.findSimilarAnomalies(
      rawRecord.protocol_type,
      rawRecord.service,
      eventId
    );
    const similarCount = similarAnomalies.length;

    // 5. Knowledge Inference & Rule Matrix (K1-K4)
    const inferenceResult = this.knowledge.infer(probability, similarCount);

    // 6. Memory Write (Store in Short-Term deque & Long-Term JSON store)
    const memoryEvent = {
      event_id: eventId,
      timestamp: new Date().toISOString(),
      protocol_type: rawRecord.protocol_type,
      service: rawRecord.service,
      prediction: predictionName,
      probability: Number(probability.toFixed(4)),
      base_risk: inferenceResult.baseRisk,
      final_risk: inferenceResult.finalRisk,
      recommendation: inferenceResult.recommendation
    };

    this.shortTermMemory.remember(memoryEvent);
    if (persist) {
      this.longTermMemory.writeEvent(memoryEvent);
    }

    return {
      eventId,
      timestamp: memoryEvent.timestamp,
      rawRecord,
      perception: perceptionResult,
      attention: attentionResult,
      aiModel: {
        probability,
        prediction: predictionName,
        groundTruth: rawRecord.label || "unknown",
        binaryTruth: rawRecord.binaryLabel !== undefined ? rawRecord.binaryLabel : (probability >= 0.5 ? 1 : 0)
      },
      memory: {
        similarAnomalies,
        similarCount,
        shortTermRecent: this.shortTermMemory.retrieveRecent(5),
        shortTermCapacity: { size: this.shortTermMemory.size(), max: this.shortTermMemory.maxEvents },
        longTermTotalCount: this.longTermMemory.retrieveAll().length
      },
      inference: inferenceResult,
      memoryEvent
    };
  }
}
