# The Hollow Crown of Karsh Vale

A **Basic Fantasy RPG** one-shot for three player characters and a referee, and the simpler
of the two tabletop samples here. One evening, one ruin, a small handbook.

Eleven sheep, two dogs and a boy named Aldo Fenn have gone missing from the upper pastures
of Karsh Vale, always on a moonless night, always within sight of the ruin the locals call
the Hollow Crown. The reeve is offering forty gold and a cottage for the winter to anyone
who ends it.

> **The other one.** [greyfen-barrows](../greyfen-barrows/) is the full version: the whole
> Basic Fantasy rulebook rather than a page of it, eight beats rather than one evening, and
> written by the product's own assistant rather than by hand. Start here to see the idea in
> twenty minutes; go there to see it carry a real rulebook. The
> [difference is set out below](#how-this-differs-from-greyfen-barrows).

---

## What this sample demonstrates

**Lore in three bands, by how widely it is known.** This is the centrepiece. Every phase of
the flow declares all three bands; the platform then intersects that list with what each
*principal* is entitled to read:

| Band | Who can retrieve it | What lives there |
|------|--------------------|------------------|
| `workspace_public` | the whole table | the Vale, the ruin, the disappearances, the tavern rumour of the tallowmen |
| `guild_lore` | the referee, **Bram** (a stonemason's son) and **Linnea** (college-trained) | how to read masons' marks, and how a binding inscription differs from a decorative one |
| `referee_lore` | the referee alone | what the Crown actually is, why the losses stopped eight days ago, and what the party's real decision will be |

Pip the halfling thief has no route to `guild_lore`, and **no player character has any route
to `referee_lore`**. That is not an instruction anyone can forget or be argued out of: scope
membership is resolved as a SQL predicate on every retrieval, so the text cannot reach their
context. When Bram reads the tool marks and tells the others, the knowledge enters the
fiction the way it should — because a character who plausibly knew said it out loud.

**Knowledge is retrieved, not pasted in.** Every entry here is an ordinary retrievable entry
with activation keys, except one: the note about how this platform's dice work, which is
about every turn and is therefore always-on. Open **Inspect context** on any message and the
lore differs turn to turn, chosen for that moment.

**The rules are common property.** The rulebook is filed under `rules` and open to everyone,
because a rule nobody can look up is not a rule. It is nine entries — an abridgement, enough
to run one evening. The referee still adjudicates; nobody is guessing at the arithmetic.

**Dice are records, not prose.** The resolve phase carries the randomizer and the referee is
told to call it and narrate what it gave — including when it goes badly. A result that was
rolled is the record; a number a model invented is not.

**Reactive turn order.** The players' phase uses `reactive` order, so they answer the referee
and each other rather than marching in a fixed rota.

---

## How this differs from greyfen-barrows

|  | karsh-vale | [greyfen-barrows](../greyfen-barrows/) |
|---|---|---|
| Length | one evening, three scenes | eight beats: creation, introductions, two fights, an interlude, a puzzle, a boss, an epilogue |
| Rules | 9 abridged entries | the whole rulebook, 482 sections, every spell and monster its own entry |
| Bundle | 117 KB | 2.3 MB |
| Lore bands | three: public, guild, referee | two: public and referee |
| Written by | a person | the product's own assistant, from a brief |
| Best for | seeing levels of lore work, quickly | seeing a real rulebook reach the turns that need it |

Both are Basic Fantasy, both carry their own dice binding, and both run standalone. Neither
needs the other.

---

## Run it

1. **Sign up.** Register with any organization name; you land in **Default Workspace** as its
   steward.
2. **Workflows → Tabletop RPG**, *before* importing. The bundle names it and the import would
   pin it anyway; choosing it first also keeps the bundle's own dice binding — the Basic
   Fantasy rule system — as the one the randomizer uses, rather than the pack's generic d20.
3. **Add a model connection.** **Personas → Model profiles → New model profile**: provider,
   model and your API key (built and tested on DeepSeek, `deepseek-chat`).
4. **Import** `karsh-vale.pyr` — on the workspace, **Export / import** (top right). It brings
   the four personas, the handbook, all four knowledge sources, both scope bands, the rule
   system and the flow.
5. **Let the import finish indexing before starting a session.** A freshly imported workspace
   is playable before it is searchable, and a session started immediately retrieves nothing
   for its first turns. Watch **Workspace → Settings → Knowledge budget**; once it reports
   room in each class, you are ready.
6. **Point the personas at your connection.** **Personas** → open each of the four → set
   **Connection (model agent)**. Each carries its own sampling overrides so a shared
   connection still produces four distinct voices.
7. **Start a session** on *The Hollow Crown of Karsh Vale*, referee as supervisor, the three
   players as participants.

Three scenes, then the referee brings it to a resting point with the real decision still in
front of the party. There is deliberately no "correct" ending written down.

### Seeing the bands work

Ask the same question of two characters. Ask Bram what he makes of the stonework and he can
tell you the last builders were sealing something *in*; ask Pip and he genuinely has nothing
— not evasion, just absence. Or open **Inspect context** on a referee turn and a player turn
and compare which entries are in each.

## The characters stay

The party is still there next session. Characters, and each player's binding to theirs,
belong to the **workspace**, not to the session that rolled them — only the transcript is
session-scoped. Start a second session in this workspace and Bram is still Bram, with the hit
points the last fight left him.

It is also the thing to know before running the sample from the top twice. A second run does
not start with blank sheets: the players open with the first party already in context. For a
genuinely fresh start, import the bundle into a fresh workspace.

---

## Attribution and licence

The rules content in this bundle is abridged and restated from the **Basic Fantasy
Role-Playing Game**, 4th edition (release 142), by **Chris Gonnerman** and contributors —
<https://www.basicfantasy.org/> — which is distributed under the **Creative Commons
Attribution-ShareAlike 4.0 International License**
(<https://creativecommons.org/licenses/by-sa/4.0/>).

The rules entries here are a derivative work of that text and are offered under the **same
CC BY-SA 4.0 licence**. No artwork from the rulebook is included.

The bundle also carries the **mechanics** themselves — the `basic_fantasy` rule system and
the tool binding that points the platform's one randomizer at it — so the one-shot is
playable on import without installing a ruleset separately. Those are a conversion of the
system (check types, expression grammar, the ability-modifier table), not of its prose, and
the same attribution and share-alike obligation travels with them. It is carried *inside* the
bundle as its own knowledge entry, so it reaches anyone who imports the file rather than only
someone reading this repository.

The setting — Karsh Vale, Ashmere, the Hollow Crown, the tallowmen, and every named character
— is original to this sample and contains no Basic Fantasy text.
