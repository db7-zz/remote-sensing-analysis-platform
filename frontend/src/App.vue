<script setup lang="ts">
import { DataAnalysis, InfoFilled } from '@element-plus/icons-vue'
</script>

<template>
  <div class="app-shell">
    <header class="topbar">
      <RouterLink class="brand" to="/">
        <span class="brand-mark"><el-icon><DataAnalysis /></el-icon></span>
        <span>
          <strong>遥感影像智能分析平台</strong>
          <small>Remote Sensing Intelligence</small>
        </span>
      </RouterLink>
      <nav class="nav-links" aria-label="主导航">
        <RouterLink to="/">平台概览</RouterLink>
        <RouterLink to="/analysis">创建任务</RouterLink>
        <RouterLink to="/tasks">历史任务</RouterLink>
        <RouterLink to="/about"><el-icon><InfoFilled /></el-icon> 项目说明</RouterLink>
      </nav>
    </header>
    <main>
      <RouterView />
    </main>
    <footer>
      基于公开数据与公开模型构建的个人复现与工程化演示版本
    </footer>
  </div>
</template>
