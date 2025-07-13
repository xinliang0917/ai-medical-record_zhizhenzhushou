<template>
  <canvas ref="canvas"></canvas>
</template>

<script>
export default {
  props: {
    // 验证码宽度
    width: {
      type: Number,
      default: 90
    },

    // 验证码高度
    height: {
      type: Number,
      default: 35
    },

    // 验证码字体
    codeFont: {
      type: String,
      default: '22px arial'
    },

    // 验证码类型   
    // calc：验证码为计算公式
    // code：验证码为数字大小写字母组合
    codeType: {
      type: String,
      default: 'code' //calc | code
    },

    // 验证码长度
    codeLength: {
      type: Number,
      default: 5
    },

    // 验证码大小写是否敏感
    strict: {
      type: Boolean,
      default: true
    },

    // 验证码计算范围
    calcRange: {
      type: Array,
      // 错误在这里，修改 default 为一个返回数组的函数
      default: () => [10, 20] // 修正点
    },
    // 验证码计算符号
    calcSymbol: {
      type: Array,
      // 错误在这里，修改 default 为一个返回数组的函数
      default: () => ['+', '-', '*'] // 修正点
    },

    // 背景干扰线数量
    lineCount: {
      type: Number,
      default: 5
    }
  },
  data() {
    return {
      canvas: null
    }
  },
  mounted() {
    const canvas = this.$refs.canvas
    canvas.width = this.width;
    canvas.height = this.height;

    this.canvas = canvas.getContext('2d');
    this.display()
  },
  methods: {
    display() {
      // 清空画布
      this.canvas.clearRect(0, 0, this.width, this.height);

      // 绘制验证码背景
      this.createLine();

      // 定义验证码属性
      this.canvas.font = this.codeFont
      this.canvas.textAlign = 'left';
      this.canvas.textBaseline = 'middle';

      // 绘制验证码
      let code = this.createCode()
      for (let i = 0; i < this.codeLength; i++) {
        this.canvas.save()
        this.canvas.fillStyle = this.randomColor()
        this.canvas.translate((i + 0.2) * this.width / this.codeLength, this.getRandom([this.height * 0.3, this.height * 0.7]))
        this.canvas.rotate(this.getRandom([-30, 30]) * Math.PI / 180)
        this.canvas.fillText(code[i], 0, 0);
        this.canvas.restore()
      }

    },

    // 画线
    createLine() {
      for (var i = 0; i < this.lineCount; i++) {
        let start = [-this.width / 2, this.width * 1.5]
        let end = [-this.height / 2, this.height * 1.5]

        this.canvas.lineWidth = this.getRandom([1, 3])
        this.canvas.strokeStyle = this.randomColor()
        this.canvas.beginPath();
        this.canvas.moveTo(this.getRandom(start), this.getRandom(end));
        this.canvas.lineTo(this.getRandom(start), this.getRandom(end));
        this.canvas.stroke();
      }
    },

    // 生成验证码
    createCode() {
      // 验证码为数字字符串
      if (this.codeType === 'code') {
        this.result = this.getString({ length: this.codeLength })
        this.$emit('getCode', this.strict ? this.result : this.result.toLocaleLowerCase())
        return this.result
      }

      // 验证码为计算公式
      const SUB = this.getRandom(this.calcRange),
        SUM = this.getArray(this.calcSymbol),
        MIN = this.getRandom(this.calcRange)
      this.result = eval(SUB + SUM + MIN);
      this.$emit('getCode', '' + this.result)
      return SUB + (SUM == '*' ? 'x' : SUM) + MIN;
    },

    /**
 * 生成指定范围内的随机数
 * * @param {array} [min,max] 数组包含最大值和最小值
 * @return {number}
 */
    getRandom([min = 0, max = 0]) {
      return Math.floor(Math.random() * (max - min + 1)) + min
    },

    /**
     * 返回随机生成指定长度的数字字母组合
     * * @param {number} length 生成的字符串长度 
     * @param {string} str 指定参与生成的字符串
     * @param {string} split 分隔位数
     * @param {string} join 分隔符 
     * @return {string}
     */
    getString({ length, str = 'abacdefghjklmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ0123456789', split = 0, join = '-' }) {
      let string = ''
      for (let i = 0; i < length; i++) {
        if (split > 0 && i !== 0 && i % split === 0) {
          string += join
        }
        string += str[this.getRandom([0, str.length - 1])]
      }
      return string
    },

    isArray: function (o) {
      if (!Array.isArray) {
        Array.isArray = function (o) {
          return Object.prototype.toString.call(o) === '[object Array]';
        };
      }
      return Array.isArray(o)
    },

    //随机获取数组中某一项
    getArray: function (arr) {
      if (!this.isArray(arr)) throw new Error('argument must be an Array')
      return arr[Math.floor(Math.random() * arr.length)];
    },

    // 生成随机色
    randomColor() {
      return `#${((Math.random() * (0xFFFFFF).toString(10)).toString(16)).slice(-6)}`
    },

  }
}
</script>