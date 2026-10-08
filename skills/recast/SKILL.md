---
name: recast
description: Rebuild a vibe-coded app in a fresh repo from consolidated, improved area specs. Survey the old app, draft and negotiate the specs with the user, then build the new repo from them. Use when the user asks to recast, rebuild or re-spec an app that has the right features but has grown messy (spec drift, dead code, inconsistent patterns), or when they mention recasting.
---

# Recasting: rebuilding a vibe-coded app from its specs

In this skill "you" is the AI doing the recast. The user owns the decisions.

## What recasting is

Recasting rebuilds a vibe-coded app in a fresh repo from a consolidated, improved spec. The old app is the model, not the source.

The name comes from lost-wax casting. The old app is the wax model: lumpy, but it has the shape the user wants. The area specs are the mould taken from it. The new repo is the clean casting.

Use it when an app has the features the user wants, working roughly how they want, but has been reshaped so often it is nobbly: spec drift, dead code, inconsistent patterns, and changes they now want to make.

Goals:

- Simplify where possible
- Consolidate the specs and improve them now the whole picture is visible
- State the changes the user wants
- Restructure the code
- Leave a repo that is easy to recast again

## Principles

- **Specs describe the current state only.** No history, no "previously", no changelog.
- **Removals vanish.** A cut item lives only in `open-questions.md` while it is being negotiated, then it is deleted. The old repo is the archive.
- **Two-way.** You propose opportunities, the user states changes, and rounds continue until settled.
- **Code stays clean.** No spec references in code comments. The link between spec and code lives in commit messages.
- **Fresh repo.** The old app stays available as the reference while the new one is built.
- **Simple.** Area specs, a constraints section in each, IDs in commits, and a temporary open-questions file. Nothing else.

## Spec structure

Specs are split into areas, and each area maps one-to-one to a code module.

```
specs/
  README.md            map of areas, one paragraph each
  <area>.md            one file per area
  open-questions.md    exists only during negotiation
```

Each area file has four parts:

| Part | Holds |
| --- | --- |
| Purpose | What the area is for, in a few sentences |
| Behaviour | Requirements with IDs and acceptance criteria, e.g. `R-cal-01` |
| Constraints | Scar tissue: rules learned the hard way, e.g. `C-cal-03` |
| Interfaces | Which other areas it uses or is used by |

A constraint is a rule, one line of why, and the test that proves it:

> **C-cal-03** Calendar queries must follow `@odata.nextLink`. Graph pages results, and a single request silently drops events. *Test:* `graph_calendar_pagination`

The test checks the app's handling, not the outside service. For an external API quirk, fake the response and assert the app copes. A constraint that cannot be tested, such as one on timing or rate limits, carries `Test: none` and the reason.

IDs take the form `<type>-<area>-<nn>`. They are stable and never reused.

## The process

Seven steps. Steps 1 to 5 happen against the old repo; steps 6 and 7 build the new one.

1. **Survey.** Read the old code, any specs and the git history, then report per area:
    - what the code actually does
    - where the specs have drifted
    - dead code, duplication and inconsistent patterns
    - scar-tissue candidates: fix commits, special cases, retries, odd error handling, "workaround" or "hack" comments
2. **Capture behaviour.** For the parts being kept only, write behaviour tests or golden examples against the old app. These become the parity check.
3. **Draft area specs.** One file per area, describing current behaviour. With no existing specs, derive them from the code and the running app. Code shows what the app does, not what the user meant, so every derived requirement is a question for the user until confirmed. Drift, oddities and scar-tissue candidates go into `open-questions.md` as questions, not silent fixes.
4. **Negotiation rounds.** Propose simplifications, merges, deletions and improvements. The user states the changes they want. Each item ends one of three ways:
    - keep: it goes into the area spec
    - change: the area spec is updated
    - drop: it is deleted everywhere, with no record left
5. **Settle and plan structure.** Settled means `open-questions.md` is empty and deleted, every requirement has acceptance criteria, and every constraint has a test or a stated reason for having none. Then derive the module layout from the areas, one module per area, and agree it with the user.
6. **Pour.** Create the new repo. The first commit is the settled specs, with no code. Build area by area from the specs, using the old code as reference only.
7. **Verify.** The behaviour tests from step 2 and every constraint test pass against the new app.

## Commit conventions

Commits carry the link between spec and code, so the code itself stays clean.

- **The first commit is specs only.** History starts from intent.
- **A behaviour change updates its spec in the same commit.**
- **The message names the area, plus the ID when one applies:** `cal: follow nextLink pagination (C-cal-03)`
- **Refactors and tooling changes need no ID**, only the area prefix.

## Making the next recast easy

The next survey becomes a per-area diff rather than an archaeology dig, because of four things set up here:

- Areas mirror modules, so each spec is compared against one module.
- Specs hold only the current state, so there is nothing stale to wade through.
- Constraints and their tests survive into the new repo, so the scar tissue is never mined twice.
- Commits carry IDs, so a grep per area shows what changed and why.

Tag the pour commit, for example `recast-1`. The next survey then reads only the commits since that tag.
