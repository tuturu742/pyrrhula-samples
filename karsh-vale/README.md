# The Hollow Crown of Karsh Vale

A **Basic Fantasy RPG** one-shot for three player characters and a referee, and the
sample that shows what a tabletop session looks like when *who knows what* is enforced by
the platform instead of asked of the model.

Eleven sheep, two dogs and a boy named Aldo Fenn have gone missing from the upper
pastures of Karsh Vale, always on a moonless night, always within sight of the ruin the
locals call the Hollow Crown. The reeve is offering forty gold and a cottage for the
winter to anyone who ends it.

---

## What this sample demonstrates

**Lore in three bands, by how widely it is known.** This is the centrepiece. Every phase
of the flow declares all three bands; the platform then intersects that list with what
each *principal* is entitled to read:

| Band | Who can retrieve it | What lives there |
|------|--------------------|------------------|
| `workspace_public` | the whole table | the Vale, the ruin, the disappearances, the tavern rumour of the tallowmen |
| `guild_lore` | the referee, **Bram** (a stonemason's son) and **Linnea** (college-trained) | how to read masons' marks, and how a binding inscription differs from a decorative one |
| `referee_lore` | the referee alone | what the Crown actually is, why the losses stopped eight days ago, and what the party's real decision will be |

Pip the halfling thief has no route to `guild_lore`, and **no player character has any
route to `referee_lore`**. That is not an instruction anyone can forget or be argued out
of: scope membership is resolved as a SQL predicate on every retrieval, so the text
cannot reach their context. When Bram reads the tool marks and tells the others, the
knowledge enters the fiction the way it should — because a character who plausibly knew
said it out loud.

**The rules are common property.** The rulebook is filed under `rules` and open to
everyone, because a rule nobody can look up is not a rule. The referee still adjudicates;
nobody is guessing at the arithmetic.

**Miscellany gets a real budget.** The counting rhyme, the inn's candle custom, the
running joke about Karsh Vale cheese and Marta Fenn setting two places are filed under
`misc` and funded in the scene and reckoning phases. This is the texture a session loses
when a budget funds only rules and plot. (The rhyme is also, if you read it twice, the
whole plot.)

**Dice are records, not prose.** The resolve phase carries the randomizer and the referee
is told to call it and narrate what it gave — including when it goes badly. A result that
was rolled is the record; a number a model invented is not.

**Reactive turn order.** The players' phase uses `reactive` order, so they answer the
referee and each other rather than marching in a fixed rota.

---

## Run it

1. **Sign up.** Register with any organization name; you land in **Default Workspace**
   as its steward.
2. **Workflows → Tabletop RPG**, *before* importing. The bundle names it and the import
   would pin it anyway; choosing it first also keeps the bundle's own dice binding — the
   Basic Fantasy rule system — as the one the randomizer uses, rather than the pack's
   generic d20.
3. **Add a model connection.** **Personas → Model profiles → New model profile**:
   provider, model and your API key (built and tested on DeepSeek, `deepseek-chat`).
4. **Import** `karsh-vale.pyr` — on the workspace, **Export / import** (top right). It
   brings the four personas, the rulebook, all four knowledge sources, both scope bands,
   the rule system and the flow.
5. **Point the personas at your connection.** **Personas** → open each of the four → set
   **Connection (model agent)**. Each carries its own sampling overrides (the referee
   cool at 0.6, the players looser) so a shared connection still produces four distinct
   voices.
6. **Start a session** on the *The Hollow Crown of Karsh Vale* flow, with the referee as
   supervisor and the three players as participants. The referee opens the scene; you
   can watch or take a seat yourself.

Three scenes, then the referee brings it to a resting point with the real decision still
in front of the party. There is deliberately no "correct" ending written down.

**Or run the long one.** The bundle's flow is an evening. The `rpg` workflow pack also
ships *A Campaign in Three Encounters* (`karsh_vale_campaign`), which uses this same cast
and rulebook across eight beats — character creation, introductions, two encounters with
an interlude between them, a puzzle, a boss fight and an epilogue. Its combat beats run
three rounds each, with the referee taking a turn between rounds, so a fight is a fight
rather than one action per player. Pick it on the session-start screen the same way.

### Seeing the bands work

The quickest proof is to ask the same question of two characters. Ask Bram what he makes
of the stonework and he can tell you the last builders were sealing something *in*; ask
Pip and he genuinely has nothing — not evasion, just absence. Or open the knowledge page
as different personas and watch the sources appear and disappear.

## The characters stay

The party is still there next session. Characters, and each player's binding to theirs,
belong to the **workspace**, not to the session that rolled them — only the transcript is
session-scoped. That is the point for a table that meets again: start a second session in
this workspace and Bram is still Bram, with the hit points the last fight left him.

It is also the thing to know before you try to run the sample from the top twice. A second
campaign here does not start with blank sheets: the players open with the first party
already in context, and a player who reads it will reasonably decline to roll a character
it already appears to have. Archiving the first session does not help — archiving hides a
session, it does not remove what the session made.

For a genuinely fresh campaign, use a fresh workspace: create one, import the bundle into
it, point the cast at your connection again, and archive the old one when you are done
with it. Archiving keeps its history; nothing in the product erases a workspace, by
design.

---

## Attribution and licence

The rules content in this bundle is abridged and restated from the **Basic Fantasy
Role-Playing Game**, 4th edition (release 142), by **Chris Gonnerman** and contributors —
<https://www.basicfantasy.org/> — which is distributed under the
**Creative Commons Attribution-ShareAlike 4.0 International License**
(<https://creativecommons.org/licenses/by-sa/4.0/>).

The rules entries here are a derivative work of that text and are offered under the
**same CC BY-SA 4.0 licence**. No artwork from the rulebook is included.

The bundle also carries the **mechanics** themselves -- the `basic_fantasy` rule system
and the tool binding that points the platform's one randomizer at it -- so the one-shot
is playable on import without installing a ruleset separately. Those are a conversion of
the system (check types, expression grammar, the ability-modifier table), not of its
prose, and the same attribution and
share-alike obligation travels with them. It is carried *inside* the bundle as its own
knowledge entry, so it reaches anyone who imports the file rather than only someone
reading this repository.

The setting — Karsh Vale, Ashmere, the Hollow Crown, the tallowmen, and every named
character — is original to this sample and contains no Basic Fantasy text.
