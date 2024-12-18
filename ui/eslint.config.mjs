// @ts-check
import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt({
  // Your custom configs here
  rules: {
    'vue/no-v-html': 'off',
    'vue/html-indent': ['error', 2], // HTML 缩进为 2 个空格
    'vue/max-attributes-per-line': ['error', {
      'singleline': 1, // 单行最多一个属性
    }],
    'vue/singleline-html-element-content-newline': 'off', // 单行元素内容不强制换行
    'vue/multiline-html-element-content-newline': 'error', // 多行元素内容强制换行
    // 'vue/name-property-casing': ['error', 'PascalCase'], // 组件名使用 PascalCase
    'vue/no-multiple-template-root': 'off', // 允许多个根模板
    'vue/no-unused-vars': 'error', // 禁止未使用的变量
    'vue/require-default-prop': 'off', // 允许没有默认值的 prop
    'vue/require-prop-types': 'error', // 强制要求 prop 类型定义
    'vue/component-tags-order': ['error', {
      'order': ['template', 'script', 'style'] // 强制组件标签顺序
    }],
    'vue/no-v-model-argument': 'off', // 允许 v-model 带参数
    'vue/attributes-order': 'error', // 强制属性顺序
    'vue/order-in-components': 'error', // 强制组件内属性顺序
    'vue/this-in-template': 'error', // 禁止在模板中使用 this
    'vue/no-template-shadow': 'error', // 禁止模板中变量名与外部变量名重名
    'vue/html-self-closing': ['error', {
      'html': {
        'void': 'always', // HTML 空标签总是自闭合
        'normal': 'never', // HTML 普通标签不自闭合
        'component': 'always' // 组件标签总是自闭合
      },
      'svg': 'always', // SVG 标签总是自闭合
      'math': 'always' // MathML 标签总是自闭合
    }],
    'vue/mustache-interpolation-spacing': ['error', 'always'], // Mustache 插值中强制空格
    'vue/no-spaces-around-equal-signs-in-attribute': 'error', // 属性中的等号两边不允许有空格
    'vue/no-useless-template-attributes': 'error', // 禁止无用的模板属性
    'vue/no-v-text-v-html-on-component': 'error', // 禁止在组件上使用 v-text 和 v-html
    'vue/prop-name-casing': ['error', 'camelCase'], // prop 名使用 camelCase
    'vue/require-direct-export': 'error', // 强制要求直接导出组件
    'vue/require-name-property': 'error', // 强制要求组件名
    '@typescript-eslint/no-unused-vars': 'error', // 禁止未使用的变量
    '@typescript-eslint/explicit-function-return-type': 'off', // 允许省略函数返回类型
  }
})
