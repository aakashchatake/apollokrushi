# Apollo Krishi Rakshak - Phase 4 Collaboration Portal

Independent premium collaboration portal for Team Apollo and Chatake Innoworks.

## Project Purpose

This portal is intentionally separate from the original student repository and existing Apollo presentation website.

It is designed to:
- showcase each student contribution individually,
- showcase each technology stream individually,
- connect visitors to Apollo presentation and paper tracks,
- provide roadmap visibility toward ROS2, rover, lander, and autonomous agriculture expansion.

## Structure

- `index.html` - master introduction and ecosystem navigation
- `students.html` - all students listing
- `student.html?id=<student-id>` - individual student profile page
- `technologies.html` - all technology listing
- `technology.html?id=<tech-id>` - individual technology page
- `css/style.css` - design system and responsive styles
- `js/data.js` - structured student and technology metadata
- `js/main.js` - rendering and page interactions

## Run Locally

You can run this static site with any server:

```bash
cd phase_4_collaboration/apollo-krishi-portal
python -m http.server 8080
```

Then open: `http://localhost:8080`

## Domain Strategy

Recommended:
- Primary product domain: `apollokrushi.chatakeinnoworks.com`
- Canonical Apollo umbrella domain: `apollo.chatakeinnoworks.com`

Suggested redirect policy:
- Keep this portal on `apollokrushi.chatakeinnoworks.com`
- Keep original Apollo presentation/paper site under `apollo.chatakeinnoworks.com`
