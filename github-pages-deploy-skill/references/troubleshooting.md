# GitHub Pages Deployment Troubleshooting

Common issues and solutions for GitHub Pages deployment.

## Table of Contents

1. [Blank Page After Deployment](#blank-page-after-deployment)
2. [404 Errors for Assets](#404-errors-for-assets)
3. [Router Not Working](#router-not-working)
4. [GitHub Actions Failures](#github-actions-failures)
5. [Custom Domain Issues](#custom-domain-issues)
6. [Build Errors](#build-errors)

---

## Blank Page After Deployment

### Symptoms
- Page loads but shows blank
- Console shows 404 errors for JS/CSS files
- Assets not loading

### Common Causes

#### 1. Incorrect Base Path

**React (Vite)**:
Check `vite.config.js`:
```javascript
export default defineConfig({
  base: '/repo-name/',  // Must match repository name
})
```

**Create React App**:
Check `package.json`:
```json
{
  "homepage": "/repo-name/"
}
```

**Vue (Vite)**:
Check `vite.config.js`:
```javascript
export default defineConfig({
  base: '/repo-name/',
})
```

**Next.js**:
Check `next.config.js`:
```javascript
const nextConfig = {
  basePath: '/repo-name',
  assetPrefix: '/repo-name',
}
```

#### 2. Trailing Slash Issue

Always include trailing slash in base path:
- ✓ `/repo-name/`
- ✗ `/repo-name`

#### 3. Case Sensitivity

Repository names are case-sensitive on GitHub Pages:
- `MyRepo` ≠ `myrepo`

### Solution

1. Check repository name: `git remote get-url origin`
2. Extract repo name from URL
3. Update config with correct repo name
4. Rebuild and redeploy

---

## 404 Errors for Assets

### Symptoms
- HTML loads but images/CSS/JS return 404
- Relative paths not resolving correctly

### Common Causes

#### 1. Absolute Paths

Using absolute paths in code:
```html
<!-- Wrong -->
<img src="/images/logo.png">
<link rel="stylesheet" href="/styles.css">
```

**Solution**: Use relative paths
```html
<!-- Correct -->
<img src="./images/logo.png">
<link rel="stylesheet" href="./styles.css">
```

#### 2. Dynamic Imports

Dynamic imports with absolute paths:
```javascript
// Wrong
const module = await import('/utils/helper.js')

// Correct
const module = await import('./utils/helper.js')
```

#### 3. Public Folder References

For Create React App, files in `public/` are served at root:
```javascript
// Wrong
process.env.PUBLIC_URL + '/image.png'

// Correct
process.env.PUBLIC_URL + '/image.png'  // PUBLIC_URL includes base path
```

### Solution

Audit all asset references:
```bash
# Find absolute paths in HTML
grep -r 'src="/' *.html

# Find absolute paths in JS
grep -r "from '/" src/
```

---

## Router Not Working

### Symptoms
- Direct links to routes return 404
- Refreshing a route returns 404
- Browser back button breaks

### Why This Happens

GitHub Pages serves static files. It doesn't know about client-side routes.

### Solutions

#### Option 1: Hash-Based Router (Recommended)

**React Router**:
```javascript
import { createHashRouter } from 'react-router-dom'

const router = createHashRouter([
  {
    path: '/',
    element: <Home />,
  },
  {
    path: '/about',
    element: <About />,
  },
])
```

**Vue Router**:
```javascript
import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [...]
})
```

#### Option 2: SPA Fallback with 404.html

Create `404.html` that redirects to `index.html`:
```html
<!DOCTYPE html>
<html>
<head>
  <script>
    // Redirect all 404s to index.html
    sessionStorage.setItem('redirect', location.pathname)
    location.href = '/'
  </script>
</head>
</html>
```

Then in your app, handle the redirect:
```javascript
const redirect = sessionStorage.getItem('redirect')
if (redirect) {
  sessionStorage.removeItem('redirect')
  // Navigate to the route
}
```

#### Option 3: Use Relative Paths in Links

Ensure all navigation uses relative paths or router's Link component:
```javascript
// Wrong
<a href="/about">About</a>

// Correct
<Link to="/about">About</Link>
```

---

## GitHub Actions Failures

### Common Errors

#### 1. Build Directory Not Found

**Error**:
```
Error: Upload artifact failed: path not found: dist
```

**Solution**: Check build output directory in workflow:
```yaml
- name: Upload artifact
  uses: actions/upload-pages-artifact@v3
  with:
    path: dist  # Must match actual build output
```

Build directories by framework:
- Vite (React/Vue): `dist`
- Create React App: `build`
- Next.js: `out`
- Vanilla: root (`.`)

#### 2. Node Version Mismatch

**Error**:
```
Error: Node.js version incompatible
```

**Solution**: Update workflow Node version:
```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'  # Match local version
```

Check local version:
```bash
node --version
```

#### 3. Build Fails Locally Too

If build fails in Actions, test locally:
```bash
npm ci
npm run build
```

Fix errors locally before pushing.

#### 4. Permission Denied

**Error**:
```
Error: Resource not accessible by integration
```

**Solution**: Ensure workflow has permissions:
```yaml
permissions:
  contents: write
  pages: write
  id-token: write
```

### Debugging Workflow

1. Go to repository Actions tab
2. Click on failed workflow run
3. Expand each step to see logs
4. Look for red error messages
5. Fix errors and commit again

---

## Custom Domain Issues

### Symptoms
- Custom domain not resolving
- HTTPS not working
- "Site not found" error

### Solution Checklist

#### 1. CNAME File

Create `CNAME` file in root or build directory:
```
www.yourdomain.com
```

Include in deployment:
```yaml
- name: Add CNAME
  run: echo 'www.yourdomain.com' > ./dist/CNAME
```

Or place in `public/` folder for React projects.

#### 2. DNS Settings

Configure DNS provider:

**For subdomain (www.yourdomain.com)**:
```
Type: CNAME
Name: www
Value: username.github.io
TTL: 3600
```

**For apex domain (yourdomain.com)**:
```
Type: A
Name: @
Value: 185.199.108.153
       185.199.109.153
       185.199.110.153
       185.199.111.153
TTL: 3600
```

#### 3. Enable HTTPS in GitHub

1. Go to repository Settings
2. Pages
3. Enforce HTTPS: On
4. Wait for DNS to propagate (can take 24-48 hours)

#### 4. Check DNS Propagation

Use `dig` or online tools:
```bash
dig www.yourdomain.com
```

Should point to GitHub Pages IPs.

---

## Build Errors

### Common Issues

#### 1. Memory Limit Exceeded

**Error**:
```
JavaScript heap out of memory
```

**Solution**: Increase Node memory in workflow:
```yaml
- name: Build
  run: npm run build
  env:
    NODE_OPTIONS: --max-old-space-size=4096
```

#### 2. Type Errors

For TypeScript projects, ensure strict mode doesn't fail build:
```json
// tsconfig.json
{
  "compilerOptions": {
    "noEmitOnError": false
  }
}
```

#### 3. Missing Environment Variables

Add environment variables to workflow:
```yaml
- name: Build
  run: npm run build
  env:
    MY_API_KEY: ${{ secrets.MY_API_KEY }}
```

Store secrets in repository Settings > Secrets > Actions.

#### 4. Asset Optimization Fails

Disable asset optimization if problematic:

**Next.js**:
```javascript
// next.config.js
module.exports = {
  images: {
    unoptimized: true
  }
}
```

**Vite**:
```javascript
// vite.config.js
export default defineConfig({
  build: {
    assetsInlineLimit: 0
  }
})
```

---

## Quick Diagnostic Commands

```bash
# Check current branch
git branch --show-current

# Check remote URL
git remote get-url origin

# Extract repo name from URL
git remote get-url origin | sed 's/.*:\(.*\)\.git/\1/'

# Test build locally
npm run build

# Serve build for testing
npx serve dist
# or
npx serve build  # for CRA
```

---

## Still Having Issues?

1. Check GitHub Actions logs
2. Verify repository settings (Pages source = GitHub Actions)
3. Ensure branch is correct (usually `main`)
4. Try clearing browser cache
5. Test in incognito/private mode
6. Check GitHub Status page for outages
