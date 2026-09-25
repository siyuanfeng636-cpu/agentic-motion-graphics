# HyperFrames & GSAP Engineering Recipes

**HyperFrames** 是由 HeyGen 开源的、专为 AI Agent 设计的确定性无头视频渲染框架。它通过标准 Web 技术栈（HTML、CSS、SVG、JavaScript/GSAP）构建视频，并通过无头 Chromium 环境实现高精度的逐帧渲染。

---

## 1. 核心架构与工程规范

### 1.1 目录结构
```text
my-project/
├── hyperframes.json      # 渲染核心配置文件
├── index.html            # 动效画布主文档
├── style.css             # 视觉样式、排版与绝对定位
├── script.js             # GSAP 时间轴控制
├── package.json          # 声明依赖 (GSAP, HyperFrames CLI)
├── assets/               # 矢量图形 (SVG)、图片、字体
└── data/
    └── timing.json       # 单词与场景时间戳
```

### 1.2 `hyperframes.json` 配置标准
```json
{
  "$schema": "https://hyperframes.dev/schema/v1.json",
  "entry": "index.html",
  "output": "dist/output.mp4",
  "width": 1920,
  "height": 1080,
  "fps": 30,
  "duration": 46.0,
  "concurrency": 4,
  "backgroundColor": "#0f172a"
}
```
* **竖屏格式（Short-form）**：`"width": 1080, "height": 1920`
* **方屏格式（Social Media）**：`"width": 1080, "height": 1080`
* **帧率推荐**：日常商业展示使用 `30fps`，极致丝滑动效使用 `60fps`。

---

## 2. 页面布局与 GSAP 编写范式

### 2.1 `index.html` 样板
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Motion Graphic</title>
  <link rel="stylesheet" href="style.css">
  <!-- 引入 GSAP 核心库 -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
</head>
<body>
  <div id="stage">
    <!-- 场景 1: Hero Section -->
    <section class="scene" id="scene-1">
      <div class="badge" id="pill-badge">🚀 新功能上线</div>
      <h1 class="headline" id="main-title">
        <span class="word" data-word="Opus">Opus</span>
        <span class="word" data-word="5.5">5.5</span>
        <span class="word" data-word="解决动效设计">解决动效设计</span>
      </h1>
      <div class="mockup-card" id="product-card">
        <img src="assets/ui_preview.png" alt="UI" />
      </div>
    </section>
  </div>
  <script src="script.js"></script>
</body>
</html>
```

### 2.2 `style.css` 核心样式
```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  background-color: #0b0f19;
  color: #ffffff;
  font-family: 'Inter', -apple-system, sans-serif;
  overflow: hidden;
  width: 1920px;
  height: 1080px;
}

#stage {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.scene {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
}
```

### 2.3 `script.js` 确定性时间轴编排
**关键原则**：必须关闭所有非确定性、随系统时钟（`requestAnimationFrame`）漂移的动效，全部统一通过主 `gsap.timeline({ paused: true })` 驱动：

```javascript
// 初始化主时间轴，保持暂停，交由 HyperFrames 逐帧步进
const masterTl = gsap.timeline({ paused: true });

// 加载外部 Whisper 时间戳对齐数据
async function initTimeline() {
  const timing = await fetch('./data/timing.json').then(r => r.json());

  // 场景 1 入场动画
  masterTl.to('#scene-1', { opacity: 1, duration: 0.3 }, 0);
  masterTl.from('#pill-badge', { y: -30, opacity: 0, scale: 0.8, duration: 0.4, ease: "back.out(1.7)" }, 0.2);

  // 遍历单词，精确在语音发音起始时间点做高亮
  timing.forEach(item => {
    const el = document.querySelector(`[data-word="${item.word}"]`);
    if (el) {
      masterTl.to(el, { color: "#6366f1", scale: 1.1, duration: 0.08 }, item.start);
      masterTl.to(el, { color: "#ffffff", scale: 1.0, duration: 0.12 }, item.end);
    }
  });

  // 产品卡片 3D 悬浮与缩放
  masterTl.from('#product-card', { 
    y: 80, 
    rotationX: 15, 
    opacity: 0, 
    duration: 0.8, 
    ease: "power3.out" 
  }, 1.2);

  // 暴露给 HyperFrames 渲染器的全局逐帧钩子
  window.seekTo = function(seconds) {
    masterTl.seek(seconds);
  };
  
  // 标记初始化完成
  window.__ANIMATION_READY__ = true;
}

initTimeline();
```

---

## 3. CLI 渲染指令与 Agent 视觉自检

### 3.1 语法与资产自检 (`lint`)
```bash
npx hyperframes lint
```
* 检查本地是否包含未引用的外部资源；
* 检查字体加载是否存在 FOUT（Flash of Unstyled Text）闪烁隐患；
* 校验全局总时长与帧率配置。

### 3.2 关键帧抽样自检 (`snapshot`)
由于 LLM 无法直接听看完整 MP4 视频，必须在执行完整渲染前，抽取代表性关键帧图片：
```bash
npx hyperframes snapshot --time 0.5,2.0,5.5,12.0,20.0 --output ./snapshots/
```
Agent 调用 `view_file` 工具查看生成的 PNG 截图，重点审查：
1. **排版是否有遮挡/截断**（文字是否超出屏幕外边距）；
2. **色彩与对比度**（背景色与主体前景文本是否清晰可读）；
3. **视觉层次（Visual Hierarchy）**：主要视觉元素是否居中醒目。

### 3.3 逐帧高精度无头渲染 (`render`)
```bash
npx hyperframes render \
  --entry index.html \
  --output dist/visual_render.mp4 \
  --fps 30 \
  --quality high
```

---

## 4. 常见避坑指南（Gotchas）

1. **字体加载竞态（Web Fonts Race）**：必须使用 CSS `font-display: block;` 并在 JavaScript 中通过 `document.fonts.ready` 确保字体完全解码就绪后再标记 `window.__ANIMATION_READY__ = true`。
2. **跨域阻断（CORS）**：HyperFrames 内部采用本地静态服务器，所有外部图片或字体尽量转存至本地 `assets/` 目录或转为 Base64 嵌入，避免网络波动导致逐帧渲染黑屏。
3. **缓动函数平滑度**：商业动效避免使用单一 `linear` 或默认 `ease`，多使用 `power3.out`（流畅减速）、`back.out(1.7)`（轻微回弹）和 `expo.out`（爆发入场）。
