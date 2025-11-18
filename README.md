# Money Education Platform

AI-powered online education platform with personalized learning paths, real-time feedback, and automated assessment.

## 🎯 Project Overview

Money Education Platform is an advanced online learning system that leverages AI tutoring (powered by Claude) to provide personalized educational experiences. Instructors can easily create courses, while learners interact with AI for effective, adaptive learning.

## 🚀 Key Features

### For Learners
- **AI Tutor**: Personalized assistance powered by Claude API
- **Adaptive Learning**: Content adjusts to your skill level and learning pace
- **Interactive Exercises**: Auto-graded assignments with instant feedback
- **Live Classes**: Real-time video sessions with instructors
- **Progress Tracking**: Detailed analytics and learning paths
- **Certificates**: Earn verified certificates upon course completion

### For Instructors
- **Course Builder**: Intuitive drag-and-drop interface
- **Content Management**: Videos, quizzes, assignments, live sessions
- **Auto-Grading**: AI-powered evaluation system
- **Analytics Dashboard**: Track student progress and engagement
- **Revenue Sharing**: Competitive 70-80% revenue share

### For Organizations
- **Team Management**: Assign courses and track team progress
- **Custom Learning Paths**: Tailored curriculum for your organization
- **LMS Integration**: Connect with existing learning systems
- **SSO Support**: Enterprise authentication

## 🛠 Technology Stack

### Backend
- **Framework**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Task Queue**: Celery with Redis broker
- **API**: RESTful + WebSocket for real-time features

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Styling**: TailwindCSS 3.4+
- **UI Components**: Radix UI, Headless UI
- **State Management**: Zustand
- **Forms**: React Hook Form with Zod validation

### AI & ML
- **AI Tutor**: Anthropic Claude API (Sonnet 4)
- **Speech**: Whisper (transcription), ElevenLabs (TTS)
- **Learning Engine**: Scikit-learn for adaptive algorithms

### Media
- **Video Platform**: Mux (streaming, encoding)
- **Video Processing**: FFmpeg
- **Live Streaming**: LiveKit

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Reverse Proxy**: Nginx
- **Monitoring**: Prometheus, Grafana
- **Deployment**: AWS/GCP recommended

### Payments
- **International**: Stripe
- **Korea**: Toss Payments (토스페이먼츠)

## 📦 Project Structure

```
money-education-platform/
├── backend/                 # Django backend
│   ├── src/
│   │   ├── ai/             # AI tutor system
│   │   ├── learning/       # Adaptive learning engine
│   │   ├── assessment/     # Auto-evaluation system
│   │   ├── courses/        # Course management
│   │   ├── users/          # User management
│   │   ├── payments/       # Payment integration
│   │   └── certificates/   # Certificate generation
│   ├── requirements.txt
│   └── manage.py
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── app/           # Next.js pages (App Router)
│   │   ├── lib/           # Utilities
│   │   ├── hooks/         # Custom hooks
│   │   └── types/         # TypeScript types
│   ├── package.json
│   └── next.config.js
├── docker/                # Docker configurations
├── docs/                  # Documentation
└── scripts/               # Utility scripts
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Environment Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd money-education-platform
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

3. **Frontend Setup**
```bash
cd frontend
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your configuration

# Start development server
npm run dev
```

4. **Start Redis & Celery**
```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Celery Worker
cd backend
celery -A config worker -l info

# Terminal 3: Celery Beat (for scheduled tasks)
celery -A config beat -l info
```

### Using Docker

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📖 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

## 🔑 Environment Variables

### Backend (.env)
```
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/education_db
REDIS_URL=redis://localhost:6379/0
ANTHROPIC_API_KEY=your-claude-api-key
STRIPE_SECRET_KEY=your-stripe-key
TOSS_SECRET_KEY=your-toss-key
MUX_TOKEN_ID=your-mux-token
MUX_TOKEN_SECRET=your-mux-secret
LIVEKIT_API_KEY=your-livekit-key
LIVEKIT_API_SECRET=your-livekit-secret
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_STRIPE_KEY=your-stripe-public-key
```

## 💰 Pricing Tiers

### For Learners

**Free Tier**
- Access to free courses
- Basic AI tutor (10 questions/month)
- Community forum access

**Pro ($19/month)**
- Unlimited course access
- Unlimited AI tutor
- Certificate generation
- Offline downloads
- Priority support

**Team ($49/month/user)**
- Team management dashboard
- Learning path assignment
- Progress reports
- Admin tools

### For Instructors
- Standard: 30% platform fee
- Premium: 20% platform fee
- Monthly payouts

## 🗺 Development Roadmap

### Phase 1 (6 weeks) - MVP
- [x] Project setup
- [ ] Course builder
- [ ] Video player
- [ ] User authentication
- [ ] Basic course viewing

### Phase 2 (4 weeks) - AI Integration
- [ ] AI tutor system
- [ ] Q&A interface
- [ ] Conversation history
- [ ] Personalized responses

### Phase 3 (4 weeks) - Adaptive Learning
- [ ] Learning analytics
- [ ] Adaptive content delivery
- [ ] Quiz system
- [ ] Progress tracking

### Phase 4 (3 weeks) - Monetization
- [ ] Stripe integration
- [ ] Toss Payments integration
- [ ] Subscription management
- [ ] Certificate generation

### Phase 5 (3 weeks) - Advanced Features
- [ ] Live classes (LiveKit)
- [ ] Analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Team/Enterprise features

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test

# E2E tests
npm run test:e2e
```

## 📊 Revenue Goals

- **3 months**: $3,000 MRR (200 Pro users)
- **6 months**: $15,000 MRR (including course sales)
- **12 months**: $50,000+ MRR (with B2B contracts)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- Documentation: [docs/](./docs/)
- Issues: GitHub Issues
- Email: support@money-education.com

## 🙏 Acknowledgments

- Powered by [Anthropic Claude](https://www.anthropic.com/)
- Video by [Mux](https://mux.com/)
- Live streaming by [LiveKit](https://livekit.io/)

---

Built with ❤️ for better education
