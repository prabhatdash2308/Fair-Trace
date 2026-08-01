# ReviewGuard AI

Enterprise-grade Bias-Aware 360° Performance Review Intelligence Platform.

## Requirements
- Docker Compose
- Node.js
- Python 3.12+

## Setup
1. Copy `.env.example` to `.env`.
2. Run `docker-compose up -d`.
3. Run `docker-compose exec backend alembic upgrade head`.
4. Run `docker-compose exec backend python seed.py`.
5. CD to `frontend`, run `npm install`, then `npm run dev`.
