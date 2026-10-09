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
- **Removals vanish.** A cut item lives only in the open questions while it is being negotiated, then it is deleted. The old repo is the archive.
- **Two-way.** You propose opportunities, the user states changes, and rounds continue until settled.
- **Suggest, don't just ask.** Every open question carries your suggested answer. Ask the big questions first, because their answers decide which smaller ones still matter.
- **Talk above the code.** The user will not know the internals of a vibe-coded app. Pitch findings, questions and proposals at a level a technical person can follow without reading the code: what a part does, how the parts fit together, and what would change. No function names, file paths or line-level detail.
- **Code stays clean.** No spec references in code comments. The link between spec and code lives in commit messages.
- **Fresh repo.** The old app stays available as the reference while the new one is built.
- **Simple.** Area specs, a constraints section in each, IDs in commits, and temporary open questions. Nothing else.

## Spec structure

Specs are split into areas, and each area maps one-to-one to a code module.

```
specs/
  README.md            map of areas, one paragraph each
  <area>.md            one file per area
  open-questions.md    only during negotiation, and only when the review page can't be used
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

    End the report by asking the user what they already want changed, added or dropped. Wait for the answer before step 2: it decides which behaviour is captured and what the specs describe.
2. **Capture behaviour.** For the parts being kept only, write behaviour tests or golden examples against the old app. These become the parity check.
3. **Draft area specs.** One file per area, describing current behaviour with the changes from step 1 applied. With no existing specs, derive them from the code and the running app. Code shows what the app does, not what the user meant, so every derived requirement is a question for the user until confirmed. Drift, oddities and scar-tissue candidates become open questions, not silent fixes. Write them as described in [Open questions](#open-questions).
4. **Negotiation rounds.** Propose simplifications, merges, deletions and improvements. Architectural changes are welcome when they serve the goal of simplifying. The user states the changes they want. Each round settles one layer of questions, starting with Shape. Each item ends one of three ways:
    - keep: it goes into the area spec
    - change: the area spec is updated
    - drop: it is deleted everywhere, with no record left
5. **Settle and plan structure.** Settled means no open questions remain, every requirement has acceptance criteria, and every constraint has a test or a stated reason for having none. Then derive the module layout from the areas, one module per area, and agree it with the user.
6. **Pour.** Create the new repo. The first commit is the settled specs, with no code. Build area by area from the specs, using the old code as reference only.
7. **Verify.** The behaviour tests from step 2 and every constraint test pass against the new app.

## Open questions

A survey of a large app turns up far more findings than anyone can answer in one sitting. Sort them before showing any.

**Layers.** Every question belongs to one layer, and a round covers one layer:

| Layer | Holds |
| --- | --- |
| 0 Shape | Area boundaries, merges and splits, and big structural moves |
| 1 Area intent | What each area is for, and which features stay, change or go |
| 2 Detail | Single requirements, drift, unused code and workarounds |

A question that only matters for one answer to another question names it in `show_if`, and stays hidden until that answer is given. Don't write questions an earlier answer is likely to change. Write them in the round after it.

**Confidence.** Every question has a suggested answer and a confidence level:

- **high:** applied without asking unless the user flags it. Most derived requirements belong here.
- **medium:** shown with the suggestion marked.
- **low:** a real fork, marked as needing the user's judgement.

**Groups.** Similar items, such as all the unused parts of one area, become one decision with exceptions rather than one question each.

**Kinds.** Label each question with one kind, shown to the user in plain words:

| Kind | Shown as |
| --- | --- |
| `proposal` | Suggested change |
| `drift` | Spec and app disagree |
| `dead-code` | Unused in the old app |
| `scar` | Workaround for a past problem |
| `derived-req` | Read from the code |

**Wording.** A question is one line. It has at most two sentences of context and two to four answers, each saying in one line what it changes.

### The review page

Where the Artifact tool is available, run the rounds through the review page:

1. Publish `review/recast-review.html` once as an Artifact with `capabilities: {db: {}}` and give the user the link.
2. Write the areas, the questions and `recast/meta` (round 1, status `open`) into its database with `ArtifactData` batches. [`review/SCHEMA.md`](review/SCHEMA.md) gives the layout.

The page shows:

- a map of the proposed areas and where each part of the old app goes
- the current layer's questions, with your suggestions marked
- the selected area's spec as it would read with the answers so far

The page cannot tell you when the user has finished, so the user tells you. When they do:

1. Read `answers` and `recast/meta`. Process every answered question, whatever its layer. Treat unflagged high-confidence questions in the layer just finished as answered with your suggestion.
2. Apply each answer to `specs/<area>.md` and to the area document: keep, change or drop. For "Something else", follow the note, rewriting the spec or asking a follow-up question.
3. Delete the answered questions and their answers. Delete questions the answers made moot. Remove `show_if` where the parent is settled. Add the questions the answers raised. Update the map and `oldParts` if areas merged, split or went.
4. Set `recast/meta` to the next round, status `open`, with a `summary` of what was settled.

At settle the database holds no questions. Offer to delete the artifact, since it keeps no record the specs don't.

Without the Artifact tool, write the current layer to `specs/open-questions.md` with the same fields: ID, kind, question, suggestion and confidence. Ask the user to reply by ID, then apply the answers the same way.

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
