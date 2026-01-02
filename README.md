# Daily Paper

An automated system for fetching, summarizing, and publishing daily AI research papers.

https://xinzhang-ops.github.io/daily_paper/index.html
https://xinzhang-ops.github.io/daily_paper/dailies/pages/2026-01-02.html

## 🎯 Features

- **Automated Paper Fetching**: Pulls top papers from HuggingFace daily
- **AI-Powered Summaries**: Uses Claude AI to generate 5-point structured summaries
- **Interactive Quizzes**: Auto-generated questions to test understanding
- **Visual Flowcharts**: SVG diagrams showing paper methodology
- **Personal Takeaways**: Add your own notes in markdown (NEW! ✨)
- **Multi-Platform**: Posts to Google Chat + generates GitHub Pages website

## 📁 Repository Structure

```
daily_paper/
├── dailies/
│   ├── pages/          # Generated HTML files (159 pages)
│   ├── notes/          # Your markdown takeaways (optional)
│   └── images/         # Images for your notes
├── bg/                 # Background images for papers
├── daily_papers.py     # Main script
├── daily_paper_utils.py # Utility functions
├── html_temps.py       # HTML templates
├── models.py           # AI model interface
└── summaries.jsonl     # Archive of all papers (5.2 MB)
```

## 🚀 Quick Start

### Running the Daily Script

```bash
python daily_papers.py
```

This will:
1. Fetch top 3 papers from HuggingFace
2. Download and analyze PDFs
3. Generate summaries, quizzes, and flowcharts
4. Post to Google Chat
5. Update GitHub Pages
6. Commit and push to git

### Adding Personal Notes

Want to add your own thoughts to a day's papers?

1. Create a markdown file:
   ```bash
   nano dailies/notes/2026-01-02.md
   ```

2. Write your notes:
   ```markdown
   # My Takeaways

   - Key insight 1
   - Key insight 2

   ![My diagram](diagram.png)
   ```

3. Add images (optional):
   ```bash
   mkdir dailies/images/2026-01-02
   cp your-image.png dailies/images/2026-01-02/
   ```

4. Re-run the script - your notes appear automatically!

See [QUICK_START.md](QUICK_START.md) for details.

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Quick reference for adding takeaways
- **[TAKEAWAYS_GUIDE.md](TAKEAWAYS_GUIDE.md)** - Complete guide with examples
- **[CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)** - Technical implementation details

## 🔧 Configuration

Set these environment variables in `.env`:

```
SPACE_ID=your_google_chat_space_id
KEY=your_google_chat_key
TEST=FALSE  # Set to TRUE to skip git push
```

## 📊 What You Get

### Daily HTML Pages
Each day's page includes:
- 3 AI-generated paper summaries
- Interactive quiz questions (3 per paper)
- Visual flowcharts of methodologies
- Your personal takeaways (if you add them)

### Example
Visit: `https://xinzhang-ops.github.io/daily_paper/dailies/pages/2026-01-02.html`

## 🛠️ Dependencies

```bash
pip install markdown requests pypdf loguru httplib2 python-dotenv
```

## 📈 Stats

- **159** days of papers tracked
- **5.2 MB** of paper summaries
- **Date range**: March 20, 2025 - January 2, 2026

## 🎨 Features Detail

### AI Summaries
Each paper is analyzed for:
1. 📘 Topic and Domain
2. 💡 Previous Research and New Ideas
3. ❓ Problem
4. 🛠️ Methods
5. 📊 Results and Evaluation

### Quiz System
- 3 multiple-choice questions per paper
- Instant feedback
- Tests comprehension of key concepts

### Personal Notes
- Write in simple markdown
- Supports all markdown features
- Beautiful purple gradient styling
- Images automatically sized and styled

## 🔗 Links

- **Live Site**: https://xinzhang-ops.github.io/daily_paper/
- **GitHub**: https://github.com/xinzhang-ops/daily_paper

## 📝 License

Personal project for research paper tracking.

---

**Made with Claude Code** 🤖
