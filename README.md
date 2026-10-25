# Weather Chat Bot

Advanced weather chatbot with AI, forecast, dashboard, admin panel, PostgreSQL, Redis, Docker, Render, and Vercel support.

## Features
- AI-powered weather assistant using OpenAI
- Real weather API using OpenWeatherMap
- 5-day forecast
- User registration and login
- JWT authentication
- Chat history per user
- Admin dashboard with stats
- Admin user management
- PostgreSQL + Redis integration
- Docker Compose ready
- Render + Vercel deployment ready

## Tech Stack
- Backend: FastAPI
- Frontend: React + Vite
- Database: PostgreSQL
- Cache: Redis
- AI: OpenAI
- Weather API: OpenWeatherMap

## Quick Start

### 1) Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Update `.env` with your values:
- `OPENWEATHER_API_KEY`
- `OPENAI_API_KEY`
- `SECRET_KEY`

Then:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2) Frontend
```bash
cd frontend
npm install
npm run dev
```

Open:
- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs

### 3) Docker
```bash
docker-compose up --build
```

## Example Chat Queries
- Weather in Lahore
- Karachi weather
- Forecast for Dubai
- What's the weather in Islamabad?

## API Examples

### Register user
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Ali Khan","email":"ali@example.com","password":"secret123"}'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=ali@example.com&password=secret123"
```

### Chat
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"message":"Weather in Lahore"}'
```

## Deployment
### Render
Use `render.yaml` for backend deployment.

### Vercel
Deploy the `frontend` folder.
Set env:
```env
VITE_API_URL=https://your-render-url
```

## Notes
- Add rate limiting in production
- Add logging and monitoring
- Use HTTPS in production
- Move secrets to environment manager
