const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === 'production'
    ? '/ai-medical-record/' // <-- 这里替换成你的 GitHub 仓库名称，例如 '/ai-medical-assistant-frontend/'
    : '/',
  outputDir: 'dist',
})
