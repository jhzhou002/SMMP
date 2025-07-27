# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SMMP (Smart Multi-Model Platform) is a multi-agent AI software development platform that simulates a complete software development team workflow. The platform uses natural language to drive automated development processes from requirement analysis to code implementation.

## Architecture

### Core Components
- **Frontend**: Vue 3 + Vite + Element Plus + Tailwind CSS
- **Backend**: Node.js + Express + TypeScript  
- **Multi-Agent Framework**: MetaGPT + LangChain
- **Database**: PostgreSQL + Redis
- **Deployment**: 宝塔面板 + PM2 + Nginx

### Project Structure
```
ai-devteam/
├── frontend/                    # Vue frontend application
│   ├── src/
│   │   ├── components/         # Shared components
│   │   ├── views/             # Page components
│   │   ├── stores/            # Pinia state management
│   │   ├── services/          # API services
│   │   └── utils/             # Utility functions
├── backend/                     # Node.js backend service
│   ├── src/
│   │   ├── controllers/       # Controllers
│   │   ├── services/          # Business logic
│   │   ├── models/            # Data models
│   │   ├── routes/            # Route definitions
│   │   ├── middleware/        # Middleware
│   │   ├── agents/            # Agent management
│   │   └── utils/             # Utility functions
├── agents/                      # Python agent services
│   ├── roles/                 # Role definitions
│   ├── workflows/             # Workflows
│   └── requirements.txt
```

## Development Commands

### Frontend Development
```bash
cd frontend
npm install                    # Install dependencies
npm run dev                   # Start development server
npm run build                 # Build for production
```

### Backend Development  
```bash
cd backend
npm install                   # Install dependencies
npm run dev                   # Start development server
npm run build                 # Build TypeScript to JavaScript
```

### Python Agent Services
```bash
cd agents
pip install -r requirements.txt  # Install Python dependencies
python main.py --project-id test --config '{"description":"测试项目"}'  # Test agent execution
```

### Local Development Setup
```bash
# 1. Start database services
sudo systemctl start postgresql
sudo systemctl start redis

# 2. Start backend service
cd backend && npm run dev

# 3. Start frontend service  
cd frontend && npm run dev

# 4. Test Python agents
cd agents && python main.py --project-id test --config '{"description":"测试项目"}'
```

## Key Technical Patterns

### Multi-Agent Communication
- Node.js backend orchestrates Python agent processes using child_process.spawn()
- Real-time communication via WebSocket (Socket.IO) for live project updates
- Agents send JSON messages to stdout which are parsed by the AgentOrchestrator

### State Management
- Frontend uses Pinia for centralized state management
- Real-time project status updates through WebSocket connections
- Agent logs and progress tracked in PostgreSQL database

### Agent Workflow
1. ProjectController receives new project request
2. AgentOrchestrator spawns Python process with MetaGPT
3. Custom roles (ProductManager, Architect, Engineer) execute in sequence
4. Progress updates sent via stdout to Node.js backend
5. Real-time updates broadcasted to frontend via WebSocket

### Database Schema
- `projects`: Main project records with status tracking
- `project_files`: Generated code files by agents
- `agent_logs`: Detailed agent execution logs
- `users`: User management (optional)

## Environment Requirements

- Node.js >= 18.0.0
- Python >= 3.9
- PostgreSQL >= 13
- Redis >= 6.0
- Git

## Deployment

The platform is designed for deployment using 宝塔面板 (BT Panel) with:
- PM2 for process management
- Nginx for reverse proxy and static file serving
- PostgreSQL and Redis as data stores

## Testing

API endpoints can be tested using curl:
```bash
# Create new project
curl -X POST http://localhost:3001/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "待办事项应用", "description": "创建一个简单的待办事项管理应用", "projectType": "web_app", "requirements": ["用户认证", "任务管理", "优先级设置"]}'

# Check project status  
curl http://localhost:3001/api/projects/{project_id}
```

## Code Conventions

- TypeScript for backend with strict type checking
- Vue 3 Composition API for frontend components
- Python follows MetaGPT framework patterns for agent definitions
- JSON-based communication protocol between Node.js and Python processes
- WebSocket events use `project:{id}:{event}` naming convention