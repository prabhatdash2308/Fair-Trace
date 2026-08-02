# ReviewGuard AI

**Enterprise AI Performance Review Platform**

ReviewGuard AI is a deterministic, explainable, and secure multi-agent platform designed to help organizations generate transparent and auditable AI-assisted employee performance reviews. It eliminates cognitive bias and standardizes evaluations across the enterprise.

## Core Capabilities
- **Radical Explainability**: Every AI decision, score, and bias alert is tied directly to source evidence.
- **Multi-Agent Pipeline**: Specialized LangGraph architecture strictly separates reasoning, extraction, and synthesis.
- **Enterprise Security**: SOC2 compliant, end-to-end encrypted, and private cloud deployment ready.
- **Premium UX**: High-information-density UI built for executives and managers, featuring zero layout shift and accessible enterprise tokens.

## Tech Stack
- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Zustand, React Query, Framer Motion
- **Backend**: FastAPI, PostgreSQL, SQLAlchemy, Alembic, LangGraph
- **Infrastructure**: Docker, JWT Authentication

## Production Deployment
ReviewGuard AI is built for scalable, zero-trust environments.

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- Python 3.12+

### Quick Start
1. Clone the repository.
2. Copy `.env.example` to `.env` and configure your enterprise SSO / LLM keys.
3. Start the backend services:
   ```bash
   docker-compose up -d
   docker-compose exec backend alembic upgrade head
   ```
4. Start the frontend:
   ```bash
   cd frontend
   npm install
   npm run build
   npm run preview
   ```

## Development Guidelines
We enforce strict architectural principles:
- **No placeholder UIs**: Real API capabilities drive all functionality.
- **Type Safety**: End-to-end type safety between FastAPI models and React interfaces.
- **Semantic Design**: Use strictly defined `surface`, `danger`, `success`, and `warning` tokens. Avoid legacy arbitrary colors.

## License
© 2026 ReviewGuard AI Inc. All rights reserved.
