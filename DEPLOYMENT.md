# Deployment and Git Handoff

## 1) Create New Independent Repository

Example repository name:
- `apollo-krishi-portal`

Do not use or overwrite `aarthika2007/Apollo-Krishi-Rakshak`.

## 2) Push This Portal

Run from Apollo workspace root:

```bash
cd phase_4_collaboration/apollo-krishi-portal
git init
git add .
git commit -m "Phase 4: Apollo Krishi Rakshak collaboration portal"
git branch -M main
git remote add origin https://github.com/<your-org-or-user>/apollo-krishi-portal.git
git push -u origin main
```

## 3) Host Options

### GitHub Pages
- Enable GitHub Pages from `main` branch root
- URL will be generated automatically

### Vercel / Netlify
- Import repository
- Framework preset: static site
- Build command: none
- Output directory: root

## 4) Domain Mapping

Preferred:
- `apollokrushi.chatakeinnoworks.com` -> new Phase 4 portal
- `apollo.chatakeinnoworks.com` -> main Apollo umbrella or paper/presentation site

If required, reverse assignment can be done, but keep one canonical owner for each URL.

## 5) Post-Deploy Validation Checklist

- Home page loads on mobile and desktop
- Student list opens all individual profiles
- Technology list opens all individual profiles
- External Apollo links resolve correctly
- Footer branding and affiliation text is correct

## 6) Optional Hardening

- Add analytics (Plausible or GA4)
- Add CSP and security headers on host
- Add status page and changelog
- Add CI lint for HTML/CSS/JS
