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
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            background-color: #4d4042; /* Set the page background color */
            background-image: url('bg.png'); /* Set the page background to bg.png */
            background-size: auto; /* Keep the original size of the background image */
            background-repeat: repeat; /* Repeat the image to fill the page */
        }
        h1 {
            color: #333;
        }
        .paper-card {
            background-color: #f9f9f9; /* Fallback background color */
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
            transition: transform 0.2s, box-shadow 0.2s; /* Smooth transition for hover effect */
            background-size: auto; /* Keep the original size of the background image */
            background-repeat: repeat; /* Allow the image to repeat to fill the card */
            background-position: center; /* Center the background image */
            background: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), url(''); /* Add a semi-transparent white overlay */
            background-blend-mode: overlay; /* Blend the overlay with the background image */
        }
        .paper-card:hover {
            transform: translateY(-5px); /* Lift effect on hover */
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2); /* Shadow on hover */
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
            transition: transform 0.2s, box-shadow 0.2s; /* Smooth transition for hover effect */
        }
        .category-chunk:hover {
            transform: translateY(-3px); /* Slightly smaller lift for categories */
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15); /* Slightly smaller shadow for categories */
        }
        .category-chunk:nth-child(1) { /* 1. Topic and Domain */
            background-color: #d3e3fd; /* Blue */
        }
        .category-chunk:nth-child(2) { /* 2. Previous Research and New Ideas */
            background-color: #e6d6fa; /* Purple */
        }
        .category-chunk:nth-child(3) { /* 3. Problem */
            background-color: #d4f8d9; /* Green */
        }
        .category-chunk:nth-child(4) { /* 4. Methods */
            background-color: #ffd7d5; /* Pink */
        }
        .category-chunk:nth-child(5) { /* 5. Results and Evaluation */
            background-color: #d3e3fd; /* Reuse Blue */
        }
    </style>
</head>
<body>
    <h1>$date Papers</h1>
    $paper_content
</body>
</html>
"""