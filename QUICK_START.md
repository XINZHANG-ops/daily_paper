# Quick Start: Adding Personal Takeaways

## TL;DR
1. Create `dailies/notes/YYYY-MM-DD.md` (e.g., `dailies/notes/2026-01-02.md`)
2. Write your notes in markdown
3. (Optional) Add images to `dailies/images/YYYY-MM-DD/`
4. Run the script - your notes appear automatically in `dailies/pages/`!

## Example Workflow

### Today is 2026-01-02, you just read the daily papers...

**Create the file:**
```bash
nano dailies/notes/2026-01-02.md
```

**Write your thoughts:**
```markdown
# Key Takeaways

## What I Learned
- The attention mechanism is fascinating
- Could apply this to my project

## Next Steps
- Try the code from paper 2
- Email the author with questions

![My notes](notes.png)
```

**Add images (if you have any):**
```bash
mkdir -p dailies/images/2026-01-02
cp ~/screenshots/notes.png dailies/images/2026-01-02/
```

**Done!** The script automatically includes your notes.

## What You Get

Your daily HTML page will show:
1. **3 AI-generated paper summaries** (automatic)
2. **Quiz questions** (automatic)
3. **📝 My Takeaways section** ⭐ NEW! (your personal notes)

The takeaways section has:
- Beautiful purple gradient background
- Styled markdown rendering
- Responsive images
- Clean typography

## Folder Organization

```
dailies/
├── pages/      # Generated HTML (don't edit)
├── notes/      # Your markdown files (edit here!)
└── images/     # Your images
```

## See It In Action

Check out `dailies/notes/2026-01-02.md` for a complete example!

---

**Pro Tip**: You can edit the `.md` file in `dailies/notes/` anytime and re-run the script to update the HTML in `dailies/pages/`. No need to touch the HTML files directly!
