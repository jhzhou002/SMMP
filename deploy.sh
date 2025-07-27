#!/bin/bash

echo "开始部署AI-DevTeam平台..."

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then 
    echo "请使用root权限运行此脚本"
    exit 1
fi

# 1. 拉取最新代码
echo "拉取最新代码..."
git pull origin main

# 2. 安装/更新系统依赖
echo "检查系统依赖..."
which node || {
    echo "安装Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
}

which python3 || {
    echo "安装Python3..."
    apt-get update
    apt-get install -y python3 python3-pip
}

which pg_config || {
    echo "安装PostgreSQL..."
    apt-get install -y postgresql postgresql-contrib
}

which redis-server || {
    echo "安装Redis..."
    apt-get install -y redis-server
}

# 3. 配置数据库
echo "配置数据库..."
sudo -u postgres psql -c "CREATE USER ai_devteam_user WITH PASSWORD 'ai_devteam_pass';" 2>/dev/null || true
sudo -u postgres psql -c "CREATE DATABASE ai_devteam OWNER ai_devteam_user;" 2>/dev/null || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ai_devteam TO ai_devteam_user;" 2>/dev/null || true

# 4. 启动数据库服务
echo "启动数据库服务..."
systemctl start postgresql
systemctl enable postgresql
systemctl start redis-server
systemctl enable redis-server

# 5. 构建前端
echo "构建前端..."
cd frontend
npm install
npm run build
cd ..

# 6. 构建后端
echo "构建后端..."
cd backend
npm install
npm run build
cd ..

# 7. 安装Python依赖
echo "安装Python依赖..."
cd agents
pip3 install -r requirements.txt
cd ..

# 8. 安装PM2（如果未安装）
which pm2 || {
    echo "安装PM2..."
    npm install -g pm2
}

# 9. 创建必要的目录
mkdir -p logs
mkdir -p backend/logs
mkdir -p agents/logs

# 10. 设置权限
chown -R www-data:www-data .
chmod +x deploy.sh

# 11. 重启服务
echo "重启服务..."
pm2 stop ai-devteam-backend 2>/dev/null || true
pm2 start ecosystem.config.js --env production
pm2 save

# 12. 配置nginx（如果安装了宝塔面板）
if [ -d "/www/server/nginx" ]; then
    echo "检测到宝塔面板，请手动配置nginx站点"
    echo "站点目录：$(pwd)/frontend/dist"
    echo "反向代理：http://127.0.0.1:3001"
fi

echo ""
echo "部署完成！"
echo "前端访问地址：http://localhost:3000"
echo "后端API地址：http://localhost:3001"
echo ""
echo "查看日志："
echo "  pm2 logs ai-devteam-backend"
echo ""
echo "停止服务："
echo "  pm2 stop ai-devteam-backend"
echo ""
echo "重启服务："
echo "  pm2 restart ai-devteam-backend"