#!/usr/bin/env python3
"""
Regenerate index.html with note badges.
"""

import os
from collections import defaultdict
from datetime import datetime
from string import Template
from loguru import logger

from index_temp import INDEX_TEMPLATE


def update_index_page(dates):
    """更新主页面，添加日期链接，按年/月/日组织"""
    # 组织日期为 year -> month -> days 结构
    date_structure = defaultdict(lambda: defaultdict(list))

    for date_str in dates:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            year = date_obj.year
            month = date_obj.month
            date_structure[year][month].append(date_str)
        except ValueError:
            logger.warning(f"Invalid date format: {date_str}")
            continue

    # 生成HTML结构
    html_content = ""
    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }

    # 按年份降序排列
    for year in sorted(date_structure.keys(), reverse=True):
        year_papers = sum(len(days) for days in date_structure[year].values())
        html_content += f'''
        <div class="year-container">
            <div class="year-header">
                <span>{year} ({year_papers} papers)</span>
                <span class="arrow">▼</span>
            </div>
            <div class="content">
        '''

        # 按月份降序排列
        for month in sorted(date_structure[year].keys(), reverse=True):
            days = date_structure[year][month]
            month_name = month_names[month]
            html_content += f'''
                <div class="month-container">
                    <div class="month-header">
                        <span>{month_name} {year} ({len(days)} papers)</span>
                        <span class="arrow">▼</span>
                    </div>
                    <div class="content">
                        <ul class="day-list">
            '''

            # 按日期降序排列
            for date_str in sorted(days, reverse=True):
                # Check if this date has notes
                has_notes = os.path.exists(f'dailies/notes/{date_str}.md')
                note_indicator = ' <span class="note-badge">📝</span>' if has_notes else ''
                html_content += f'                        <li><a href="dailies/pages/{date_str}.html">{date_str}{note_indicator}</a></li>\n'

            html_content += '''                        </ul>
                    </div>
                </div>
            '''

        html_content += '''            </div>
        </div>
        '''

    # 生成统计信息
    total_papers = len(dates)
    total_years = len(date_structure)
    stats = f"Total: {total_papers} papers across {total_years} year{'s' if total_years > 1 else ''}"

    # Count papers with notes
    notes_count = sum(1 for d in dates if os.path.exists(f'dailies/notes/{d}.md'))
    stats += f" | {notes_count} with notes 📝"

    # 使用 Template 进行替换
    template = Template(INDEX_TEMPLATE)
    index_html = template.substitute(
        date_structure=html_content,
        stats=stats
    )
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)


if __name__ == "__main__":
    pages_dir = 'dailies/pages'
    if os.path.exists(pages_dir):
        existing_dates = [f.split('.html')[0] for f in os.listdir(pages_dir) if f.endswith('.html')]
    else:
        existing_dates = []

    logger.info(f"Found {len(existing_dates)} dates")
    update_index_page(existing_dates)
    logger.success("Index page regenerated with note badges!")
