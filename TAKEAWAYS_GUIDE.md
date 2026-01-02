# Daily Paper Takeaways Guide

## Overview
You can now add personal notes and takeaways to your daily paper summaries! These will appear as a beautiful styled section at the bottom of each day's HTML page.

## How to Add Your Takeaways

### Step 1: Create a Markdown File
For each day you want to add notes, create a markdown file in the `dailies/notes/` folder with the format:
```
dailies/notes/YYYY-MM-DD.md
```

**Example**: `dailies/notes/2026-01-02.md`

### Step 2: Write Your Content
Use standard markdown syntax to write your takeaways:

```markdown
# Today's Key Insights

After reading today's papers, here are my main takeaways:

## Common Themes
- Point 1
- Point 2

### Detailed Notes
Your detailed thoughts here...

> Important quote or insight

**Bold text** for emphasis
*Italic text* for subtle emphasis

## Action Items
- [ ] Task 1
- [ ] Task 2
```

### Step 3: Add Images (Optional)
1. Create an images folder for that specific date:
   ```bash
   mkdir -p dailies/images/YYYY-MM-DD/
   ```

2. Put your images in that folder:
   ```
   dailies/images/2026-01-02/screenshot.png
   dailies/images/2026-01-02/diagram.jpg
   ```

3. Reference them in your markdown with simple names:
   ```markdown
   ![My Screenshot](screenshot.png)
   ![Diagram](diagram.jpg)
   ```

   The system will automatically convert these to the correct paths!

### Step 4: Run the Script
When you run `daily_papers.py`, it will automatically:
- Look for a matching `.md` file for that date
- Convert the markdown to styled HTML
- Add it as a beautiful section after the papers

## Markdown Features Supported

### Text Formatting
- **Bold**: `**text**`
- *Italic*: `*text*`
- `Code`: `` `code` ``

### Headers
```markdown
# H1 Header
## H2 Header
### H3 Header
```

### Lists
```markdown
- Unordered list item
- Another item

1. Ordered list item
2. Another item
```

### Quotes
```markdown
> This is a blockquote
```

### Code Blocks
````markdown
```python
def example():
    print("Code with syntax highlighting")
```
````

### Links
```markdown
[Link text](https://example.com)
```

### Images
```markdown
![Alt text](image.png)
![Remote image](https://example.com/image.jpg)
```

## Example Structure

Your daily paper folder structure should look like:
```
dailies/
├── pages/                   # Auto-generated HTML files
│   ├── 2026-01-02.html
│   ├── 2026-01-03.html
│   └── ...
├── notes/                   # Your personal markdown notes
│   ├── 2026-01-02.md
│   ├── 2026-01-03.md
│   └── ...
└── images/                  # Images organized by date
    ├── 2026-01-02/
    │   ├── screenshot.png
    │   └── diagram.jpg
    └── 2026-01-03/
        └── photo.jpg
```

## Tips

1. **No need to modify HTML files** - They're regenerated automatically in `dailies/pages/`
2. **Markdown files are optional** - If no `.md` file exists in `dailies/notes/`, the page just shows the papers
3. **Images are optional** - You can have text-only takeaways
4. **Edit anytime** - Just edit the `.md` file in `dailies/notes/` and re-run the script
5. **Version control friendly** - Markdown files are easy to track in git
6. **Organized structure** - HTML pages, notes, and images are in separate folders for cleanliness

## Example Takeaway File

See `dailies/notes/2026-01-02.md` for a complete example with:
- Headers and subheaders
- Bullet points and numbered lists
- Bold and italic text
- Quotes
- Checkboxes
- Ratings and metadata

## Styling

The takeaway section has a beautiful purple gradient background with white content area. All markdown elements are styled consistently with the rest of the page.

---

**Need help?** Check the example file at `dailies/2026-01-02.md` or ask for assistance!
