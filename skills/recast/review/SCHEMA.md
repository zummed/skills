# Review page data

`recast-review.html` is published once as an Artifact with `capabilities: {db: {}}`. Everything it shows lives in the artifact's database, which you read and write with the `ArtifactData` tool. The page never needs republishing between rounds.

Four collections:

| Path | Written by | Holds |
| --- | --- | --- |
| `recast/meta` | you, then the page | The round: app name, round number, status, summary, old parts |
| `areas/<area>` | you | One document per area: map position, interfaces, the area spec |
| `questions/<Q-id>` | you | One document per open question |
| `answers/<Q-id>` | the page | The user's answer to one question |

Write in batches (`action: "batch"`, up to 50 writes). Pin every write to an existing document with the `if_version` you last read.

## `recast/meta`

```json
{
  "app": "Larder",
  "round": 2,
  "status": "open",
  "summary": ["Sync and the offline cache are one Sync area", "Legacy v1 API shim dropped"],
  "oldParts": [
    { "name": "Offline cache", "into": ["sync"] },
    { "name": "Custom analytics", "fate": "drop" }
  ]
}
```

- `status` is `open` while the user answers. The page sets it to `submitted`, with `submittedAt`, when they press **Send round to Claude**. You set it back to `open` when the next round is written.
- `summary` lists what the last round settled, in a few words each. The page shows it as a banner.
- `oldParts` are the parts of the old app, named the way a person would describe them, not file paths. `into` names the new areas each one moves to. Use `fate: "drop"` for a part that is going.

## `areas/<area>`

```json
{
  "name": "Pantry",
  "purpose": "What the household has in, and how much.",
  "pos": { "c": 1, "r": 2 },
  "uses": ["sync"],
  "note": "",
  "reqs": [{ "id": "R-pantry-01", "text": "Each household has one pantry listing ingredients with quantity and unit." }],
  "constraints": [{ "id": "C-pantry-01", "text": "Ingredient names match ignoring case and plurals.", "test": "pantry_name_matching" }]
}
```

- `pos` places the box on the map grid: column `c`, row `r`, and an optional width `w` in columns. Use three columns. Put areas next to the areas they use, so lines stay short. Give a shared platform area that everything uses a full-width row of its own (`w: 3`). The page draws no lines to it, so put "Under every data area" or similar in `note`.
- `uses` lists the areas this one depends on. These become the map's arrows and the spec's Interfaces line.
- `reqs` and `constraints` mirror the area spec file. Keep them in step with `specs/<area>.md`.

## `questions/<Q-id>`

```json
{
  "layer": 1,
  "kind": "scar",
  "areas": ["pantry"],
  "order": 4,
  "title": "Store quantities as numbers instead of text?",
  "detail": "Quantities are saved as written, like '1 1/2' or 'a handful', so shopping-list totals are sometimes wrong.",
  "evidence": "A parser with 30 special cases tries to read the text back into numbers.",
  "choices": [
    { "id": "number", "label": "Number and unit", "effect": "Totals add up correctly.",
      "patch": [{ "req": "R-pantry-02", "text": "Quantities are stored as a number and a unit." }] },
    { "id": "text", "label": "Keep free text" }
  ],
  "default": "number",
  "confidence": "low",
  "affects": ["R-pantry-02"],
  "show_if": { "q": "Q-shape-03", "is": ["derive"] },
  "group": { "id": "dead-recipes", "title": "Unused parts of Recipes", "detail": "Nothing in the app reaches these." }
}
```

| Field | Meaning |
| --- | --- |
| `layer` | `0` Shape, `1` Area intent, `2` Detail |
| `kind` | `proposal`, `drift`, `dead-code`, `scar` or `derived-req`. The page shows these as "Suggested change", "Spec and app disagree", "Unused in the old app", "Workaround for a past problem" and "Read from the code" |
| `areas` | Area ids the question belongs to. Empty for whole-app questions |
| `order` | Sort position within its layer |
| `title` | The question, in one line |
| `detail` | Optional. Two sentences of context at most |
| `evidence` | Optional. What in the old app raised it, shown behind "Why this came up". Still above the code: commit counts and behaviour, not file paths or function names |
| `choices` | Two to four answers. The page adds "Something else…" itself |
| `choices[].effect` | Optional. One line on what this answer changes |
| `choices[].patch` | Optional. Spec lines this answer rewrites. `text: null` removes the line, and a new id adds one. The spec preview applies these live |
| `choices[].short` | Optional. A one-word label used in grouped rows |
| `default` | Your suggested choice id |
| `confidence` | `high`, `medium` or `low`. High is applied without asking unless the user flags it. Low is marked "Needs your judgement" |
| `affects` | Optional. Spec ids a "Something else" answer leaves needing a rewrite |
| `show_if` | Optional. Hide this question until question `q` is answered with one of the `is` choices. If `q` gets any other answer, this question no longer applies |
| `group` | Optional. Questions with the same `group.id` and the same choices show as one card with "… all" buttons |

## `answers/<Q-id>`

Written by the page, one per question the user touched:

```json
{ "choice": "number", "note": "Keep the original text too.", "flagged": false, "at": "2026-10-09T13:46:27Z" }
```

`choice` is `null` if the user cleared it, and `"other"` for "Something else", which should come with a `note`. `flagged: true` on a high-confidence question means the user wants it asked properly.
