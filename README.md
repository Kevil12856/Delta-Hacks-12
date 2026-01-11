# Mike Ross Juris: The AI Legal Associate

![Mike Ross Juris Banner](public/logo.png) (Place holder for logo/screenshot)

> **"I don't play the odds, I play the man... and the library."**
> *The AI Division of Pearson Specter Litt.*

---

## 📖 Introduction
**Mike Ross Juris** is not just a chatbot. It is a **State-of-the-Art Agentic Legal Associate** capable of autonomous research, document retrieval, and ethical routing.

Built for **Delta Hacks 12**, this system bridges the "Justice Gap" by providing free, high-precision legal guidance. Unlike standard LLMs that hallucinate laws, Mike Ross Juris uses a **Hybrid Router Architecture** to verify every claim against the *Official Criminal Code* and *Residential Tenancies Act*.

### Why "Mike Ross"?
Like the character, this agent has a photographic memory (**Vector Search**) of the law. But it also knows its limits—it won't fake being a lawyer. If you need representation, it finds you one.

---

## ✨ Key Features (The "Wow" Factor)

### 1. 🧠 Agentic RAG (The Brain)
We don't just "Search and Chat". We use **Semantic Routing** to classify your intent:
*   **Advice Mode:** Uses **Voyage AI** to search the Vector DB for specific statutes.
*   **Form Mode:** "Get me the N12 form." -> Returns distinctive, direct Government PDF links (no hallucinations).
*   **Representation Mode:** "I need a lawyer." -> Connects you to the Law Society referral service.

### 2. 📚 Unified Vector Space (The Memory)
We rejected "Data Silos". We ingested **10 Million+ Characters** of law into a **Single MongoDB Collection**:
*   *Criminal Code of Canada* (Federal)
*   *Income Tax Act* (Federal)
*   *Residential Tenancies Act* (Ontario)
*   **Benefit:** Enables Cross-Jurisdictional Querying (e.g. "How does Federal Bankruptcy affect Ontario Eviction?").

### 3. ⚖️ Ethical Guardrails
*   **No "Fake Lawyers":** The system refuses to recommend specific private firms. It only refers to regulatory bodies (LSO/Legal Aid).
*   **Strict Citations:** Every piece of advice cites the specific section of the act (e.g., *Section 48(1) RTA*).

### 4. 👔 Saul Goodman Mode (The Easter Egg)
*   Toggle the switch in the header.
*   *Spoiler:* "The law is a particular endeavour and has no room for shenanigans." (Try it yourself!)

---

## 🛠️ The Tech Stack (SOTA 2026)

| Component | Choice | Why? |
| :--- | :--- | :--- |
| **Reasoning Engine** | **Google Gemini 1.5 Flash** | Native Structured Outputs (Pydantic) & Massive Context Window for re-ranking. |
| **Embeddings** | **Voyage AI (`voyage-law-2`)** | Specialized legal model. Outperforms OpenAI `text-embedding-3` on statute retrieval. |
| **Orchestration** | **LangGraph** | A State Machine (not a Chain). Allows for cyclic routing, clarification loops, and tool calling. |
| **Database** | **MongoDB Atlas Vector Search** | **Metadata Filtering** + Vector Indexing = Millisecond retrieval speed. |
| **Frontend** | **Next.js + Tailwind** | "Suits" inspired dark/premium aesthetic. |

---

## 🏗️ Architecture Design

```mermaid
graph TD
    User -->|Query| Router{Intent Router}
    
    Router -->|ADVICE| Vector[Vector Search (Voyage/Mongo)]
    Router -->|FORM| FormTool[Official PDF Finder]
    Router -->|SEARCH| LawyerTool[Law Society Referral]
    
    Vector --> Generator[Gemini 1.5 Flash]
    FormTool --> Generator
    LawyerTool --> Generator
    
    Generator -->|Structured Response| Client
```

---

## 🚀 Impact & Scalability
*   **Current State:** Fully functional for Ontario Tenancy and Federal Criminal/Tax Law.
*   **Scalability:** The **Single Collection Strategy** allows us to add *British Columbia* or *New York* law simply by ingesting the text with a new `jurisdiction` tag—no code changes required.

---

## 💻 How to Run (Development)

1.  **Clone & Install**
    ```bash
    git clone https://github.com/your-repo/mike-ross-juris.git
    cd mike-ross-juris
    pip install -r requirements.txt
    cd web && npm install
    ```

2.  **Environment Secrets**
    Create a `.env` file in the root:
    ```bash
    GOOGLE_API_KEY=...
    MONGODB_URI=...
    VOYAGE_API_KEY=...
    ```

3.  **Run Backend**
    ```bash
    # From root directory
    uvicorn agent.server:app --host 0.0.0.0 --port 8000 --reload
    ```

4.  **Run Frontend**
    ```bash
    cd web
    npm run dev
    ```

5.  **Access App:** `http://localhost:3000`

---

## 🏆 For Judges: Why Mike Ross Juris?
*   **It's Actionable:** We don't just give advice; we give forms and phone numbers.
*   **It's Accurate:** Specialized Legal Embeddings > Generic GPT.
*   **It's Architected:** LangGraph State Machine > Simple LangChain.

> *"Next month, I'll drop the Saul Goodman Edition for all the real criminals out there."*
