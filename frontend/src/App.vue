<template>
  <div id="app">
    <el-container class="layout-container">
      <el-header>
        <div class="header-content">
          <h1>AI-DevTeam</h1>
          <nav>
            <router-link to="/" class="nav-link">项目管理</router-link>
            <router-link to="/about" class="nav-link">关于</router-link>
          </nav>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useProjectStore } from '@/stores/project'
import socketService from '@/services/socket'

const projectStore = useProjectStore()

onMounted(() => {
  socketService.connect()
  projectStore.fetchProjects()
})
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-content h1 {
  color: #409eff;
  margin: 0;
}

.nav-link {
  margin-left: 20px;
  text-decoration: none;
  color: #606266;
  font-weight: 500;
}

.nav-link:hover {
  color: #409eff;
}

.router-link-active {
  color: #409eff;
}
</style>