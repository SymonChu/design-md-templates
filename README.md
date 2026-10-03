# design-md-templates

74 ready-to-use `DESIGN.md` files — drop one into a project root, tell your AI
coding agent *"build me a page that looks like this"*, and get UI that matches one
design language instead of a stitched-together guess.

Derived from [`VoltAgent/awesome-design-md`](https://github.com/VoltAgent/awesome-design-md)
(MIT), at upstream commit `f6961238` (2026-10-03), with two additions per file:

1. **A Hermes Implementation Notes block** at the top — each design's proprietary
   faces mapped to Google Fonts substitutes, with a paste-ready `<link>` tag and
   the exact CSS font stacks. Most upstream files already carry a
   `Note on Font Substitutes` section; this block is the agent-facing summary.
2. **`DESIGN.md` bodies are kept verbatim.** Everything after the Notes block is
   byte-identical to upstream, so `diff` against upstream stays meaningful when you
   re-sync.

56 of the 74 files carry the upstream YAML frontmatter (Google Stitch DESIGN.md
spec: tokens + normative values). The rest are on upstream's older numbered-section
format — upstream itself runs five different section shapes.

## Use

```bash
curl -O https://raw.githubusercontent.com/SymonChu/design-md-templates/main/templates/stripe.md
mv stripe.md DESIGN.md       # put it in your project root
```

Then tell your agent: *"Use DESIGN.md as the design system for this page."*

## What's inside

| Group | Entries |
|---|---|
| AI & ML | claude, cohere, elevenlabs, minimax, mistral.ai, ollama, opencode.ai, replicate, runwayml, together.ai, voltagent, x.ai |
| Developer tools | cursor, expo, linear.app, lovable, raycast, resend, sentry, supabase, superhuman, vercel, warp |
| Infra & cloud | clickhouse, composio, hashicorp, mongodb, posthog, sanity, stripe |
| Design & productivity | airtable, cal, clay, figma, framer, intercom, miro, notion, pinterest, slack, webflow, zapier |
| Fintech & crypto | binance, coinbase, kraken, mastercard, revolut, wise |
| E-commerce & retail | airbnb, nike, shopify, starbucks |
| Media & consumer | apple, bmw, hp, ibm, meta, nvidia, playstation, spacex, spotify, theverge, uber, vodafone, wired |
| Automotive | bmw-m, bugatti, ferrari, lamborghini, renault, tesla |
| Retro web | dell-1996, nintendo-2001 |

Full descriptions per entry: see the catalog in [`SKILL.md`](SKILL.md).

## License

The repository structure and the Hermes Implementation Notes are MIT (see
[LICENSE](LICENSE), inherited from upstream). The extracted design tokens describe
publicly visible CSS values from the referenced sites. No affiliation with, or
endorsement by, any of the named companies is claimed; all trademarks, brand names
and proprietary typefaces belong to their respective owners.
