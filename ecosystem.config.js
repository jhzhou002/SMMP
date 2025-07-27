module.exports = {
  apps: [
    {
      name: 'ai-devteam-backend',
      script: './backend/dist/app.js',
      cwd: '/www/wwwroot/ai-devteam',
      instances: 1,
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'production',
        PORT: 3001,
        DB_HOST: 'localhost',
        DB_PORT: 5432,
        DB_NAME: 'ai_devteam',
        DB_USER: 'ai_devteam_user',
        DB_PASS: 'your_password',
        REDIS_URL: 'redis://localhost:6379',
        FRONTEND_URL: 'http://localhost:3000'
      },
      error_file: './logs/err.log',
      out_file: './logs/out.log',
      log_file: './logs/combined.log',
      time: true,
      max_memory_restart: '1G',
      node_args: '--max-old-space-size=1024'
    }
  ],

  deploy: {
    production: {
      user: 'root',
      host: 'your-server-ip',
      ref: 'origin/main',
      repo: 'https://github.com/jhzhou002/SMMP.git',
      path: '/www/wwwroot/ai-devteam',
      'pre-deploy-local': '',
      'post-deploy': 'npm install && npm run build && pm2 reload ecosystem.config.js --env production',
      'pre-setup': ''
    }
  }
}