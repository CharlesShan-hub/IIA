module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2021: true
  },
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended'
  ],
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false, // 禁用Babel配置文件检查
    sourceType: 'module',
    ecmaVersion: 2021
  },
  plugins: [
    'vue'
  ],
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    // 其他ESLint规则可以在这里添加
  },
  settings: {
    'import/resolver': {
      webpack: {
        config: 'vue.config.js'
      }
    }
  }
};