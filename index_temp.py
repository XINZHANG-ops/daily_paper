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
            background-color: #f5f5f5;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .year-container {
            margin-bottom: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .year-header {
            background-color: #1a73e8;
            color: white;
            padding: 15px 20px;
            cursor: pointer;
            font-size: 1.2em;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
        }
        .year-header:hover {
            background-color: #1557b0;
        }
        .year-header .arrow {
            transition: transform 0.3s;
        }
        .year-header.collapsed .arrow {
            transform: rotate(-90deg);
        }
        .month-container {
            border-left: 3px solid #e8f0fe;
            margin-left: 20px;
        }
        .month-header {
            background-color: #e8f0fe;
            color: #1a73e8;
            padding: 12px 20px;
            cursor: pointer;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
        }
        .month-header:hover {
            background-color: #d2e3fc;
        }
        .month-header .arrow {
            transition: transform 0.3s;
            font-size: 0.8em;
        }
        .month-header.collapsed .arrow {
            transform: rotate(-90deg);
        }
        .day-list {
            list-style: none;
            padding: 10px 20px 10px 40px;
            margin: 0;
            background-color: #fafafa;
        }
        .day-list li {
            margin: 8px 0;
        }
        .day-list a {
            text-decoration: none;
            color: #333;
            display: block;
            padding: 8px 12px;
            border-radius: 4px;
            transition: background-color 0.2s;
        }
        .day-list a:hover {
            background-color: #e8f0fe;
            color: #1a73e8;
        }
        .day-list a::before {
            content: "📄 ";
            margin-right: 8px;
        }
        .content {
            display: block;
            max-height: 2000px;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
        }
        .content.collapsed {
            max-height: 0;
        }
        .stats {
            text-align: center;
            color: #666;
            margin-bottom: 20px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <h1>📚 Daily Paper Archive</h1>
    <div class="stats">$stats</div>
    $date_structure

    <script>
        // Toggle year sections
        document.querySelectorAll('.year-header').forEach(header => {
            header.addEventListener('click', function() {
                this.classList.toggle('collapsed');
                this.nextElementSibling.classList.toggle('collapsed');
            });
        });

        // Toggle month sections
        document.querySelectorAll('.month-header').forEach(header => {
            header.addEventListener('click', function() {
                this.classList.toggle('collapsed');
                this.nextElementSibling.classList.toggle('collapsed');
            });
        });

        // Expand most recent year and month by default
        const firstYear = document.querySelector('.year-header');
        const firstMonth = document.querySelector('.month-header');
        if (firstYear && firstMonth) {
            // They start expanded, so we don't need to do anything
            // But if you want them collapsed by default, uncomment:
            // firstYear.classList.add('collapsed');
            // firstYear.nextElementSibling.classList.add('collapsed');
        }
    </script>
</body>
</html>
"""
