INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Paper</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            margin: 10px 0;
        }
        a {
            text-decoration: none;
            color: #1a73e8;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Daily Paper</h1>
    <ul>
        $date_links
    </ul>
</body>
</html>
"""

SUBPAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$date Papers</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            background-color: #4d4042;
            background-image: url('bg.png');
            background-size: auto;
            background-repeat: repeat;
            overflow-x: hidden;
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
            width: 100%;
            margin-right: 20px;
            overflow-wrap: break-word;
        }
        .paper-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        .paper-card h2 {
            margin: 0 0 10px;
            font-size: 1.2em;
        }
        .paper-card p {
            margin: 5px 0;
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
        
        @media (max-width: 768px) {
            .paper-container {
                flex-direction: column;
            }
            .paper-card {
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
            }
            /* 移动设备上弹窗已经是居中显示，无需额外样式 */
        }
    </style>
</head>
<body>
    <h1>$date Papers</h1>
    $paper_content
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
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
                        feedbackElement.textContent = '答对了！';
                        feedbackElement.classList.add('correct');
                        feedbackElement.classList.remove('incorrect');
                    } else {
                        this.classList.add('incorrect');
                        feedbackElement.textContent = '答错了，再试一次！';
                        feedbackElement.classList.add('incorrect');
                        feedbackElement.classList.remove('correct');
                    }
                    
                    feedbackElement.style.display = 'block';
                });
            });
        });
    </script>
</body>
</html>
"""