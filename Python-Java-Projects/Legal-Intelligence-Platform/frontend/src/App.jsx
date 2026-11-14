import { useState } from "react";
import "./App.css";

// ============================================================
// API CONFIGURATION
// ============================================================

// Production: Vercel deployed backend
// Local development: create a .env file with VITE_API_URL
const API =
  import.meta.env.VITE_API_URL ||
  "https://legal-intelligence-platform-l4te-ice68xam8-llllcom.vercel.app";

function App() {
  const [activeView, setActiveView] = useState("Dashboard");

  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [compliance, setCompliance] = useState(null);
  const [alerts, setAlerts] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [copilotQuestion, setCopilotQuestion] = useState("");
  const [copilotAnswer, setCopilotAnswer] = useState("");
  const [copilotLoading, setCopilotLoading] = useState(false);

  // ============================================================
  // FILE SELECT
  // ============================================================

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];

    if (!selectedFile) return;

    if (!selectedFile.name.toLowerCase().endsWith(".pdf")) {
      setError("Only PDF files are supported.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setError("");
  };

  // ============================================================
  // ANALYZE CONTRACT
  // ============================================================

  const analyzeContract = async () => {
    if (!file) {
      setError("Please select a PDF contract first.");
      return;
    }

    setLoading(true);
    setError("");
    setAnalysis(null);
    setCompliance(null);
    setAlerts(null);
    setCopilotAnswer("");
    setCopilotQuestion("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      // Main contract analysis
      const analysisResponse = await fetch(
        `${API}/contracts/analyze`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!analysisResponse.ok) {
        const errorText = await analysisResponse.text();
        throw new Error(
          `Contract analysis failed (${analysisResponse.status}). ${errorText}`
        );
      }

      const analysisData = await analysisResponse.json();
      setAnalysis(analysisData);

      // ========================================================
      // COMPLIANCE
      // ========================================================

      const complianceForm = new FormData();
      complianceForm.append("file", file);

      const complianceResponse = await fetch(
        `${API}/compliance/check`,
        {
          method: "POST",
          body: complianceForm,
        }
      );

      if (complianceResponse.ok) {
        const complianceData = await complianceResponse.json();
        setCompliance(complianceData);
      }

      // ========================================================
      // ALERTS
      // ========================================================

      const alertForm = new FormData();
      alertForm.append("file", file);

      const alertResponse = await fetch(
        `${API}/alerts/generate`,
        {
          method: "POST",
          body: alertForm,
        }
      );

      if (alertResponse.ok) {
        const alertData = await alertResponse.json();
        setAlerts(alertData);
      }
    } catch (err) {
      console.error("API Error:", err);

      setError(
        err.message ||
        "Unable to connect to Legal Intelligence API."
      );
    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // AI COPILOT
  // ============================================================

  const askCopilot = async (question = copilotQuestion) => {
    if (!question.trim()) return;

    if (!analysis?.text) {
      setError("Please analyze a contract first.");
      return;
    }

    setCopilotLoading(true);
    setCopilotAnswer("");
    setError("");

    try {
      const response = await fetch(`${API}/copilot/ask`, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          question: question,
          contract_text: analysis.text,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();

        throw new Error(
          `Copilot request failed (${response.status}). ${errorText}`
        );
      }

      const data = await response.json();

      setCopilotAnswer(
        data.answer || "No answer was returned by the AI Copilot."
      );

      setCopilotQuestion(question);
    } catch (err) {
      console.error("Copilot Error:", err);

      setError(
        err.message || "Unable to connect to AI Legal Copilot."
      );
    } finally {
      setCopilotLoading(false);
    }
  };

  // ============================================================
  // RESET
  // ============================================================

  const resetDashboard = () => {
    setFile(null);
    setAnalysis(null);
    setCompliance(null);
    setAlerts(null);
    setCopilotQuestion("");
    setCopilotAnswer("");
    setError("");
    setActiveView("Dashboard");
  };

  // ============================================================
  // HELPERS
  // ============================================================

  const getRiskClass = (level) => {
    if (!level) return "low";

    return String(level).toLowerCase();
  };

  const getSeverityClass = (severity) => {
    if (!severity) return "medium";

    return String(severity).toLowerCase();
  };

  // ============================================================
  // SIDEBAR
  // ============================================================

  const Sidebar = () => (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">⚖️</div>

        <div>
          <h2>LegalIntel</h2>
          <p>LEGAL OPERATIONS PLATFORM</p>
        </div>
      </div>

      <div className="sidebar-menu">
        <div
          className={`menu-item ${activeView === "Dashboard" ? "active" : ""
            }`}
          onClick={() => setActiveView("Dashboard")}
        >
          <span>📊</span>
          Dashboard
        </div>

        <div
          className={`menu-item ${activeView === "Contracts" ? "active" : ""
            }`}
          onClick={() => setActiveView("Contracts")}
        >
          <span>📄</span>
          Contracts
        </div>

        <div
          className={`menu-item ${activeView === "Risk Intelligence"
              ? "active"
              : ""
            }`}
          onClick={() =>
            setActiveView("Risk Intelligence")
          }
        >
          <span>⚠️</span>
          Risk Intelligence
        </div>

        <div
          className={`menu-item ${activeView === "Compliance" ? "active" : ""
            }`}
          onClick={() => setActiveView("Compliance")}
        >
          <span>🛡️</span>
          Compliance
        </div>

        <div
          className={`menu-item ${activeView === "Alert Center" ? "active" : ""
            }`}
          onClick={() => setActiveView("Alert Center")}
        >
          <span>🚨</span>
          Alert Center
        </div>

        <div
          className={`menu-item ${activeView === "AI Copilot" ? "active" : ""
            }`}
          onClick={() => setActiveView("AI Copilot")}
        >
          <span>🤖</span>
          AI Copilot
        </div>
      </div>

      <div className="sidebar-bottom">
        <div className="system-status">
          <span className="status-dot"></span>
          System Operational
        </div>

        <p>Enterprise Legal Intelligence</p>
        <p>Version 1.0.0</p>
      </div>
    </aside>
  );

  // ============================================================
  // TOPBAR
  // ============================================================

  const Topbar = () => (
    <div className="topbar">
      <div>
        <h1>{activeView}</h1>

        <p>
          AI-powered contract analysis, risk detection and
          compliance intelligence.
        </p>
      </div>

      <div className="api-status">
        <span></span>
        API Online
      </div>
    </div>
  );

  // ============================================================
  // UPLOAD CARD
  // ============================================================

  const UploadCard = () => (
    <div className="upload-card">
      <div className="upload-info">
        <div className="upload-icon">📄</div>

        <div>
          <h2>Analyze Legal Contract</h2>

          <p>
            Upload an NDA, Service Agreement, Vendor
            Agreement, Employment Contract or other legal
            document.
          </p>
        </div>
      </div>

      <div className="upload-controls">
        <label className="file-input">
          📄{" "}
          {file
            ? file.name
            : "Choose PDF"}

          <input
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleFileChange}
          />
        </label>

        <button
          className="analyze-button"
          onClick={analyzeContract}
          disabled={loading || !file}
        >
          {loading
            ? "Analyzing..."
            : "Analyze Contract"}
        </button>

        <button
          className="reset-button"
          onClick={resetDashboard}
        >
          Reset
        </button>
      </div>
    </div>
  );

  // ============================================================
  // ERROR
  // ============================================================

  const ErrorBox = () => {
    if (!error) return null;

    return (
      <div className="error-box">
        {error}
      </div>
    );
  };

  // ============================================================
  // CONTRACT INFO
  // ============================================================

  const ContractInfo = () => {
    if (!analysis) return null;

    return (
      <div className="contract-info">
        <div>
          <span>DOCUMENT</span>
          <strong>{analysis.filename}</strong>
        </div>

        <div>
          <span>PAGES</span>
          <strong>{analysis.pages}</strong>
        </div>

        <div>
          <span>EXTRACTED CHARACTERS</span>
          <strong>{analysis.text_length}</strong>
        </div>

        <div>
          <span>ANALYSIS STATUS</span>
          <strong>Complete</strong>
        </div>
      </div>
    );
  };

  // ============================================================
  // STATS
  // ============================================================

  const Stats = () => {
    if (!analysis) return null;

    const data = analysis.analysis || {};

    return (
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">⚖️</div>

          <div>
            <span>Risk Score</span>

            <strong>
              {data.risk_score ?? 0}
            </strong>

            <small
              className={getRiskClass(data.risk_level)}
            >
              {data.risk_level || "Low"} Risk
            </small>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📑</div>

          <div>
            <span>Detected Clauses</span>

            <strong>
              {(data.clauses || []).length}
            </strong>

            <small>Legal clauses found</small>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⚠️</div>

          <div>
            <span>Risks Found</span>

            <strong>
              {(data.risks || []).length}
            </strong>

            <small>Potential issues</small>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📅</div>

          <div>
            <span>Obligations</span>

            <strong>
              {(data.obligations || []).length}
            </strong>

            <small>Contract obligations</small>
          </div>
        </div>
      </div>
    );
  };

  // ============================================================
  // RISK PANEL
  // ============================================================

  const RiskPanel = () => {
    if (!analysis) return null;

    const data = analysis.analysis || {};

    return (
      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>⚠️ Risk Intelligence</h2>

            <p>
              Overall contractual risk assessment
            </p>
          </div>

          <span
            className={`badge ${getRiskClass(
              data.risk_level
            )}`}
          >
            {data.risk_level || "Low"}
          </span>
        </div>

        <div className="risk-content">
          <div className="risk-circle">
            <strong>
              {data.risk_score ?? 0}
            </strong>

            <span>/ 100</span>
          </div>

          <div className="risk-description">
            <h3>
              {data.risk_level === "High"
                ? "High Risk Contract"
                : data.risk_level === "Medium"
                  ? "Contract Needs Review"
                  : "Low Risk Contract"}
            </h3>

            <p>
              The intelligence engine evaluated detected
              clauses, missing clauses and contractual risk
              indicators.
            </p>
          </div>
        </div>
      </section>
    );
  };

  // ============================================================
  // COMPLIANCE PANEL
  // ============================================================

  const CompliancePanel = () => {
    if (!analysis) return null;

    const data =
      compliance || {
        compliance:
          analysis.analysis?.compliance || [],
        compliance_score: 0,
      };

    const items = data.compliance || [];

    return (
      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>🛡️ Compliance Intelligence</h2>

            <p>
              Regulatory and policy signals
            </p>
          </div>

          <span className="score-badge">
            {data.compliance_score ?? 0}%
          </span>
        </div>

        <div className="progress-container">
          <div className="progress-label">
            <span>Compliance Coverage</span>

            <strong>
              {data.compliance_score ?? 0}%
            </strong>
          </div>

          <div className="progress">
            <div
              className="progress-fill"
              style={{
                width: `${data.compliance_score ?? 0}%`,
              }}
            ></div>
          </div>
        </div>

        <div className="compliance-list">
          {items.length === 0 ? (
            <div className="empty-state">
              No compliance signals detected.
            </div>
          ) : (
            items.map((item, index) => (
              <div
                className="compliance-item"
                key={index}
              >
                <span>
                  {item.status === "Detected"
                    ? "✓"
                    : "!"}
                </span>

                <div>
                  <strong>
                    {item.framework}
                  </strong>

                  <small>
                    {item.status}
                  </small>
                </div>
              </div>
            ))
          )}
        </div>
      </section>
    );
  };

  // ============================================================
  // CLAUSE PANEL
  // ============================================================

  const ClausePanel = () => {
    if (!analysis) return null;

    const data = analysis.analysis || {};

    return (
      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>📑 Clause Intelligence</h2>

            <p>
              Contractual clauses automatically detected
              by the intelligence engine.
            </p>
          </div>

          <span className="count-badge">
            {(data.clauses || []).length} Detected
          </span>
        </div>

        <div className="clause-grid">
          {(data.clauses || []).map(
            (clause, index) => (
              <div
                className="clause-card"
                key={index}
              >
                <div className="clause-check">
                  ✓
                </div>

                <div>
                  <h3>{clause.clause}</h3>

                  <p>
                    Keywords:{" "}
                    {(clause.keywords || []).join(
                      ", "
                    )}
                  </p>
                </div>
              </div>
            )
          )}
        </div>

        {(data.missing_clauses || []).length >
          0 && (
            <div className="missing-section">
              <h3>⚠️ Missing Clauses</h3>

              <div className="missing-list">
                {data.missing_clauses.map(
                  (clause, index) => (
                    <div
                      className="missing-item"
                      key={index}
                    >
                      <span>!</span>

                      <div>
                        <strong>
                          {clause.clause}
                        </strong>

                        <small>
                          This clause was not detected.
                        </small>
                      </div>
                    </div>
                  )
                )}
              </div>
            </div>
          )}
      </section>
    );
  };

  // ============================================================
  // RISKS
  // ============================================================

  const RisksPanel = () => {
    if (!analysis) return null;

    const risks =
      analysis.analysis?.risks || [];

    return (
      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>⚠️ Identified Risks</h2>

            <p>
              Potential contractual and compliance
              risks.
            </p>
          </div>

          <span className="count-badge">
            {risks.length} Risks
          </span>
        </div>

        <div className="risk-list">
          {risks.length === 0 ? (
            <div className="empty-state">
              No significant contractual risks were
              detected.
            </div>
          ) : (
            risks.map((risk, index) => (
              <div
                className={`risk-item ${getSeverityClass(
                  risk.severity
                )}`}
                key={index}
              >
                <div className="risk-icon">
                  ⚠️
                </div>

                <div className="risk-details">
                  <div className="risk-title">
                    <h3>{risk.risk}</h3>

                    <span className="severity">
                      {risk.severity}
                    </span>
                  </div>

                  <p>{risk.explanation}</p>
                </div>
              </div>
            ))
          )}
        </div>
      </section>
    );
  };

  // ============================================================
  // OBLIGATIONS
  // ============================================================

  const ObligationsPanel = () => {
    if (!analysis) return null;

    const obligations =
      analysis.analysis?.obligations || [];

    return (
      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>📅 Contract Obligations</h2>

            <p>
              Important contractual responsibilities
              extracted from the document.
            </p>
          </div>

          <span className="count-badge">
            {obligations.length} Obligations
          </span>
        </div>

        <div className="obligation-list">
          {obligations.length === 0 ? (
            <div className="empty-state">
              No obligations detected.
            </div>
          ) : (
            obligations.map(
              (item, index) => (
                <div
                  className="obligation-item"
                  key={index}
                >
                  <div className="obligation-number">
                    {index + 1}
                  </div>

                  <p>
                    {item.obligation}
                  </p>
                </div>
              )
            )
          )}
        </div>
      </section>
    );
  };

  // ============================================================
  // ALERT CENTER
  // ============================================================

  const AlertsPanel = () => {
    if (!alerts) {
      return (
        <section className="panel">
          <div className="empty-state">
            Analyze a contract to generate alerts.
          </div>
        </section>
      );
    }

    return (
      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>🚨 Alert Center</h2>

            <p>
              AI-generated alerts requiring legal
              review.
            </p>
          </div>

          <span className="count-badge">
            {alerts.total_alerts || 0} Alerts
          </span>
        </div>

        <div className="alert-summary">
          <div className="alert-stat high">
            <strong>
              {alerts.high_priority || 0}
            </strong>

            <span>High Priority</span>
          </div>

          <div className="alert-stat medium">
            <strong>
              {alerts.medium_priority || 0}
            </strong>

            <span>Medium Priority</span>
          </div>

          <div className="alert-stat low">
            <strong>
              {alerts.low_priority || 0}
            </strong>

            <span>Low Priority</span>
          </div>
        </div>

        <div className="alert-list">
          {(alerts.alerts || []).map(
            (alert, index) => (
              <div
                className={`alert-item ${getSeverityClass(
                  alert.severity
                )}`}
                key={index}
              >
                <div className="alert-symbol">
                  {alert.severity === "High"
                    ? "🔴"
                    : alert.severity === "Medium"
                      ? "🟠"
                      : "🟡"}
                </div>

                <div>
                  <div className="alert-title">
                    <strong>
                      {alert.title}
                    </strong>

                    <span>
                      {alert.severity}
                    </span>
                  </div>

                  <p>
                    {alert.description}
                  </p>
                </div>
              </div>
            )
          )}
        </div>
      </section>
    );
  };

  // ============================================================
  // COPILOT PANEL
  // ============================================================

  const CopilotPanel = () => (
    <section className="panel copilot-panel">
      <div className="panel-header">
        <div>
          <h2>🤖 AI Legal Copilot</h2>

          <p>
            Ask questions about the currently analyzed
            contract.
          </p>
        </div>

        <span className="copilot-status">
          ●{" "}
          {analysis
            ? "Contract Connected"
            : "No Contract"}
        </span>
      </div>

      <div className="copilot-suggestions">
        <button
          onClick={() =>
            askCopilot("Summarize this contract")
          }
          disabled={!analysis || copilotLoading}
        >
          Summarize contract
        </button>

        <button
          onClick={() =>
            askCopilot("What are the risks?")
          }
          disabled={!analysis || copilotLoading}
        >
          Find risks
        </button>

        <button
          onClick={() =>
            askCopilot(
              "What obligations exist?"
            )
          }
          disabled={!analysis || copilotLoading}
        >
          Find obligations
        </button>

        <button
          onClick={() =>
            askCopilot(
              "Which clauses are missing?"
            )
          }
          disabled={!analysis || copilotLoading}
        >
          Find missing clauses
        </button>
      </div>

      <div className="copilot-box">
        <div className="copilot-title">
          🤖 Ask your contract a question
        </div>

        <textarea
          value={copilotQuestion}
          onChange={(e) =>
            setCopilotQuestion(
              e.target.value
            )
          }
          placeholder={
            analysis
              ? "Example: What are the main risks in this agreement?"
              : "Analyze a contract first..."
          }
          rows="4"
        />

        <button
          className="copilot-button"
          onClick={() => askCopilot()}
          disabled={
            copilotLoading ||
            !copilotQuestion.trim() ||
            !analysis
          }
        >
          {copilotLoading
            ? "Thinking..."
            : "Ask Copilot"}
        </button>
      </div>

      {copilotAnswer && (
        <div className="copilot-answer">
          <div className="answer-icon">
            🤖
          </div>

          <div>
            <h3>Copilot Response</h3>

            <p>{copilotAnswer}</p>
          </div>
        </div>
      )}
    </section>
  );

  // ============================================================
  // EMPTY WELCOME
  // ============================================================

  const Welcome = () => (
    <div className="welcome">
      <div className="welcome-icon">
        ⚖️
      </div>

      <h2>
        Enterprise Legal Intelligence
      </h2>

      <p>
        Upload a legal contract to analyze clauses,
        identify contractual risks, evaluate compliance,
        extract obligations and interact with the AI
        Legal Copilot.
      </p>

      <div className="feature-row">
        <div>📑 Clause Detection</div>
        <div>⚠️ Risk Intelligence</div>
        <div>🛡️ Compliance</div>
        <div>🚨 Alerts</div>
        <div>🤖 AI Copilot</div>
      </div>
    </div>
  );

  // ============================================================
  // DASHBOARD VIEW
  // ============================================================

  const DashboardView = () => (
    <>
      <UploadCard />
      <ErrorBox />

      {!analysis ? (
        <Welcome />
      ) : (
        <>
          <ContractInfo />
          <Stats />

          <div className="two-column">
            <RiskPanel />
            <CompliancePanel />
          </div>

          <ClausePanel />

          <div className="two-column">
            <RisksPanel />
            <ObligationsPanel />
          </div>

          <AlertsPanel />

          <CopilotPanel />
        </>
      )}
    </>
  );

  // ============================================================
  // CONTRACTS VIEW
  // ============================================================

  const ContractsView = () => (
    <>
      <UploadCard />
      <ErrorBox />

      {analysis ? (
        <>
          <ContractInfo />

          <section className="panel">
            <div className="panel-header">
              <div>
                <h2>
                  📄 Contract Information
                </h2>

                <p>
                  Currently analyzed legal document.
                </p>
              </div>
            </div>

            <div className="contract-info">
              <div>
                <span>FILE</span>
                <strong>
                  {analysis.filename}
                </strong>
              </div>

              <div>
                <span>PAGES</span>
                <strong>
                  {analysis.pages}
                </strong>
              </div>

              <div>
                <span>CHARACTERS</span>
                <strong>
                  {analysis.text_length}
                </strong>
              </div>
            </div>
          </section>

          <section className="panel">
            <div className="panel-header">
              <div>
                <h2>
                  📃 Extracted Contract Text
                </h2>

                <p>
                  Text extracted from the uploaded
                  PDF.
                </p>
              </div>
            </div>

            <div className="empty-state">
              {analysis.text}
            </div>
          </section>
        </>
      ) : (
        <Welcome />
      )}
    </>
  );

  // ============================================================
  // RISK VIEW
  // ============================================================

  const RiskView = () => (
    <>
      {!analysis ? (
        <>
          <UploadCard />
          <ErrorBox />
          <Welcome />
        </>
      ) : (
        <>
          <Stats />
          <RiskPanel />
          <RisksPanel />
        </>
      )}
    </>
  );

  // ============================================================
  // COMPLIANCE VIEW
  // ============================================================

  const ComplianceView = () => (
    <>
      {!analysis ? (
        <>
          <UploadCard />
          <ErrorBox />
          <Welcome />
        </>
      ) : (
        <>
          <Stats />
          <CompliancePanel />
        </>
      )}
    </>
  );

  // ============================================================
  // ALERT VIEW
  // ============================================================

  const AlertView = () => (
    <>
      {!analysis ? (
        <>
          <UploadCard />
          <ErrorBox />
          <Welcome />
        </>
      ) : (
        <AlertsPanel />
      )}
    </>
  );

  // ============================================================
  // COPILOT VIEW
  // ============================================================

  const CopilotView = () => (
    <>
      {!analysis && (
        <div className="error-box">
          Please upload and analyze a contract first.
        </div>
      )}

      <CopilotPanel />
    </>
  );

  // ============================================================
  // MAIN CONTENT
  // ============================================================

  const renderView = () => {
    switch (activeView) {
      case "Contracts":
        return <ContractsView />;

      case "Risk Intelligence":
        return <RiskView />;

      case "Compliance":
        return <ComplianceView />;

      case "Alert Center":
        return <AlertView />;

      case "AI Copilot":
        return <CopilotView />;

      default:
        return <DashboardView />;
    }
  };

  // ============================================================
  // APP
  // ============================================================

  return (
    <div className="app">
      <Sidebar />

      <main className="main">
        <Topbar />

        {renderView()}
      </main>
    </div>
  );
}

export default App;