const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === 'production'
    ? '/ai-medical-record_zhizhenzhushou/' // <-- 这里替换成你的 GitHub 仓库名称
    : '/',
  outputDir: 'dist',
})
