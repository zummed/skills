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

- **The user's goals decide.** The user says what the new code is for, in order, and what must hold everywhere. Everything proposed or built is weighed against that first.
- **Talk above the code.** The user will not know the internals of a vibe-coded app. Pitch findings, questions and proposals at a level a technical person can follow without reading the code, in the words the user uses: what a part does, how the parts fit together, and what would change. No function names, file paths or line-level detail.
- **Small decisions are yours.** Make them by the user's goals and say what you chose. Bring the user only choices that change what the app is for someone using it, a few at a time, in prose.
- **Two-way.** You propose opportunities, the user states changes, and rounds continue until settled.
- **Specs describe the current state only.** No history, no "previously", no changelog.
- **Removals vanish.** A cut item lives only in `open-questions.md` while it is being negotiated, then it is deleted. The old repo is the archive.
- **Code stays clean.** No spec references in code comments. The link between spec and code lives in commit messages.
- **Fresh repo.** The old app stays available as the reference while the new one is built, and is never edited.
- **Simple.** Overviews, lean rules behind them, IDs in commits, and a temporary open-questions file. Nothing else joins the specs.

## Spec structure

Specs are split into areas, and each area maps one-to-one to a code module. Each area has two files, because the user has to be able to read the design and a list of numbered rules hides it.

```
specs/
  README.md            the whole app in a page, and the map of areas
  <area>.md            the overview of an area: what the user reads
  rules/<area>.md      the rules behind the overview: what the tests are written against
  open-questions.md    exists only during negotiation
```

**The overview** is the authority. It is plain prose grouped by topic, with worked examples and drawings where they help, and no IDs: what the area is for, how it behaves, and which other areas it uses. The README page and the overviews are what the user approves, reading as much of them as they choose.

**The rules** sit under the same topic headings as the overview, requirements and then constraints under each, and say nothing the overview does not. The user need not read them.

A requirement is a behaviour and the test or captured case that shows it:

> **R-cal-01** A week's view shows every event that starts or ends in that week. *Test:* `week_view_shows_events_that_span_weeks`

A constraint is scar tissue: a rule learned the hard way, one line of why, and the test that proves it:

> **C-cal-03** Calendar queries must follow `@odata.nextLink`. Graph pages results, and a single request silently drops events. *Test:* `graph_calendar_pagination`

The test checks the app's handling, not the outside service. For an external API quirk, fake the response and assert the app copes. A constraint that cannot be tested, such as one on timing or rate limits, carries `Test: none` and the reason.

**A rule earns its place.** It states a behaviour that something outside the area relies on, or it guards something that matters (data, a secret, money, the user's machine), or it is scar tissue. Wording, small edges, internal names and what another rule already says are left to the overview and the tests. A sentence with no check to name is overview, not a rule.

IDs take the form `<type>-<area>-<nn>`. They are stable and never reused.

## The process

Seven steps. Steps 1 to 5 read the old repo and write into the new repo's folder, which has no commits until step 6. Working material that is not spec (survey reports, research, audits) goes in a `.recast/` folder there, kept out of git.

1. **Survey.** Read the old code, any specs and the git history, then report per area:
    - what the code actually does
    - where the specs have drifted
    - dead code, duplication and inconsistent patterns
    - scar-tissue candidates: fix commits, special cases, retries, odd error handling, "workaround" or "hack" comments

    End the report by asking the user three things: what they already want changed, added or dropped; what the new code is for (their goals in order, and anything that must hold everywhere); and which other programs use the app, and whether they adapt to the new one or it to them. Wait for the answers before step 2: every later choice rests on them.
2. **Capture behaviour.** For the parts being kept only, write behaviour tests or golden examples against the old app. These captured cases go into the new repo as its parity check.
3. **Draft the overviews.** One per area, describing current behaviour with the changes from step 1 applied. With no existing specs, derive them from the code and the running app. Code shows what the app does, not what the user meant: where the two might differ, decide by the goals, write the choice into the overview, and say in the next round what you chose. Only the choices that change what the app is for someone using it go into `open-questions.md`.
4. **Negotiation rounds.** Propose simplifications, merges, deletions and improvements. Architectural changes are welcome when they serve the user's goals. The user states the changes they want. Each item ends one of three ways:
    - keep: it goes into the overview
    - change: the overview is updated
    - drop: it is deleted everywhere, with no record left

    Before settling, have a reader with no part in the writing try to break the overviews, and give the user that view.
5. **Settle and plan structure.** Settled means `open-questions.md` is empty and deleted and the user has agreed the overviews. Then write the constraints from the survey's scar tissue, each with its test or a stated reason for having none. Derive the module layout from the areas, one module per area, and agree it with the user.
6. **Pour.** Create the new repo with an instructions file (`CLAUDE.md` or the like) holding the user's goals, this skill's rules for specs and commits, and the order of building. The first commit is that file, the settled specs and the captured cases, with no code. Build area by area from the overviews, using the old code as reference only. An area's requirements are written as it is built, each in the same commit as its code and its test, and a constraint's test is written with the code it guards.

    Building finds what the overviews left unsaid. Fill a small gap by the goals and say what you chose. When a gap changes what the app does, or you have built something the agreed design did not contain, take it to the user first: the overview changes before the code, with their agreement, and a breach of one of their principles is never written into an overview as a known limit. This holds for all later work, so it goes in the instructions file too.
7. **Verify.** Passing tests do not show that the specs were built. Before saying the recast is done:
    - the captured cases pass against the new app, and a case the design changes on purpose has had its expected result changed
    - every rule's named test exists and passes; count the names in the rules against the tests
    - every overview has been read against the code; what it promises and is missing is built, or, where nobody needs it, taken out of the overview and named in the report
    - the app has run for real at least once, against the real services it depends on and not stand-ins; the user decides which services are tried and supplies the keys, which stay out of the repo

    Report in one short page, and say plainly what has not been built, checked or run for real.

## Commit conventions

Commits carry the link between spec and code, so the code itself stays clean.

- **The first commit has no code.** History starts from intent.
- **A behaviour change updates its overview and its rules in the same commit as the code.**
- **The message names the area, plus the ID when one applies:** `cal: follow nextLink pagination (C-cal-03)`
- **Refactors and tooling changes need no ID**, only the area prefix.

## Making the next recast easy

The next survey becomes a per-area diff rather than an archaeology dig, because of five things set up here:

- Areas mirror modules, so each spec is compared against one module.
- Specs hold only the current state, so there is nothing stale to wade through.
- The instructions file holds the goals, so the next recast starts from what the code is for.
- Constraints and their tests survive into the new repo, so the scar tissue is never mined twice.
- Commits carry IDs, so a grep per area shows what changed and why.

Tag the commit at which step 7 is done, for example `recast-1`. The next survey then reads only the commits since that tag.
