
**Examples:**
- Add vector store schema and weighting logic
- Fix bug in Kubernetes event extraction
- Update README with hallucination article
- Refactor feedback handling for runtime tests

Avoid generic messages like "update", "fix", or "changes".

---

## Article: LLM Hallucinations vs. Vector Database Grounding

Large Language Models (LLMs) are powerful tools for generating and summarizing information, but they are prone to hallucinations—confidently producing incorrect or fabricated answers, especially when lacking context or when prompted with ambiguous queries.

### Why Do LLMs Hallucinate?
- LLMs generate text based on patterns in their training data, not on real-time facts or external knowledge bases.
- Without grounding, they may invent details, misinterpret technical terms, or provide plausible-sounding but false explanations.

### The Role of a Vector Database
A vector database stores embeddings of trusted documents (logs, events, official and internal documentation) and enables similarity search. By retrieving the most relevant, high-confidence context for a user query, it allows the system to:

- Provide the LLM with accurate, up-to-date, and company-specific information
- Filter and prioritize sources (e.g., internal docs > official docs > logs)
- Limit the LLM's context to only what is relevant, reducing the risk of hallucination

### Workflow for Reducing Hallucinations
1. Extract and index trusted sources in the vector database
2. For each query, retrieve the top-K most similar items (with threshold/weighting)
3. Only submit these validated contexts to the LLM
4. Optionally, check the LLM's response for integrity and consistency

### Benefits
- **Accuracy:** LLM answers are grounded in real, relevant data
- **Security:** Sensitive or company-specific knowledge is prioritized and controlled
- **Transparency:** The source of each answer can be traced and audited

### Conclusion
Combining LLMs with a vector database is a best practice for enterprise troubleshooting and knowledge management. It maximizes the value of generative AI while minimizing the risk of misleading or incorrect answers.
## Vector Database Schema & Weighting

The vector database stores embeddings and metadata for troubleshooting items (logs, events, documentation, etc.).

- **Schema Example:**
	- `embedding`: vector (array of floats)
	- `type`: source type (log, event, kube-doc, company-doc, etc.)
	- `content`: original text
	- `source`: file, URL, or object reference
	- `weight`: float (importance, e.g. company-doc > kube-doc > logs)
	- `ttl`: time-to-live (for lifecycle management)
	- `feedback`: user feedback (optional)

**Weighting:**
- Company documentation is assigned a higher weight than Kubernetes official docs, which are weighted higher than runtime logs/events.
- This influences similarity scoring and LLM context selection.

**Lifecycle (TTL):**
- Each entry can have a TTL (time-to-live) for automatic expiration and refresh.
- Useful for logs/events that become obsolete, or for updating documentation.

**Feedback & Runtime Testing:**
- User feedback can be stored to improve future retrieval and LLM answers.
- Runtime tests can be performed to validate the troubleshooting workflow and ensure data integrity.

## Example Schema (YAML)

```yaml
- embedding: [0.1, 0.2, ...]
	type: company-doc
	content: "Internal troubleshooting guide for X"
	source: "docs/internal/x.md"
	weight: 1.0
	ttl: 2592000  # seconds (30 days)
	feedback: "helpful"
- embedding: [0.3, 0.4, ...]
	type: kube-doc
	content: "Kubernetes official doc excerpt"
	source: "https://kubernetes.io/docs/..."
	weight: 0.8
	ttl: 2592000
	feedback: null
- embedding: [0.5, 0.6, ...]
	type: log
	content: "Pod crashed with OOMKilled"
	source: "kube_events.py"
	weight: 0.5
	ttl: 604800  # 7 days
	feedback: null
```
## Workflow (Flowchart)

```mermaid
flowchart TD
	A[Extract K8s logs/events] --> B[Index in vector DB (cosine/Jaccard)]
	B --> C{Similarity >= 0.73?}
	C -- Yes --> D[Select all above threshold]
	C -- No --> E[Select top-K]
	D & E --> F[Submit to LLM]
	F --> G[Check integrity]
	G --> H[Return validated answer]
```
# k8s-ai-troubleshooting

## Purpose

Python tools for Kubernetes troubleshooting with native extraction of logs/events, Helm/Helmfile parsing, vector indexing (cosine/Jaccard), top-K filtering, and selective submission to an LLM with integrity control.

## Project Structure

- `src/`: main Python modules
	- `kube_events.py`: extract Kubernetes logs/events
	- `vector_store.py`: cosine/Jaccard vector database
	- `llm_interface.py`: LLM interface and integrity check
- `scripts/`: automation scripts
- `helm/`: Helm/Helmfile charts and templates
- `docs/`: internal documentation, guides, links to kubernetes.io and GitHub
- `requirements.txt`: Python dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Extract Kubernetes logs/events with `src/kube_events.py`
2. Index and query data with `src/vector_store.py`
3. Filter top-K (threshold 0.73) and submit to the LLM via `src/llm_interface.py`
4. Check the integrity of responses to limit hallucinations

## Useful Links
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm](https://helm.sh/docs/)
- [Helmfile](https://github.com/roboll/helmfile)

## Security & Integrity
- Never submit sensitive information to the LLM
- Use integrity checks to prevent data leaks or incoherent responses
