# GitHub Pages Deployment Skill

A Claude Code skill for deploying static websites to GitHub Pages with automatic configuration.

## Installation

1. Download `github-pages-deploy.skill`
2. In Claude Code, use the skill management interface to install it
3. The skill will be automatically triggered when you ask to deploy to GitHub Pages

## What This Skill Does

This skill helps you deploy static websites to GitHub Pages by:

- Automatically detecting your project type (vanilla HTML/CSS/JS, React, Vue, Next.js)
- Generating the appropriate GitHub Actions workflow file
- Configuring build settings (base paths, environment variables)
- Setting up custom domains (optional)
- Troubleshooting common deployment issues

## Usage

Simply ask Claude to deploy your project to GitHub Pages:

```
"部署我的项目到 GitHub Pages"
"Deploy to GitHub Pages"
"Help me deploy this to GitHub Pages"
```

## Supported Project Types

- Vanilla HTML/CSS/JS
- React (Vite)
- Create React App
- Vue (Vite)
- Next.js (static export)

## Features

- Automatic GitHub Actions workflow generation
- Build configuration for different frameworks
- Custom domain support
- Comprehensive troubleshooting guide
- Pre-configured deployment scripts

## Skill Structure

```
github-pages-deploy.skill
├── SKILL.md                          # Main skill documentation
├── scripts/
│   └── create_workflow.py           # Workflow generation script
├── references/
│   └── troubleshooting.md           # Common issues and solutions
└── assets/
    └── CNAME.example                # Custom domain template
```

## Example Workflow

After installation, when you ask to deploy:

1. Claude analyzes your project structure
2. Creates `.github/workflows/deploy.yml`
3. Configures build settings (vite.config.js, package.json, etc.)
4. Provides instructions for enabling GitHub Pages
5. You commit and push to trigger deployment

## Troubleshooting

The skill includes a comprehensive troubleshooting guide covering:
- Blank page after deployment
- 404 errors for assets
- Router not working
- GitHub Actions failures
- Custom domain issues
- Build errors

## Requirements

- Git repository
- GitHub account
- Static website project

## License

This skill is provided as-is for deployment to GitHub Pages.
