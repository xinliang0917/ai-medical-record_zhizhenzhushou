// frontend/.eslintrc.js

module.exports = {
  root: true,
  env: {
    node: true
  },
  'extends': [
    'plugin:vue/vue3-essential', // 或者 plugin:vue/vue3-recommended
    'eslint:recommended'
    // 如果你选择了 TypeScript，请保留或添加以下行：
    // '@vue/typescript/recommended'
    // 如果你使用了 Prettier，请保留或添加以下行：
    // 'plugin:prettier/recommended'
  ],
  parserOptions: {
    // 确保使用 @babel/eslint-parser 作为解析器
    parser: '@babel/eslint-parser',
    // 关键修复：告诉 @babel/eslint-parser 不需要查找 Babel 配置文件
    // 这对于像 babel.config.js 这样的文件特别有用
    requireConfigFile: false
  },
  rules: {
    // 根据你的需要添加或修改规则
    // 例如，开发环境下允许 console.log
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off'
    // ... 其他规则
  }
}