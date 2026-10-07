/**
 * NetGuard: Cognitive AI System for Network Anomaly Detection
 * Course: Cognitive technologies and decision support systems | Khabiyev Zhangirkhan
 * Authors: Madiyar B., Angsar S., Alisher A. — AAI-2501M
 * Repository: https://github.com/Mad03633/NetGuard
 * 
 * Dataset & Ontology Definitions (NSL-KDD, Attention, Memory, Rules)
 */

const NETGUARD_DATA = {
  meta: {
    title: "NetGuard: Cognitive AI System for Network Anomaly Detection",
    course: "Cognitive technologies and decision support systems | Instructor: Khabiyev Zhangirkhan",
    authors: "Madiyar B., Angsar S., Alisher A. — AAI-2501M",
    github: "https://github.com/Mad03633/NetGuard",
    status: "ONLINE"
  },

  features: [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
    "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",
    "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
    "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
    "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
    "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
    "dst_host_rerror_rate", "dst_host_srv_rerror_rate"
  ],

  // Top Random Forest Feature Importance values from cognitive.ipynb
  attentionRanking: [
    { rank: 1, feature: "src_bytes", importance: 0.172345, group: "HIGH", role: "Primary traffic payload indicator (source)" },
    { rank: 2, feature: "dst_bytes", importance: 0.116215, group: "HIGH", role: "Response traffic volume indicator" },
    { rank: 3, feature: "flag", importance: 0.080317, group: "HIGH", role: "TCP connection status flag (SF, REJ, S2, etc.)" },
    { rank: 4, feature: "same_srv_rate", importance: 0.071144, group: "HIGH", role: "% of connections to the same service" },
    { rank: 5, feature: "dst_host_srv_count", importance: 0.068655, group: "HIGH", role: "Destination host service connection count" },
    { rank: 6, feature: "dst_host_same_srv_rate", importance: 0.054321, group: "MEDIUM", role: "Rate of same-service accesses at target" },
    { rank: 7, feature: "diff_srv_rate", importance: 0.048912, group: "MEDIUM", role: "% of connections to different services" },
    { rank: 8, feature: "dst_host_serror_rate", importance: 0.045610, group: "MEDIUM", role: "SYN error rate on target host" },
    { rank: 9, feature: "count", importance: 0.041235, group: "MEDIUM", role: "Connections to same destination in past 2s" },
    { rank: 10, feature: "srv_serror_rate", importance: 0.038921, group: "MEDIUM", role: "Service SYN error rate" },
    // Low importance noise dropped by Attention module
    { rank: 37, feature: "urgent", importance: 0.000041, group: "LOW (Noise)", role: "Urgent packets counter (near zero impact)" },
    { rank: 38, feature: "su_attempted", importance: 0.000033, group: "LOW (Noise)", role: "Superuser state attempts (infrequent)" },
    { rank: 39, feature: "land", importance: 0.000022, group: "LOW (Noise)", role: "Land attack spoof (filtered as noise)" },
    { rank: 40, feature: "is_host_login", importance: 0.000000, group: "LOW (Noise)", role: "Host login flag (uninformative)" },
    { rank: 41, feature: "num_outbound_cmds", importance: 0.000000, group: "LOW (Noise)", role: "Outbound command count (constant)" }
  ],

  // Knowledge Graph Ontology
  ontology: {
    entities: [
      { id: "NetworkConnection", label: "NetworkConnection", type: "Core Subject", icon: "🌐", desc: "Raw or processed NSL-KDD session entity" },
      { id: "Protocol", label: "Protocol", type: "Attribute", icon: "📡", desc: "Transport protocol (TCP, UDP, ICMP)" },
      { id: "Service", label: "Service", type: "Target", icon: "🖥️", desc: "Destination service (http, ftp_data, private, smtp)" },
      { id: "Prediction", label: "Prediction", type: "AI State", icon: "🧠", desc: "ML probability & classification (Normal / Anomaly)" },
      { id: "RiskLevel", label: "RiskLevel", type: "Cognitive State", icon: "🛡️", desc: "Contextual risk rating (LOW, MEDIUM, HIGH, CRITICAL)" },
      { id: "SecurityAction", label: "SecurityAction", type: "Decision", icon: "⚡", desc: "Enforced response (Monitor, Inspect, Escalate, Block)" }
    ],
    relationships: [
      { source: "NetworkConnection", target: "Protocol", relation: "uses", desc: "Connection communicates via network protocol" },
      { source: "NetworkConnection", target: "Service", relation: "accesses", desc: "Connection targets specific network service" },
      { source: "NetworkConnection", target: "Prediction", relation: "produces", desc: "Connection evaluation yields ML prediction" },
      { source: "Prediction", target: "RiskLevel", relation: "has", desc: "Prediction maps to baseline risk category" },
      { source: "RiskLevel", target: "SecurityAction", relation: "triggers", desc: "Final cognitive risk enforces security policy" }
    ],
    rules: [
      { id: "K1", name: "High Probability Rule", condition: "P(Anomaly) >= 0.80", outcome: "Risk = HIGH", action: "Immediate analyst review", desc: "Clear malicious signature with high model confidence." },
      { id: "K2", name: "Medium Probability Rule", condition: "0.50 <= P(Anomaly) < 0.80", outcome: "Risk = MEDIUM", action: "Inspect suspicious connection", desc: "Borderline anomaly. Subject to contextual memory escalation." },
      { id: "K3", name: "Low Probability Rule", condition: "P(Anomaly) < 0.50", outcome: "Risk = LOW", action: "Continue monitoring", desc: "Traffic consistent with benign network profile." },
      { id: "K4", name: "Memory-Aware Escalation Rule", condition: "Anomaly = True AND Previous Similar Anomalies in Memory >= 2", outcome: "Escalate Risk Priority (MEDIUM➔HIGH, HIGH➔CRITICAL)", action: "Escalate to analyst: repeated anomalous pattern found in long-term memory", desc: "Dynamic cognitive leap: historical repetition turns uncertain alerts into verified threats." }
    ]
  },

  // Initial persistent memory seed (corresponds to notebook history for Case 3 demonstration)
  defaultLongTermMemory: [
    {
      event_id: "test_7527",
      timestamp: "2026-10-05T14:11:56.931Z",
      protocol_type: "tcp",
      service: "http",
      prediction: "Anomaly",
      probability: 1.000000,
      base_risk: "HIGH",
      final_risk: "HIGH",
      recommendation: "Immediate analyst review"
    },
    {
      event_id: "test_11868",
      timestamp: "2026-10-05T14:11:56.942Z",
      protocol_type: "tcp",
      service: "http",
      prediction: "Anomaly",
      probability: 1.000000,
      base_risk: "HIGH",
      final_risk: "HIGH",
      recommendation: "Immediate analyst review"
    }
  ],

  // Pre-configured Scenarios
  scenarios: [
    {
      id: "case-1",
      badge: "Scenario 1",
      title: "Legitimate FTP Transfer",
      subtitle: "Low Risk — Continue Monitoring",
      description: "Standard data session on ftp_data with complete handshake (SF) and normal bytes transfer. Low anomaly probability triggers Rule K3.",
      sourceNode: { name: "Client Workstation", ip: "192.168.1.105", port: 51240, type: "host" },
      targetNode: { name: "FTP File Server", ip: "10.0.0.45", port: 20, type: "server" },
      rawInput: {
        protocol_type: "tcp",
        service: "ftp_data",
        flag: "SF",
        src_bytes: 12983,
        dst_bytes: 0,
        count: 1,
        srv_count: 1,
        same_srv_rate: 1.0,
        dst_host_srv_count: 86
      },
      perceptionVector: [-0.005036, -0.004614, 9.0, 0.749108, -0.300837, 0.0, 0.0, 0.12, 0.0],
      attentionFocus: [
        { feature: "src_bytes", importance: 0.172345, raw: "12983", processed: "-0.0050" },
        { feature: "dst_bytes", importance: 0.116215, raw: "0", processed: "-0.0046" },
        { feature: "flag", importance: 0.080317, raw: "SF", processed: "9.00" },
        { feature: "same_srv_rate", importance: 0.071144, raw: "1.0", processed: "0.7491" },
        { feature: "dst_host_srv_count", importance: 0.068655, raw: "86", processed: "-0.3008" }
      ],
      noiseDropped: ["urgent (0.000041)", "land (0.000022)", "su_attempted (0.000033)"],
      modelPrediction: {
        probability: 0.0000,
        verdict: "Normal",
        label: "normal",
        binaryLabel: 0
      },
      memoryQuery: {
        protocol_type: "tcp",
        service: "ftp_data",
        prediction: "Anomaly"
      },
      seedMemoryRequired: false,
      expectedRules: ["K3"],
      baseRisk: "LOW",
      finalRisk: "LOW",
      escalated: false,
      recommendation: "Continue monitoring",
      cognitiveSummary: "ML probability is 0.0000 (Low). Memory contains 0 prior anomalous incidents for (tcp/ftp_data). Rule K3 fires; risk remains LOW without escalation."
    },

    {
      id: "case-2",
      badge: "Scenario 2",
      title: "Neptune SYN Flood Attack",
      subtitle: "High Risk — Immediate Analyst Review",
      description: "Aggressive DoS flood with connection rejected (REJ) flags and zero payload targeting internal private services. Model confidence is 100%, triggering Rule K1.",
      sourceNode: { name: "External Attacker", ip: "185.220.101.5", port: 44211, type: "attacker" },
      targetNode: { name: "Internal Gateway", ip: "10.0.0.1", port: 445, type: "server" },
      rawInput: {
        protocol_type: "tcp",
        service: "private",
        flag: "REJ",
        src_bytes: 0,
        dst_bytes: 0,
        count: 229,
        srv_count: 10,
        same_srv_rate: 0.04,
        dst_host_srv_count: 10
      },
      perceptionVector: [-0.007436, -0.004614, 1.0, -1.449992, -0.984094, 1.25, 0.0, 0.95, 0.0],
      attentionFocus: [
        { feature: "src_bytes", importance: 0.172345, raw: "0", processed: "-0.0074" },
        { feature: "dst_bytes", importance: 0.116215, raw: "0", processed: "-0.0046" },
        { feature: "flag", importance: 0.080317, raw: "REJ", processed: "1.00" },
        { feature: "same_srv_rate", importance: 0.071144, raw: "0.04", processed: "-1.4500" },
        { feature: "dst_host_srv_count", importance: 0.068655, raw: "10", processed: "-0.9841" }
      ],
      noiseDropped: ["urgent (0.000041)", "land (0.000022)", "is_host_login (0.000000)"],
      modelPrediction: {
        probability: 1.0000,
        verdict: "Anomaly",
        label: "neptune",
        binaryLabel: 1
      },
      memoryQuery: {
        protocol_type: "tcp",
        service: "private",
        prediction: "Anomaly"
      },
      seedMemoryRequired: false,
      expectedRules: ["K1"],
      baseRisk: "HIGH",
      finalRisk: "HIGH",
      escalated: false,
      recommendation: "Immediate analyst review",
      cognitiveSummary: "ML probability is 1.0000 (>= 0.80). Rule K1 directly triggers HIGH risk for immediate analyst review. Severity is already maximum base tier."
    },

    {
      id: "case-3",
      badge: "Scenario 3 (Star Demo)",
      title: "Apache 'Back' DoS Exploit",
      subtitle: "Memory Escalation: MEDIUM ➔ HIGH",
      description: "Subtle DoS exploit flooding Apache HTTP server. The standalone ML model generates an ambiguous Medium probability (P=0.65). The Cognitive Memory Engine intervenes, finds 2 previous historical incidents for (tcp/http), and triggers Rule K4 to escalate risk to HIGH!",
      sourceNode: { name: "Suspicious Host", ip: "194.26.29.112", port: 38992, type: "attacker" },
      targetNode: { name: "Web Application Server", ip: "10.0.0.80", port: 80, type: "server" },
      rawInput: {
        protocol_type: "tcp",
        service: "http",
        flag: "S2",
        src_bytes: 54540,
        dst_bytes: 8315,
        count: 4,
        srv_count: 4,
        same_srv_rate: 1.0,
        dst_host_srv_count: 254
      },
      perceptionVector: [0.002646, -0.002369, 7.0, 0.749108, 1.209521, 0.0, 0.0, 0.05, 0.0],
      attentionFocus: [
        { feature: "src_bytes", importance: 0.172345, raw: "54540", processed: "0.0026" },
        { feature: "dst_bytes", importance: 0.116215, raw: "8315", processed: "-0.0024" },
        { feature: "flag", importance: 0.080317, raw: "S2", processed: "7.00" },
        { feature: "same_srv_rate", importance: 0.071144, raw: "1.0", processed: "0.7491" },
        { feature: "dst_host_srv_count", importance: 0.068655, raw: "254", processed: "1.2095" }
      ],
      noiseDropped: ["urgent (0.000041)", "land (0.000022)", "su_attempted (0.000033)"],
      modelPrediction: {
        probability: 0.6500,
        verdict: "Anomaly",
        label: "back",
        binaryLabel: 1
      },
      memoryQuery: {
        protocol_type: "tcp",
        service: "http",
        prediction: "Anomaly"
      },
      seedMemoryRequired: true,
      expectedRules: ["K2", "K4"],
      baseRisk: "MEDIUM",
      finalRisk: "HIGH",
      escalated: true,
      recommendation: "Escalate to analyst: repeated anomalous protocol/service pattern found in long-term memory",
      cognitiveSummary: "CRITICAL COGNITIVE SHIFT: ML output is only MEDIUM (P=0.6500, Rule K2). However, Long-Term Memory retrieves 2 prior confirmed anomalies matching (tcp, http). Rule K4 triggers and ESCALATES risk to HIGH! This prevents a stealth DoS exploit from going overlooked."
    },

    {
      id: "case-4",
      badge: "Scenario 4",
      title: "Recurrent Botnet Reconnaissance",
      subtitle: "Memory Escalation: HIGH ➔ CRITICAL",
      description: "Persistent scanning sweep across private ports with multiple previous hits on record. Baseline High risk is escalated to CRITICAL due to recurrent threat presence.",
      sourceNode: { name: "Botnet Cluster", ip: "203.0.113.88", port: 60233, type: "attacker" },
      targetNode: { name: "Database DMZ", ip: "10.0.0.150", port: 1433, type: "server" },
      rawInput: {
        protocol_type: "tcp",
        service: "private",
        flag: "S0",
        src_bytes: 0,
        dst_bytes: 0,
        count: 180,
        srv_count: 8,
        same_srv_rate: 0.05,
        dst_host_srv_count: 5
      },
      perceptionVector: [-0.007436, -0.004614, 5.0, -1.350000, -1.100000, 1.8, 0.0, 0.88, 0.0],
      attentionFocus: [
        { feature: "src_bytes", importance: 0.172345, raw: "0", processed: "-0.0074" },
        { feature: "dst_bytes", importance: 0.116215, raw: "0", processed: "-0.0046" },
        { feature: "flag", importance: 0.080317, raw: "S0", processed: "5.00" },
        { feature: "same_srv_rate", importance: 0.071144, raw: "0.05", processed: "-1.3500" },
        { feature: "dst_host_srv_count", importance: 0.068655, raw: "5", processed: "-1.1000" }
      ],
      noiseDropped: ["urgent (0.000041)", "land (0.000022)", "num_outbound_cmds (0.000000)"],
      modelPrediction: {
        probability: 0.8800,
        verdict: "Anomaly",
        label: "portsweep",
        binaryLabel: 1
      },
      memoryQuery: {
        protocol_type: "tcp",
        service: "private",
        prediction: "Anomaly"
      },
      seedMemoryRequired: true,
      customHistorySeed: [
        { event_id: "test_private_1", timestamp: "2026-10-06T18:00:00Z", protocol_type: "tcp", service: "private", prediction: "Anomaly", probability: 0.95, base_risk: "HIGH", final_risk: "HIGH" },
        { event_id: "test_private_2", timestamp: "2026-10-06T20:30:00Z", protocol_type: "tcp", service: "private", prediction: "Anomaly", probability: 0.92, base_risk: "HIGH", final_risk: "HIGH" }
      ],
      expectedRules: ["K1", "K4"],
      baseRisk: "HIGH",
      finalRisk: "CRITICAL",
      escalated: true,
      recommendation: "Escalate to analyst: repeated anomalous protocol/service pattern found in long-term memory",
      cognitiveSummary: "ML probability is 0.8800 (Base HIGH, Rule K1). Long-Term Memory discovers repeated previous anomalies on private service. Rule K4 escalates HIGH to CRITICAL, triggering immediate quarantine and firewall block."
    }
  ]
};
