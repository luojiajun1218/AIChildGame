---
name: github-webpages-deploy
description: Deploy static websites to GitHub Pages with automatic configuration generation. Use this when users explicitly request to deploy a website to GitHub Pages, including tasks like: (1) Deploying an HTML/CSS/JS project to GitHub Pages, (2) Setting up GitHub Actions workflow for automatic deployment, (3) Configuring custom domains with CNAME files, (4) Converting repository settings for GitHub Pages hosting. This skill handles the complete deployment workflow for static sites including React, Vue, vanilla JavaScript, and other frontend frameworks.
---

# GitHub Pages Deployment

Deploy static websites to GitHub Pages automatically.

## Quick Start

1. Check repository status
2. Create GitHub Actions workflow
3. Configure deployment settings (branch, directory, custom domain)
4. Push to trigger deployment

## When to Use This Skill

Use ONLY when user explicitly mentions:
- "deploy to GitHub Pages"
- "部署到 GitHub 网页"
- "GitHub Pages deployment"
- Similar explicit deployment requests to GitHub Pages

Do NOT use for:
- Other hosting platforms (Vercel, Netlify, etc.)
- General web deployment without GitHub Pages context
- Local development server setup

## Deployment Workflow

### 1. Analyze Project Structure

Check project type and build configuration:

```bash
# Identify project type
ls -la
cat package.json  # if exists
```

**Project types:**
- **Vanilla HTML/CSS/JS**: Static files ready to deploy
- **React/Vue/Angular**: Needs build step
- **Next.js/Nuxt**: Needs static export

### 2. Create GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

**For vanilla HTML/CSS/JS:**
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**For React (Vite):**
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build
        env:
          # For Vite projects
          VITE_BASE_URL: /${{ github.event.repository.name }}

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist  # Vite default output

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**For Create React App:**
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build
        env:
          # For CRA projects
          PUBLIC_URL: /${{ github.event.repository.name }}

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: build  # CRA default output

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**For Vue (Vite):**
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**For Next.js (Static Export):**
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: out

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 3. Configure Project Build Settings

**For Vite projects (React/Vue):**

Update `vite.config.js`:
```javascript
import { defineConfig } from 'vite'

export default defineConfig({
  base: '/your-repo-name/',  // Replace with actual repo name
  // ... other config
})
```

**For Vue (Vite) specifically:**

Update `vite.config.js`:
```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/your-repo-name/',  // Replace with actual repo name
})
```

**For Create React App:**

Add `homepage` field to `package.json`:
```json
{
  "homepage": "/your-repo-name/",
  "name": "your-app",
  "version": "0.1.0",
  ...
}
```

**For Next.js:**

Update `next.config.js`:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/your-repo-name',
  assetPrefix: '/your-repo-name',
  images: {
    unoptimized: true
  }
}

module.exports = nextConfig
```

Update `package.json` scripts:
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "export": "next build"
  }
}
```

### 4. Configure Custom Domain (Optional)

If user wants a custom domain:

1. Create `CNAME` file in root or appropriate directory:
```
www.yourdomain.com
```

2. Update workflow to include CNAME in deployment:
```yaml
      - name: Add CNAME
        run: echo 'www.yourdomain.com' > ./dist/CNAME
```

Or place `CNAME` in `public/` folder for React projects.

### 5. Repository Settings

Ensure GitHub Pages is enabled:

**Via GitHub CLI:**
```bash
# If gh is installed
gh repo view --web
# Then manually enable Pages in Settings > Pages
# Source: GitHub Actions
```

**Manual steps:**
1. Go to repository Settings
2. Click Pages
3. Build and deployment: Source = GitHub Actions
4. Save

## Common Issues and Solutions

### Issue: Blank page after deployment

**Cause**: Incorrect base path configuration

**Solution**:
- Ensure `base` in vite.config.js matches repo name
- Ensure `homepage` in package.json matches repo name
- Format: `/repo-name/` (with slashes)

### Issue: 404 for assets

**Cause**: Incorrect relative paths

**Solution**:
- Use relative paths: `./image.png` not `/image.png`
- Configure framework base path correctly

### Issue: Router not working

**Cause**: Client-side routing needs server configuration

**Solution**:
- Use hash-based routing: `createHashRouter()` (React Router)
- Or configure fallback in 404.html

### Issue: GitHub Actions fails

**Common causes**:
- Build directory path incorrect in workflow
- Node version mismatch
- Missing dependencies

**Debug**:
1. Check Actions tab in GitHub
2. Review build logs
3. Fix errors and push again

## Project Type Detection

Use these indicators:

| Project Type | Indicators |
|------------|-----------|
| Vanilla HTML/CSS/JS | `index.html` exists, no `package.json` or no build script |
| React (Vite) | `vite.config.js`, `src/main.jsx` or `src/main.tsx` |
| Create React App | `package.json` has `react-scripts` in dependencies |
| Vue (Vite) | `vite.config.js` with `@vitejs/plugin-vue` |
| Next.js | `next.config.js`, `pages/` or `app/` directory |
| Nuxt | `nuxt.config.ts` |

## Build Output Directories

| Framework | Default Output |
|-----------|---------------|
| Vite (React/Vue) | `dist/` |
| Create React App | `build/` |
| Next.js (export) | `out/` |
| Vanilla JS | Root directory `./` |

## Testing Before Deploying

Always test locally first:

```bash
# For Node projects
npm run build

# Test production build locally
npx serve dist  # or build/, out/, etc.

# For vanilla HTML
python -m http.server 8000
# Then open http://localhost:8000
```

## Summary Workflow

1. **Identify project type** from file structure
2. **Create workflow** matching project type
3. **Configure build settings** (base path, homepage, etc.)
4. **Test build locally** to catch errors
5. **Commit and push** to trigger deployment
6. **Verify deployment** at `https://username.github.io/repo-name/`
