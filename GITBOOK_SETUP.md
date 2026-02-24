# 📚 GitBook Setup Guide for Rift Protocol

> **Professional documentation powered by GitBook**

---

## 🎯 What We've Created

### GitBook Configuration Files

| File | Purpose | Status |
|------|---------|--------|
| `SUMMARY.md` | Table of contents (GitBook index) | ✅ Enhanced |
| `docs/README.md` | GitBook landing page | ✅ Created |
| `book.json` | GitBook configuration | ✅ Created |
| `styles/website.css` | Custom branding styles | ✅ Created |

---

## 📖 GitBook Structure

```
rift-core-internal/
├── SUMMARY.md              ⭐ GitBook Table of Contents
├── book.json               ⭐ GitBook Configuration
├── styles/
│   └── website.css         ⭐ Custom Styling
├── docs/
│   ├── README.md           ⭐ GitBook Home Page
│   ├── TECHNICAL_OVERVIEW.md
│   ├── HACKATHON_DEMO.md
│   ├── architecture.md
│   ├── tech_stack.md
│   ├── getting_started.md
│   ├── RPC_ISSUES.md
│   └── PHASE4_EXECUTOR_PLAN.md
├── watcher/
│   └── README.md           ⭐ Component Documentation
├── README.md               📄 Main GitHub README
└── CONTRIBUTING.md         🤝 Contribution Guide
```

---

## 🚀 Deploy to GitBook (3 Methods)

### Method 1: GitBook Integration (Recommended)

**Step 1: Connect GitHub Repository**

1. Go to [GitBook.com](https://www.gitbook.com/)
2. Sign in with GitHub
3. Click "New Project" → "Import from Git"
4. Select your `rift-core-internal` repository
5. GitBook auto-detects `SUMMARY.md` and `book.json`

**Step 2: Configure GitBook**

- **Root Directory**: Leave blank (uses repo root)
- **Branch**: `main`
- **Configuration File**: `book.json` (auto-detected)

**Step 3: Publish**

- Click "Publish"
- GitBook builds your documentation
- Get live URL: `https://rift-protocol.gitbook.io/`

**Benefits**:
- ✅ Automatic updates on git push
- ✅ Professional hosting
- ✅ Search functionality
- ✅ Version control
- ✅ Analytics

---

### Method 2: Local GitBook CLI (For Testing)

**Install GitBook CLI**:

```bash
# Install Node.js (if not installed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install GitBook CLI
npm install -g gitbook-cli

# Verify installation
gitbook --version
```

**Build Locally**:

```bash
cd ~/rift-core-internal

# Install plugins
gitbook install

# Serve locally (http://localhost:4000)
gitbook serve

# Build static site
gitbook build
```

**Benefits**:
- ✅ Test before publishing
- ✅ Offline development
- ✅ Custom plugins

---

### Method 3: GitHub Pages (Free Alternative)

**Step 1: Install gitbook-cli**

```bash
npm install -g gitbook-cli
```

**Step 2: Build for GitHub Pages**

```bash
cd ~/rift-core-internal

# Install plugins
gitbook install

# Build to _book directory
gitbook build

# Copy to docs folder (for GitHub Pages)
cp -r _book/* docs/

# Commit and push
git add docs/
git commit -m "Build GitBook for GitHub Pages"
git push origin main
```

**Step 3: Enable GitHub Pages**

1. Go to repository Settings → Pages
2. Source: Deploy from branch
3. Branch: `main`, folder: `/docs`
4. Save

**Your docs will be live at**: `https://your-username.github.io/rift-core-internal/`

---

## 🎨 Customization

### Branding (book.json)

Current configuration:

```json
{
  "title": "Rift Protocol Documentation",
  "description": "Break the 10-Minute Barrier: Instant Bitcoin Verification on Starknet",
  "author": "Rift Protocol Team",
  "language": "en"
}
```

**Customize**:
- Change `title` for your project name
- Update `description` for SEO
- Add social media links in `links.sharing`

---

### Styling (styles/website.css)

**Brand Colors**:

```css
:root {
  --rift-orange: #ff6b35;  /* Primary accent */
  --rift-blue: #004e89;    /* Links, headers */
  --rift-dark: #1a1a2e;    /* Text, sidebar */
  --rift-light: #f7f7f7;   /* Backgrounds */
}
```

**Customize**:
- Update color variables for your brand
- Add custom fonts
- Modify table styles
- Change code block themes

---

### Navigation (SUMMARY.md)

**Structure**:

```markdown
# Table of Contents

## 🏠 Introduction
* [Welcome](docs/README.md)
* [Technical Overview](docs/TECHNICAL_OVERVIEW.md)

## 🚀 Getting Started
* [Quick Start](docs/getting_started.md)

## 📚 Core Documentation
* [Architecture](docs/architecture.md)
* [Tech Stack](docs/tech_stack.md)

... (more sections)
```

**Tips**:
- Use emojis for visual appeal
- Group related docs together
- Add "Start Here" markers ⭐
- Include external links

---

## 📊 GitBook Features

### Enabled Plugins (book.json)

| Plugin | Purpose |
|--------|---------|
| `search` | Full-text search |
| `lunr` | Search index |
| `codeblock-label` | Code block labels |
| `copy-code-button` | Copy code to clipboard |
| `expandable-chapters` | Collapsible sections |
| `anchors` | Anchor links |
| `github` | GitHub integration |
| `theme-default` | Default theme |

### Additional Plugins (Optional)

Install more plugins:

```bash
# Edit book.json, add to "plugins" array
"plugins": [
  ...existing...,
  "sitemap",
  "ga",  # Google Analytics
  "disqus"  # Comments
]

# Install
gitbook install
```

**Popular Plugins**:
- `sitemap` - SEO sitemap
- `ga` - Google Analytics
- `disqus` - Comment system
- `edit-link` - "Edit this page" button
- `anchors` - Anchor links for headings

---

## 🔗 Navigation Links

### Sidebar Links (book.json)

```json
"links": {
  "sidebar": {
    "GitHub": "https://github.com/your-repo",
    "Technical Overview": "docs/TECHNICAL_OVERVIEW.md",
    "Demo Guide": "docs/HACKATHON_DEMO.md"
  }
}
```

### Footer Links

Add to `docs/README.md`:

```markdown
<div align="center">

**⚡ Making Bitcoin Instant**

[GitHub](https://github.com/your-repo) • [Documentation Index](SUMMARY.md)

</div>
```

---

## 📱 Multi-Format Output

GitBook automatically generates:

| Format | Use Case |
|--------|----------|
| **Website** | Online documentation |
| **PDF** | Printable version |
| **ePub** | E-readers (Kindle, Apple Books) |
| **Mobi** | Kindle devices |

**Download Links** (auto-generated by GitBook):
- Export → PDF
- Export → ePub
- Export → Mobi

---

## 🎯 GitBook Best Practices

### Content Organization

✅ **Do**:
- Start with overview/TL;DR
- Use clear hierarchy (H1 → H2 → H3)
- Include code examples
- Add diagrams/visuals
- Link related documents
- Use tables for comparisons

❌ **Don't**:
- Create walls of text
- Use deep nesting (max 3 levels)
- Forget to update SUMMARY.md
- Ignore mobile responsiveness

---

### Writing Style

**For Hackathon Judges**:
- Keep it scannable
- Use bold for key points
- Include "Start Here" markers
- Add time estimates (5 min read)
- Provide quick navigation

**Example**:

```markdown
## 🎯 Quick Navigation

### New to Rift?
1. [Technical Overview](docs/TECHNICAL_OVERVIEW.md) ⭐ **Start Here**
2. [Run Demo](docs/HACKATHON_DEMO.md) - 2 minutes
3. [Architecture](docs/architecture.md) - 10 minutes

### For Judges
- [Evaluation Criteria](docs/TECHNICAL_OVERVIEW.md#why-rift-protocol)
- [Presentation Script](docs/TECHNICAL_OVERVIEW.md#presentation-script)
```

---

## 📊 Analytics (Optional)

### Google Analytics Integration

**Step 1**: Get tracking ID from [Google Analytics](https://analytics.google.com/)

**Step 2**: Add to `book.json`:

```json
"plugins": ["ga"],
"pluginsConfig": {
  "ga": {
    "token": "UA-XXXXX-X"
  }
}
```

**Step 3**: Install plugin

```bash
gitbook install
```

---

## 🚀 Deployment Checklist

### Before Publishing

- [ ] SUMMARY.md is complete and organized
- [ ] All links work (test internally)
- [ ] book.json configured correctly
- [ ] Custom styles in place (optional)
- [ ] docs/README.md is welcoming
- [ ] Images/diagrams render correctly
- [ ] Code blocks are formatted
- [ ] No typos or broken formatting

### After Publishing

- [ ] Test live site on desktop
- [ ] Test on mobile (responsive)
- [ ] Verify search works
- [ ] Check all navigation links
- [ ] Test download links (PDF/ePub)
- [ ] Share with team for review
- [ ] Update GitHub README with GitBook link

---

## 🎨 Example Output

### What Judges Will See

**Landing Page**:
```
┌─────────────────────────────────────────────┐
│  ⚡ Rift Protocol Documentation             │
│  Break the 10-Minute Barrier                │
├─────────────────────────────────────────────┤
│  📖 Table of Contents                       │
│  ├─ 🏠 Introduction                         │
│  ├─ 🚀 Getting Started                      │
│  ├─ 📚 Core Documentation                   │
│  ├─ 🎓 Technical Deep Dive                  │
│  └─ 🎯 Hackathon Resources                  │
├─────────────────────────────────────────────┤
│  [Search Box]                               │
│  [GitHub Link] [Demo Guide] [Overview]      │
└─────────────────────────────────────────────┘
```

**Document Page**:
```
┌─────────────────────────────────────────────┐
│  Technical Overview                         │
│  ─────────────────────────────────────────  │
│  Executive Summary...                       │
│                                             │
│  ## Architecture                            │
│  [Diagram]                                  │
│                                             │
│  ## Quick Start                             │
│  ```bash                                    │
│  ./watcher/run-hackathon-demo.sh            │
│  ```                                        │
│  [Copy Button]                              │
└─────────────────────────────────────────────┘
```

---

## 📞 Support & Resources

### GitBook Documentation
- [GitBook Docs](https://docs.gitbook.com/)
- [Configuration Reference](https://docs.gitbook.com/product-tour/gitbook-config)
- [Plugin Directory](https://plugins.gitbook.com/)

### Rift Protocol Docs
- [SUMMARY.md](SUMMARY.md) - Table of contents
- [book.json](book.json) - Configuration
- [styles/website.css](styles/website.css) - Custom styles
- [docs/README.md](docs/README.md) - Landing page

---

## 🎯 Next Steps

### Immediate (For Hackathon)

1. **Deploy to GitBook** (Method 1 - 5 minutes)
   - Connect GitHub
   - Auto-deploy
   - Get live URL

2. **Add to Submission**
   - Include GitBook URL in Devpost
   - Mention in README
   - Share with judges

### Long-term

1. **Custom Domain**
   - Connect custom domain in GitBook
   - Use `docs.riftprotocol.com`

2. **Version Control**
   - Create versions for releases
   - Maintain changelog

3. **Community**
   - Enable comments (Disqus)
   - Add feedback widget
   - Track analytics

---

<div align="center">

**📚 Your Documentation is GitBook-Ready!**

[Back to Main Docs](SUMMARY.md) • [Configuration Guide](book.json) • [Style Guide](styles/website.css)

</div>
