# Mike Ross AI: The Agentic Legal Associate

> **"I don't play the odds, I play the man... and the library."**
> *The AI Division of Pearson Specter Litt V2*

![Office View](web/public/hero-bg.png)

---

## 📖 Executive Summary
**Mike Ross AI** is a state-of-the-art intelligent legal agent designed to democratize access to justice. Built for **Delta Hacks 12** ("Best Use of Gemini"), it leverages advanced Retrieval Augmented Generation (RAG) to provide instant, cited, and actionable legal guidance.

Unlike standard LLMs that hallucinate laws or offer generic advice, Mike Ross AI utilizes a **LangGraph State Machine** architecture to deterministically route queries, verify claims against a vector database of **16,170 official legal documents**, and deliver results with the precision of a senior associate.

---

### The Origin Story: Why We Built This
Access to justice shouldn't be a luxury. The idea for Mike Ross AI was born when a close friend found themselves in a sudden legal bind. Unable to afford a **$400/hour retainer**, they turned to LLMs, which confidently provided **incorrect legal information**.

We watched them struggle, digging through endless, confusing government forums just to find a single PDF form. We realized the system wasn't broken—it was just inaccessible.

**Mike Ross AI** bridges this gap. It reads the law, cites its sources (down to the section number), and gives ordinary Canadians a fighting chance.

### The "Mike Ross" Philosophy
Like the character, this agent has a **photographic memory** (Vector Search) of the law. But it also knows its limits—it won't fake being a lawyer. If you need representation, it connects you to the Law Society. If you need a form, it fetches the official PDF. No shenanigans.

---

## ✨ Key Capabilities

### 1. 🧠 Autonomous Agentic Workflow (LangGraph)
We moved beyond simple "Chat with Data". The system uses a **State Graph** to reason about your intent:
*   **Complex Drafting:** "My wife cheated, can I keep the house?" → Queries Federal Divorce Act & Provincial Property Law → Synthesizes a cited strategy.
*   **Smart Form Retrieval:** "I need to evict a tenant for damage." → Identifies "Damage" intent → Retrieves official **N5 Form** direct link.
*   **Representation Routing:** "Find me a criminal lawyer in Toronto." → Semantic search for "Defense Attorney" → Connects to LSO Referral Service.

### 2. 📚 The "Brain": 16,170 Legal Documents
We rejected "Data Silos". We ingested over **16,000 pages** of Canadian Law into a single, unified **MongoDB Atlas Vector Store**:
*   **Federal Statutes:** *Criminal Code of Canada (C-46)*, *Divorce Act (C-3)*, *Income Tax Act*, *Excise Tax Act*.
*   **Provincial Statutes:** *Residential Tenancies Act* (Ontario, BC, Alberta).
*   **Benefit:** Enables Cross-Jurisdictional Querying (e.g., "How does Federal Bankruptcy affect Ontario Eviction?").

### 3. 🛡️ Enterprise-Grade Reliability
*   **Zero Hallucination Policy:** Every claim is backed by a retrieved context chunk. If the law isn't in the database, the agent admits it.
*   **Security:** API Keys managed via Railway/Vercel. Database access restricted via IP whitelisting.

---

## 🛠️ The Technical Stack (SOTA 2026)

| Component | Technology | Why We Chose It |
| :--- | :--- | :--- |
| **Reasoning Engine** | **Google Gemini 2.0 Flash** | Massive 1M+ token context window allowing for superior synthesis of long legal texts without "forgetting" the prompt instructions. |
| **Embeddings** | **Google Gecko (`text-embedding-004`)** | 768-dimensional dense vectors optimized for semantic retrieval reliability. |
| **Vector Database** | **MongoDB Atlas Search** | Native integration with our data layer. Uses HNSW (Hierarchical Navigable Small World) graphs for sub-second retrieval latency (0.4s avg). |
| **Orchestration** | **LangGraph** | Allows for cyclic, stateful workflows (Router -> Research -> Draft) rather than linear chains. |
| **Frontend** | **Next.js 14 + Tailwind** | "Suits" inspired dark/premium aesthetic with Vercel Analytics for performance tracking. |

---

## 🏗️ System Architecture

```mermaid
graph TD
    User -->|Query| Router{Intent Router}
    
    Router -->|ADVICE| Vector[Vector Search (Mongo Atlas)]
    Router -->|FORM| FormTool[Official PDF Finder]
    Router -->|SEARCH| LawyerTool[LSO Referral Service]
    
    Vector --> Generator[Gemini 2.0 Flash]
    FormTool --> Generator
    LawyerTool --> Generator
    
    Generator -->|Structured Response| Client
```

---

## 👥 The Partners
**Suleyman Kiani** | *Senior Name Partner*
*   **Role:** Full Stack Engineering & System Architecture
*   **Credentials:** BASc Honours Computer Science, M.Eng Computing & Software (McMaster University)
*   [LinkedIn](https://www.linkedin.com/in/suleyman-kiani/) | [GitHub](https://github.com/kianis4)

**Karim Elbasiouni** | *Name Partner*
*   **Role:** AI Research & Model Fine-Tuning
*   **Credentials:** 4th Year Software Engineering Student (McMaster University)
*   [LinkedIn](https://www.linkedin.com/in/karim-elbasiouni2/) | [GitHub](https://github.com/KarimElbasiouni)

---

> *"The only time success comes before work is in the dictionary."* — Harvey Specter

