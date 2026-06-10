import { useState } from "react";
import ReactMarkdown from "react-markdown";

export default function QueryPage() {
  const [fileName, setFileName] = useState("");
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  async function submitQuery() {
    setLoading(true);

    try {
        const res = await fetch(
        `http://127.0.0.1:8000/query?fileName=${encodeURIComponent(fileName)}&query=${encodeURIComponent(query)}`
        );

        // Error handling
        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.detail);
        }

        const data = await res.json();
        setResponse(data.response);
    }
    catch (err : any) {
        setResponse(`Error: ${err.message}`)
    }
    finally {
        setLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="container">
        <header className="header">
          <h1>RAG Project</h1>
          <span>Get answers from your documents</span>
        </header>

        <div className="card">
          <div className="query-row">
            <input
              className="file-input"
              placeholder="File Name"
              value={fileName}
              onChange={(e) => setFileName(e.target.value)}
            />

            <input
              className="query-input"
              placeholder="Query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />

            <button
              className="ask-button"
              disabled={loading}
              onClick={submitQuery}
            >
              {loading ? "..." : "Ask"}
            </button>
          </div>

          <div className="results-grid">
            <div className="answer-panel">
              <h3>ANSWER</h3>

              {loading ? (
                <p>Processing your query...</p>
              ) : (
                <ReactMarkdown>{response}</ReactMarkdown>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}