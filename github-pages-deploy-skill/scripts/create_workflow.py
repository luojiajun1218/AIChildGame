#!/usr/bin/env python3
"""
Create GitHub Actions workflow for deploying to GitHub Pages.
Supports multiple project types: vanilla, react-vite, cra, vue, nextjs.
"""

import os
import sys
from pathlib import Path


def get_workflow_template(project_type, repo_name, build_dir=None):
    """Get workflow template based on project type."""

    if project_type == "vanilla":
        workflow = '''name: Deploy to GitHub Pages

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
'''

    elif project_type == "react-vite":
        workflow = f'''name: Deploy to GitHub Pages

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
          VITE_BASE_URL: /{repo_name}/

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
'''

    elif project_type == "cra":
        workflow = f'''name: Deploy to GitHub Pages

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
          PUBLIC_URL: /{repo_name}/

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: build

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
'''

    elif project_type == "vue":
        workflow = f'''name: Deploy to GitHub Pages

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
'''

    elif project_type == "nextjs":
        workflow = f'''name: Deploy to GitHub Pages

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
'''

    else:
        raise ValueError(f"Unknown project type: {project_type}")

    return workflow


def create_workflow(project_type, repo_name, output_path=None):
    """Create GitHub Actions workflow file."""

    if output_path is None:
        output_path = Path.cwd() / ".github" / "workflows" / "deploy.yml"
    else:
        output_path = Path(output_path)

    # Create directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Get workflow template
    workflow = get_workflow_template(project_type, repo_name)

    # Write workflow file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(workflow)

    print(f"[OK] Created GitHub Actions workflow at: {output_path}")
    return output_path


def main():
    """CLI interface."""
    if len(sys.argv) < 3:
        print("Usage: python create_workflow.py <project_type> <repo_name> [output_path]")
        print("\nProject types:")
        print("  vanilla     - Plain HTML/CSS/JS")
        print("  react-vite  - React with Vite")
        print("  cra         - Create React App")
        print("  vue         - Vue with Vite")
        print("  nextjs      - Next.js static export")
        sys.exit(1)

    project_type = sys.argv[1]
    repo_name = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        create_workflow(project_type, repo_name, output_path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
