# 🧠 HRMinds – AI-Powered HR Assistant

HRMinds is an intelligent, conversational HR assistant built using LangChain, Azure OpenAI GPT-4o, and PostgreSQL. It empowers HR teams to interact with employee data using natural language, perform critical HR calculations, and retrieve insights in real time.

---

## 🚀 Features

### ✅ Conversational SQL Agent
- Query HR databases in natural language.
- Automatically converts queries to SQL using LangChain's SQL Agent Toolkit.

### ✅ Live Streaming AI Responses
- Uses Azure OpenAI GPT-4o with Server-Sent Events (SSE) for real-time, streaming chat.
- Handles both database and general HR queries with a fallback mechanism.

### ✅ HR-Specific Calculations
- Perform analytics and KPIs like:
  - Attrition rate
  - Headcount trends
  - Average employee tenure
  - Training completion rates
  - Performance rating distributions

### ✅ Memory-Enhanced Conversations
- Uses LangChain `ConversationBufferMemory` to maintain contextual, multi-turn conversations.

---

## 🗃️ Connected Tables

- `employees`
- `departments`
- `job_positions`
- `leave_requests`
- `performance_reviews`
- `benefit_plans`
- `benefits_enrollment`
- `training_certifications`

---

## 🧰 Tech Stack

| Layer        | Technology                        |
|--------------|------------------------------------|
| Backend      | Python + LangChain                |
| LLM          | Azure OpenAI GPT-4o               |
| Database     | PostgreSQL (Azure)                |
| Frontend     | HTML, CSS, JS with SSE streaming  |
| Hosting      | Azure OpenAI, App Services        |

---

## 💬 Sample Queries

- "Show employees in the Engineering department."
- "What is the attrition rate for Q1 2024?"
- "List employees with outstanding performance."
- "Who completed Data Analysis training?"
- "Give me a count of leave requests this month."

---

## 📦 Setup & Deployment

1. Clone the repo.
2. Set your environment variables:
   - `OPENAI_API_KEY`
   - `AZURE_OPENAI_ENDPOINT`
   - `DATABASE_URL`
3. Run the backend:
   ```bash
   uvicorn app:app --reload
