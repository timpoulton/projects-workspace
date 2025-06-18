# projekt-ai-website Memory

## Music & Hospitality Niche Checklist

- Messaging & Hero Section
  - Rewrite homepage headline to "Automate your venue's social media & promo workflows with AI."
  - Add a 3-step "How it Works" diagram: 1) Define content calendar, 2) Auto-generate posts, 3) Schedule across channels

- Dedicated Service Pages
  - Create `/services/social-media-automation.html` describing pain points, AI-powered solution, and key features; include CTA "See a live demo."
  - Create `/services/marketing-automations.html` covering email drips, audience segmentation, event reminders

- Case Studies & Social Proof
  - Build a case study template (challenge → solution → impact → testimonial)
  - Publish first case study: e.g. "How we helped Club77 boost Instagram engagement by 40%."
  - Add a "Trusted by" carousel of logos for labels, venues, and promoters you've worked with

- Thought-Leadership & SEO
  - Spin up `/blog/` and publish posts: "5 AI automations every music promoter needs" and "How to schedule a month of Instagram Stories in 5 minutes"
  - Create a free PDF lead magnet "Social Media Automation Checklist" and offer via newsletter signup

- Interactive Demos & Conversions
  - Embed a chatbot widget on the homepage to generate sample posts (e.g. "Write an Instagram caption for a jazz night")
  - Build a simple ROI calculator (estimate time saved per event)
  - Add sticky CTAs: "Book your free demo" and "Download checklist"

- Lead Capture & Nurturing
  - Install a newsletter signup (Mailchimp or SendGrid) tied to the checklist incentive
  - Configure automated email drip: Day 1 welcome + checklist, Day 3 case study, Day 7 strategy call offer

- Automation Integrations
  - Wire up Buffer/Hootsuite/Zapier integrations to auto-publish generated content
  - Build a Zap/Make flow: on new blog post → auto-tweet + push to LinkedIn

- Analytics & Tracking
  - Install Google Analytics 4 and track "Request Demo" and "Checklist Download" events
  - Set up conversion goals and monitor via GA dashboards

- Site Audit & Optimization
  - Ensure each page has SEO-friendly titles/descriptions targeting "music automation" and "venue marketing AI"
  - Optimize images, enable caching headers, and test performance with Lighthouse

- Finalize Documentation & Workflow
  - Update Master Doc and Standardization guides with new `/services/`, `/blog/`, and CTA patterns
  - Test the in-project chat wrapper (`./scripts/chat.sh --workflow`) to train AI memory on these steps

## Reel Builder Automation Case Study Setup

- **Brand voice**: Builder-in-public transparency, high-agency optimism, data-backed pragmatism; conversational tone inspired by Nick Saraev.
- **Target persona**: Music-industry clients & independent creators.
- **Asset paths**  (relative to site root):
  - `assets/videos/automation-overview.mp4` – 1 m 51 s walkthrough.
  - `assets/videos/reel-output.mp4` – 45 s finished reel.
  - Image placeholders in `assets/img/case-study/` (hero mock-up, flow diagram, chat screenshots, video posters).
- **Case-study structure**: Hero → Snapshot → Challenge → Solution → Step-by-step flow → Tech stack → Results & impact → Demo videos → CTA.
- **Key metrics**: 90–95 % time saved; ≤ 19 MB file; <$0.50 compute cost per reel; scalable to hundreds/day.
- **Tech stack**: Telegram Bot API (Node/TS), Apify Actors, Creatomate templates, Cloud Run/AWS Lambda, Redis/Supabase, Zapier/Make connectors.

_(Last updated: see chat on 2025-06-18)_

