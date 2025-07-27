<template>
  <div class="about">
    <el-card>
      <div class="about-content">
        <h1>AI-DevTeam</h1>
        <h2>智能软件开发团队</h2>
        
        <div class="description">
          <p>
            基于多智能体架构的AI软件开发平台，通过自然语言驱动，模拟完整的软件开发团队协作流程，
            自动完成从需求分析到代码实现的全流程开发。
          </p>
        </div>

        <div class="features">
          <h3>核心特性</h3>
          <ul>
            <li>🤖 多智能体协作开发</li>
            <li>🚀 自然语言驱动</li>
            <li>📊 实时进度跟踪</li>
            <li>💻 多项目类型支持</li>
            <li>🔄 完整开发流程</li>
          </ul>
        </div>

        <div class="tech-stack">
          <h3>技术栈</h3>
          <div class="tech-grid">
            <div class="tech-item">
              <h4>前端</h4>
              <p>Vue 3 + Vite + Element Plus + Tailwind CSS</p>
            </div>
            <div class="tech-item">
              <h4>后端</h4>
              <p>Node.js + Express + TypeScript</p>
            </div>
            <div class="tech-item">
              <h4>智能体框架</h4>
              <p>MetaGPT + LangChain</p>
            </div>
            <div class="tech-item">
              <h4>数据库</h4>
              <p>PostgreSQL + Redis</p>
            </div>
          </div>
        </div>

        <div class="version">
          <p>版本: 1.0.0</p>
          <p>作者: AI-DevTeam</p>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
// About页面组件
</script>

<style scoped>
.about {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.about-content {
  text-align: center;
  padding: 40px;
}

.about-content h1 {
  color: #409eff;
  margin-bottom: 8px;
  font-size: 2.5em;
}

.about-content h2 {
  color: #606266;
  margin-bottom: 30px;
  font-weight: normal;
}

.description {
  margin-bottom: 40px;
}

.description p {
  font-size: 16px;
  line-height: 1.6;
  color: #606266;
  margin: 0;
}

.features {
  margin-bottom: 40px;
  text-align: left;
}

.features h3 {
  color: #303133;
  margin-bottom: 20px;
  text-align: center;
}

.features ul {
  list-style: none;
  padding: 0;
  max-width: 400px;
  margin: 0 auto;
}

.features li {
  padding: 8px 0;
  font-size: 16px;
  color: #606266;
}

.tech-stack {
  margin-bottom: 40px;
}

.tech-stack h3 {
  color: #303133;
  margin-bottom: 20px;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  text-align: left;
}

.tech-item {
  padding: 20px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  background: #fafafa;
}

.tech-item h4 {
  color: #409eff;
  margin: 0 0 8px 0;
}

.tech-item p {
  color: #606266;
  margin: 0;
  font-size: 14px;
}

.version {
  border-top: 1px solid #ebeef5;
  padding-top: 20px;
  color: #909399;
}

.version p {
  margin: 4px 0;
}
</style>