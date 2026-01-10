SUBPAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${date} Papers</title>
    <style>
        * {
            box-sizing: border-box; /* 确保所有元素使用border-box模型 */
        }

        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            background-color: #4d4042;
            background-image: url('../../bg.png');
            background-size: auto;
            background-repeat: repeat;
            overflow-x: hidden;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        h1 {
            color: #333;
        }
        .paper-container {
            position: relative;
            display: flex;
            margin-bottom: 30px;
            justify-content: space-between;
            max-width: 100%;
            transition: all 0.3s ease;
        }
        
        /* 卡片容器样式 - 新增 */
        .card-deck {
            width: 100%;
            position: relative;
            margin-right: 20px;
            min-height: 600px; /* 改为最小高度而不是固定高度 */
            max-height: 90vh; /* 限制最大高度防止溢出 */
            height: auto; /* 自适应内容高度 */
            cursor: pointer; /* 增加指针样式提示可点击 */
        }
        
        /* 卡片通用样式 */
        .paper-card {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            transition: all 0.3s ease;
            background-size: auto;
            background-repeat: repeat;
            background-position: center;
            background: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), url('');
            background-blend-mode: overlay;
            overflow-wrap: break-word;
        }
        
        /* 轮播卡片样式 - 新增 */
        .card-deck .paper-card {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            box-sizing: border-box;
            height: 100%; /* 使用容器的100%高度 */
            transition: transform 0.5s ease, opacity 0.5s ease;
            overflow-y: auto; /* 允许垂直滚动 */
            overflow-x: hidden; /* 防止横向滚动 */
        }
        
        /* 非激活卡片的样式 - 新增 */
        .card-deck .paper-card:not(.active) {
            opacity: 0;
            pointer-events: none;
            transform: translateY(-10px);
        }
        
        /* 激活卡片的样式 - 新增 */
        .card-deck .paper-card.active {
            opacity: 1;
            pointer-events: auto;
            transform: translateY(0);
            z-index: 1;
        }
        
        /* 第一张卡片（文本内容）不需要滚动 */
        .card-deck .paper-card:first-child {
            overflow-y: auto;
        }

        .card-deck .paper-card:first-child:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* 第二张卡片（流程图）支持滚动 */
        .flowchart-card {
            text-align: center;
            background-color: #fff !important;
            overflow-y: auto !important; /* 允许垂直滚动 */
            overflow-x: hidden !important; /* 防止横向滚动 */
            padding: 20px; /* 添加内边距 */
            padding-bottom: 50px; /* 添加底部填充确保能看到底部 */
        }

        .flowchart-card svg {
            width: 100%;
            height: auto;
            max-width: 100%; /* 确保不超出容器宽度 */
            display: block; /* 防止底部空白 */
            margin: 0 auto; /* 居中显示 */
        }
        
        /* 传统卡片样式 */
        .paper-container > .paper-card {
            width: 100%;
            margin-right: 20px;
        }
        
        .paper-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .paper-card h2 {
            margin: 0 0 10px;
            font-size: 1.2em;
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
        }

        .paper-card p {
            margin: 5px 0;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        
        .paper-card a {
            color: #1a73e8;
            text-decoration: none;
        }
        
        .paper-card a:hover {
            text-decoration: underline;
        }
        
        .category-chunk {
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            transition: transform 0.2s, box-shadow 0.2s;
            word-wrap: break-word;
            overflow-wrap: break-word;
            overflow: hidden; /* 防止内容溢出 */
        }

        .category-chunk * {
            word-wrap: break-word;
            overflow-wrap: break-word;
            max-width: 100%;
        }
        
        .category-chunk:hover {
            transform: translateY(-3px);
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
        }
        
        .category-chunk:nth-child(1) {
            background-color: #d3e3fd;
        }
        
        .category-chunk:nth-child(2) {
            background-color: #e6d6fa;
        }
        
        .category-chunk:nth-child(3) {
            background-color: #d4f8d9;
        }
        
        .category-chunk:nth-child(4) {
            background-color: #ffd7d5;
        }
        
        .category-chunk:nth-child(5) {
            background-color: #d3e3fd;
        }
        
        /* 卡片计数器 - 新增 */
        .card-counter {
            position: absolute;
            top: 10px;
            right: 10px;
            background-color: rgba(0, 0, 0, 0.6);
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
            z-index: 2;
        }

        /* Quiz tabs and popup styles */
        .quiz-tabs {
            display: flex;
            flex-direction: column;
            position: sticky;
            top: 20px;
            align-self: flex-start;
            width: fit-content;
            min-width: 50px;
            margin-left: auto;
        }
        .quiz-tab {
            width: 50px;
            height: 50px;
            background-color: #1a73e8;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 15px;
            cursor: pointer;
            position: relative;
            font-weight: bold;
            font-size: 16px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s, box-shadow 0.2s;
            z-index: 10;
        }
        .quiz-tab:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        .quiz-popup {
            position: fixed; /* 改为固定定位，不随滚动而移动 */
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%); /* 居中显示 */
            width: 90%;
            max-width: 500px; /* 增加最大宽度，适应长内容 */
            max-height: 80vh; /* 限制最大高度 */
            overflow-y: auto; /* 内容过多时可滚动 */
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            display: none;
            z-index: 9999; /* 确保显示在最上层 */
        }
        
        /* 添加遮罩层，防止问题卡被其他内容遮挡 */
        .popup-backdrop {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 9998;
            display: none;
        }
        
        .popup-backdrop.active {
            display: block;
        }
        /* 使用JavaScript控制问题卡的显示和隐藏，不再使用hover */
        .quiz-popup.active {
            display: block;
        }
        .quiz-question {
            font-weight: bold;
            margin-bottom: 20px;
            color: #333;
            font-size: 18px;
            line-height: 1.5;
            word-wrap: break-word; /* 确保长单词自动换行 */
            overflow-wrap: break-word;
            hyphens: auto; /* 在必要时使用连字符 */
        }
        .quiz-choices {
            display: flex;
            flex-direction: column;
        }
        .quiz-choice {
            padding: 12px 15px;
            margin: 8px 0;
            border: 1px solid #ddd;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            color: #333;
            font-size: 15px;
            background-color: #f9f9f9;
            word-wrap: break-word; /* 确保长单词自动换行 */
            overflow-wrap: break-word;
            line-height: 1.4;
            text-align: left; /* 长文本左对齐 */
            display: block; /* 确保是块级元素 */
            white-space: normal; /* 允许自动换行 */
        }
        .quiz-choice:hover {
            background-color: #f0f0f0;
        }
        .quiz-choice.selected {
            background-color: #d3e3fd;
            border-color: #1a73e8;
        }
        .quiz-choice.correct {
            background-color: #d4f8d9;
            border-color: #0f9d58;
        }
        .quiz-choice.incorrect {
            background-color: #ffd7d5;
            border-color: #d93025;
        }
        .quiz-feedback {
            margin-top: 15px;
            padding: 10px;
            border-radius: 4px;
            display: none;
            font-weight: bold;
            text-align: center;
        }
        .quiz-feedback.correct {
            background-color: #d4f8d9;
            color: #0f9d58;
            display: block;
            border: 1px solid #0f9d58;
        }
        .quiz-feedback.incorrect {
            background-color: #ffd7d5;
            color: #d93025;
            display: block;
            border: 1px solid #d93025;
        }
        
        /* 长文本选项的特殊样式 */
        .quiz-choice.long-text {
            font-size: 13px;
            line-height: 1.3;
            padding: 10px 12px;
        }
        
        /* 确保弹窗中的按钮文本不会溢出 */
        .quiz-choice button,
        .quiz-choice a {
            word-break: break-word;
            white-space: normal;
            text-align: left;
            width: 100%;
        }
        
        /* 适应超长选项文本 */
        @media (max-width: 500px) {
            .quiz-popup {
                width: 95%;
                padding: 12px;
            }
            .quiz-question {
                font-size: 15px;
                margin-bottom: 12px;
            }
            .quiz-choice {
                padding: 8px 10px;
                font-size: 13px;
                line-height: 1.3;
            }
            .quiz-feedback {
                font-size: 13px;
                padding: 8px;
            }
        }
        
        /* 中等屏幕设备（如平板） */
        @media (max-width: 1024px) {
            .card-deck {
                min-height: 500px;
            }

            .card-deck .paper-card {
                max-height: 88vh;
            }
        }

        /* 移动设备和小屏幕 */
        @media (max-width: 768px) {
            body {
                padding: 10px; /* 减少移动设备上的内边距 */
            }

            .paper-container {
                flex-direction: column;
            }

            .card-deck {
                margin-right: 0;
                margin-bottom: 40px;
                min-height: 400px; /* 移动设备上使用更小的最小高度 */
                height: auto; /* 自适应高度 */
            }

            .card-deck .paper-card {
                max-height: 85vh; /* 移动设备上限制更多 */
                font-size: 0.95em; /* 稍微减小字体 */
            }

            .paper-card h2 {
                font-size: 1.1em; /* 移动设备上调整标题大小 */
            }

            .paper-container > .paper-card {
                width: 100% !important;
                margin-bottom: 20px;
                margin-right: 0;
            }

            .quiz-tabs {
                width: 100%;
                flex-direction: row;
                flex-wrap: wrap;
                justify-content: flex-start;
                position: relative;
                margin-left: 0;
            }

            .quiz-tab {
                margin-right: 10px;
                margin-bottom: 10px;
                width: 45px; /* 移动设备上稍小的按钮 */
                height: 45px;
                font-size: 14px;
            }
        }

        /* 极小屏幕（如小手机） */
        @media (max-width: 480px) {
            body {
                padding: 5px;
            }

            .card-deck {
                min-height: 300px;
            }

            .card-deck .paper-card {
                max-height: 80vh;
                font-size: 0.9em;
                padding: 10px;
            }

            .paper-card h2 {
                font-size: 1em;
            }

            .category-chunk {
                padding: 8px;
                font-size: 0.9em;
            }

            .quiz-tab {
                width: 40px;
                height: 40px;
                font-size: 12px;
            }
        }

        /* Personal Takeaways Section Styles */
        .takeaways-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 30px;
            margin: 40px 0;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }

        .takeaways-section h2 {
            color: #ffffff;
            font-size: 2em;
            margin-bottom: 20px;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        .takeaways-content {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 8px;
            padding: 25px;
            line-height: 1.8;
            color: #333;
        }

        .takeaways-content h3 {
            color: #667eea;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        .takeaways-content img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 15px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .takeaways-content p {
            margin: 15px 0;
        }

        .takeaways-content ul, .takeaways-content ol {
            margin: 15px 0;
            padding-left: 30px;
        }

        .takeaways-content li {
            margin: 8px 0;
        }

        .takeaways-content blockquote {
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin: 20px 0;
            font-style: italic;
            color: #555;
            background-color: #f8f9fa;
            padding: 15px 20px;
            border-radius: 4px;
        }

        .takeaways-content code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #d73a49;
        }

        .takeaways-content pre {
            background-color: #f6f8fa;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
            border: 1px solid #e1e4e8;
        }

        .takeaways-content pre code {
            background-color: transparent;
            padding: 0;
            color: #333;
        }
    </style>
</head>
<body>
    <h1>${date} Papers</h1>
    ${paper_content}

    <!-- Personal Takeaways Section -->
    <div id="takeaways-container"></div>

    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

    <!-- MathJax for LaTeX rendering (only for takeaways section) -->
    <script>
        MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true,
                processEnvironments: true
            },
            options: {
                skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
            },
            startup: {
                pageReady: () => {
                    // Disable automatic processing - we'll only process takeaways manually
                    return Promise.resolve();
                }
            }
        };
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Load and render markdown takeaways
            const dateMatch = document.querySelector('h1').textContent.match(/(\d{4}-\d{2}-\d{2})/);
            if (dateMatch) {
                const date = dateMatch[1];
                const mdPath = `../notes/$${date}.md`;

                // Use XMLHttpRequest for better file:// protocol support
                const xhr = new XMLHttpRequest();
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4) {
                        console.log('XHR Status:', xhr.status, 'Response length:', xhr.responseText.length);

                        if (xhr.status === 200 || xhr.status === 0) {  // status 0 for file://
                            const markdown = xhr.responseText;

                            if (!markdown || markdown.trim().length === 0) {
                                console.log('Empty markdown file');
                                return;
                            }

                            console.log('Markdown loaded, length:', markdown.length);

                            // Check if marked is loaded
                            if (typeof marked === 'undefined') {
                                console.error('marked.js library not loaded');
                                return;
                            }

                            // Convert markdown to HTML
                            const htmlContent = marked.parse(markdown);
                            console.log('HTML converted, length:', htmlContent.length);

                            // Fix image paths
                            const fixedContent = htmlContent.replace(
                                /src="(?!http:\/\/|https:\/\/|\/|\.\.\/)([^"]+)"/g,
                                `src="../images/$${date}/$$1"`
                            );

                            // Wrap in styled divs
                            const wrappedHtml = `
                                <div class="takeaways-section">
                                    <h2>📝 My Takeaways</h2>
                                    <div class="takeaways-content">
                                        $${fixedContent}
                                    </div>
                                </div>
                            `;

                            document.getElementById('takeaways-container').innerHTML = wrappedHtml;
                            console.log('Takeaways section rendered');

                            // Trigger MathJax to render LaTeX equations
                            if (typeof MathJax !== 'undefined') {
                                MathJax.typesetPromise([document.getElementById('takeaways-container')])
                                    .then(() => {
                                        console.log('MathJax rendering complete');
                                    })
                                    .catch((err) => console.error('MathJax rendering error:', err));
                            }
                        } else {
                            console.log('XHR failed - Status:', xhr.status);
                        }
                    }
                };
                xhr.open('GET', mdPath, true);
                console.log('Loading markdown from:', mdPath);
                xhr.send();
            }

            // 创建遮罩层
            const backdrop = document.createElement('div');
            backdrop.className = 'popup-backdrop';
            document.body.appendChild(backdrop);
            
            // 获取所有问题标签
            const quizTabs = document.querySelectorAll('.quiz-tab');
            
            // 设置点击事件处理
            quizTabs.forEach(tab => {
                const popup = tab.querySelector('.quiz-popup');
                
                // 点击标签切换问题卡的显示状态
                tab.addEventListener('click', function(e) {
                    e.stopPropagation(); // 阻止事件冒泡
                    
                    // 如果当前问题卡已经显示，则隐藏它
                    if (popup.classList.contains('active')) {
                        popup.classList.remove('active');
                        backdrop.classList.remove('active');
                    } else {
                        // 先隐藏所有其他问题卡
                        document.querySelectorAll('.quiz-popup').forEach(p => {
                            p.classList.remove('active');
                        });
                        
                        // 将弹窗内容复制到页面最外层的弹窗中
                        document.body.appendChild(popup);
                        
                        // 显示当前问题卡和背景遮罩
                        popup.classList.add('active');
                        backdrop.classList.add('active');
                    }
                });
                
                // 确保点击问题卡内部时不会关闭问题卡
                popup.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            });
            
            // 点击遮罩层或页面任何其他位置时隐藏所有问题卡
            backdrop.addEventListener('click', closeAllPopups);
            document.addEventListener('click', closeAllPopups);
            
            function closeAllPopups() {
                document.querySelectorAll('.quiz-popup').forEach(popup => {
                    popup.classList.remove('active');
                });
                backdrop.classList.remove('active');
            }
            
            // 为每个选项添加点击事件
            document.querySelectorAll('.quiz-choice').forEach(choice => {
                choice.addEventListener('click', function() {
                    const choiceContainer = this.closest('.quiz-choices');
                    const popupContainer = this.closest('.quiz-popup');
                    const feedbackElement = popupContainer.querySelector('.quiz-feedback');
                    const correctAnswer = popupContainer.getAttribute('data-answer');
                    
                    // 重置所有选项
                    choiceContainer.querySelectorAll('.quiz-choice').forEach(c => {
                        c.classList.remove('selected', 'correct', 'incorrect');
                    });
                    
                    // 标记当前选项为已选
                    this.classList.add('selected');
                    
                    // 检查是否正确
                    if (this.getAttribute('data-value') === correctAnswer) {
                        this.classList.add('correct');
                        feedbackElement.textContent = '✔️ Correct！';
                        feedbackElement.classList.add('correct');
                        feedbackElement.classList.remove('incorrect');
                    } else {
                        this.classList.add('incorrect');
                        feedbackElement.textContent = '❌ Wrong！';
                        feedbackElement.classList.add('incorrect');
                        feedbackElement.classList.remove('correct');
                    }
                    
                    feedbackElement.style.display = 'block';
                });
            });
            
            // 卡片轮播功能 - 新增
            const cardDecks = document.querySelectorAll('.card-deck');
            
            cardDecks.forEach(cardDeck => {
                const cards = cardDeck.querySelectorAll('.paper-card');
                const counter = cardDeck.querySelector('.card-counter');
                let currentIndex = 0;
                const totalCards = cards.length;
                
                // 更新计数器显示
                function updateCounter() {
                    if (counter) {
                        counter.textContent = `$${currentIndex + 1}/$${totalCards}`;
                    }
                }
                
                // 显示指定索引的卡片
                function showCard(index) {
                    // 处理循环
                    if (index >= totalCards) index = 0;
                    if (index < 0) index = totalCards - 1;
                    
                    // 更新当前索引
                    currentIndex = index;
                    
                    // 更新卡片显示
                    cards.forEach((card, i) => {
                        if (i === currentIndex) {
                            card.classList.add('active');
                        } else {
                            card.classList.remove('active');
                        }
                    });
                    
                    // 更新计数器
                    updateCounter();
                }
                
                // 下一张卡片
                function nextCard(e) {
                    e.stopPropagation(); // 防止事件冒泡导致问题卡关闭
                    showCard(currentIndex + 1);
                }
                
                // 为卡片容器添加点击事件
                cardDeck.addEventListener('click', function(e) {
                    // 检查点击是否发生在流程图卡片内部的滚动区域
                    // 如果是在滚动条上点击，不切换卡片
                    const targetCard = e.target.closest('.paper-card');
                    if (targetCard && targetCard.classList.contains('flowchart-card')) {
                        // 计算点击位置是否在滚动条区域
                        const rect = targetCard.getBoundingClientRect();
                        const isScrollbarClick = 
                            (e.clientY >= rect.top && e.clientY <= rect.bottom && e.clientX >= rect.right - 20 && e.clientX <= rect.right) ||
                            (e.clientX >= rect.left && e.clientX <= rect.right && e.clientY >= rect.bottom - 20 && e.clientY <= rect.bottom);
                        
                        if (!isScrollbarClick) {
                            nextCard(e);
                        }
                    } else {
                        nextCard(e);
                    }
                });
                
                // 键盘导航
                document.addEventListener('keydown', (e) => {
                    if (e.key === 'ArrowRight') {
                        showCard(currentIndex + 1);
                    } else if (e.key === 'ArrowLeft') {
                        showCard(currentIndex - 1);
                    }
                });
            });
        });
    </script>
</body>
</html>
"""