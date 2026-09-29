# The Greyfen Barrows

An eight-beat **Basic Fantasy RPG** campaign for three player characters and a referee,
carrying the whole rulebook, and **written by the product's own assistant** rather than by a
person.

A spring landslide has cracked open a chieftain's barrow on the high moor above Cromlech.
Since then livestock have gone missing and pale things walk the mist. The reeve is offering a
land-charter and coin to anyone who will go up and stop it.

> **The other one.** [karsh-vale](../karsh-vale/) is the simpler version: one evening, nine
> pages of rules, hand-written. Start there if you want the idea in twenty minutes. The
> [difference is set out below](#how-this-differs-from-karsh-vale).

---

## What this sample demonstrates

**Knowledge that is retrieved, not injected.** Every lore entry here is an ordinary
retrievable entry; **none** is always-on. Open **Inspect context** on a turn and you will see
them arriving as `dense+keyed+reranked`, chosen for that moment, different from the turn
before. That is what a handbook is for, and it is the thing a sample can accidentally fail to
demonstrate by marking everything always-on.

**The whole rulebook, reachable.** The bundle carries the Basic Fantasy Role-Playing Game as
**482 entries**, one per section, each spell and each monster its own entry. Activation keys
are derived from the titles when the source is published, so a turn naming a goblin, a saving
throw or a Fighter pulls that section rather than whatever the prose happens to resemble.
Encounters are built from creatures that are actually in the book, with their real statistics.

**Levels of lore.** Two entries are filed under `facilitator_only`: what is really happening
under the barrow, and how it ends. Measured over a live run, they appeared in every referee
turn and no player turn — not because anyone is told to keep quiet, but because the scope is
resolved as a database predicate before a context is built.

**Dice that are records.** Character creation rolls 3d6 six times per character through the
randomizer under the `basic_fantasy` rule system and binds a real character sheet. Hit points
came out exactly right across two runs: class hit die plus the Constitution modifier, with the
minimum of one per die applied.

**Written by the assistant.** The setting, the eight lore entries, the four personas, the
eight-beat flow and the session were authored by the workspace assistant from a brief, through
its propose-then-confirm interface. It read the rulebook to choose its monsters and read an
existing flow to learn the document shape. Nothing in the bundle was written by hand.

---

## How this differs from karsh-vale

|  | greyfen-barrows | [karsh-vale](../karsh-vale/) |
|---|---|---|
| Length | eight beats: creation, introductions, two fights, an interlude, a puzzle, a boss, an epilogue | one evening, three scenes |
| Rules | the whole rulebook, 482 sections | 9 abridged entries |
| Bundle | 2.3 MB | 117 KB |
| Lore bands | two: public and referee | three: public, guild, referee |
| Written by | the product's own assistant, from a brief | a person |
| Best for | seeing a real rulebook reach the turns that need it | seeing levels of lore work, quickly |

Both are Basic Fantasy, both carry their own dice binding, and both run standalone.

---

## What this sample does not do well

Read this before you judge the output.

**It does not enforce prime requisites.** Basic Fantasy requires a class's prime requisite to
be 9 or better. Across two runs, two of six characters were illegal — a Cleric with Wisdom 7
and a Magic-User with Intelligence 6 — and the referee declared both in order. The rulebook was
attached and searchable; the rule simply was not in the referee's context at the moment it
validated, because retrieval is driven by what the previous speaker *said*, and a player
announcing a class in character never names the rule that governs it. Check the sheets
yourself, or say so to the referee and it will correct them.

**The first beat can run before indexing finishes.** A freshly imported workspace is playable
before it is searchable. Timed on one run, the embedding sweep took four minutes and the first
four turns ran inside it, so character creation happened with nothing retrieved at all. Wait
for **Workspace → Settings → Knowledge budget** to report room in each class before starting.

---

## Before you start

- a Pyrrhula deployment you can sign up on
- an API key from a model provider (built and tested on **DeepSeek**)

Four agents through eight beats is not free. Run the first beat and check what your provider
charges before letting it run to the end.

## Run it

1. **Sign up.** Register with any organization name.
2. **Add your model connection.** **Personas → Model profiles → New model profile**: your
   provider, model and key.
3. **Import** `greyfen-barrows.pyr` on the workspace, under **Export / import**. It brings the
   rulebook, the setting, the cast, the flow and the Basic Fantasy rule system the dice
   validate against.
4. **Wait for indexing** — see above. The bundle is 2.3 MB and takes a few minutes to embed.
5. **Point the cast at your connection.** **Personas** → open each of the four → set
   **Connection**.
6. **Start a session** on *The Greyfen Barrows* with the referee as supervisor and the three
   players as participants. It opens at character creation.

The combat beats run several rounds with the referee taking a turn between them.

## What to look at

- **Workspace → Settings → Knowledge budget.** Every class has room for retrieval and nothing
  is always-on. That is what makes attaching a 482-section rulebook worth doing at all.
- **Inspect context** on any message. The lore entries differ turn to turn, and the rules
  entries are the ones the turn was about.
- **A referee turn against a player turn.** The two `gm_` entries are in one and not the other,
  every time.

---

## Attribution and licence

The rules content is the **Basic Fantasy Role-Playing Game**, 4th edition (release 142), by
**Chris Gonnerman** and contributors — <https://www.basicfantasy.org/> — distributed under the
**Creative Commons Attribution-ShareAlike 4.0 International License**
(<https://creativecommons.org/licenses/by-sa/4.0/>). It travels here under the same licence, as
does the `basic_fantasy` rule system and the randomizer binding that carries its check types.
No artwork is included.

`tools/bfrpg_odt_to_entries.py` in this repository is how the rulebook was converted from the
published `.odt` into one entry per section, so the derivation is reproducible and checkable.

The setting — the Greyfen, Cromlech, the Grey King's barrow and every named character — was
generated for this sample and contains no Basic Fantasy text.
