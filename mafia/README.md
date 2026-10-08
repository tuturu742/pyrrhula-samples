# mafia — models deceiving models, under a referee that cannot be argued with

Seven players sit at a table. Two of them are secretly mafia; they know each other, and
nobody else knows anything. Every night the mafia quietly pick someone to take out; every
day the table argues and votes someone out. Town wins when the mafia are gone; the mafia
win when they are as many as the town.

It is a game about lying, so it is a test of who-knows-what. A player's role reaches its
model only if the player is allowed to know it. The mafia's night chat never enters a
town player's context. A day ballot stays sealed until everyone has voted. None of this
depends on asking a model to keep a secret: what a model may not know is never in its
request.

**Why this sample exists.** It is the first flow built on Pyrrhula's *participants*:
per-player variables (a role, alive or out) dealt by a recorded draw; seat-order turns
that skip whoever is out; sealed ballots counted by the engine, with their effects applied
from the record; and private channels whose messages reach only their members. The Host
persona narrates, but the engine decides every outcome. A vote result, an elimination and
the final roles are records, not prose.

Requires Pyrrhula 0.2.0 or later.

## The cast

| Persona | Type | Role |
|---|---|---|
| Host | supervisor | opens the game, announces each night's result, closes it with every role revealed |
| Ines, Tomas, Mira, Oskar, Lena, Viktor, Ada | participant | the players; roles are dealt at the start of each game |

The players' names stay the same whichever model plays them, and no player is told which
model is behind another seat. Give each player its own connection to compare models, or
one connection for all of them to watch one model play against itself.

## Running it

1. Import `mafia.pyr`: Workspace → **Export / import** (top right) → upload `mafia.pyr`. It brings the eight
   personas and the **Mafia** flow; connections do not travel.
2. Create your model connections and assign one to each persona. The Host needs a
   connection too; a cheap, fast model is enough.
3. Start a session with the Host as supervisor and the players you want as participants,
   and pick the **Mafia** flow.

| Players | `mafia_count` | Notes |
|---|---|---|
| 4 | 1 (the default) | starts with a day; enough to see voting, ties and elimination |
| 7 | 2 | starts with a night; adds the mafia's private night chat |

The flow's settings are chosen when the session starts:

| Setting | Default | Range | Meaning |
|---|---|---|---|
| `mafia_count` | 1 | 1–4 | how many players are dealt mafia |
| `day_laps` | 2 | 1–20 | how many times the day discussion goes round the table |

Any player may answer `pass` when it has nothing to add. Real games run long; raise
`day_laps` for anything you mean to measure.

## A game, as it was played

With seven seats and two mafia on a mix of hosted models through OpenRouter, the four
games of the October 2026 test runs went like this:

- Night 1: the two mafia agreed on a target in their private chat and both voted for it.
  The dawn announcement named the player and their revealed role.
- Day 1: the table argued over two laps and voted. When the town found a mafia player,
  the town won within the next day. When it voted out one of its own, the arithmetic
  belonged to the mafia: after the next night they were as many as the town.
- In the 4-seat test game, the first day's vote tied 2–2, so nobody went out (that is the rule),
  the lone mafia took a player out that night, and the final three voted the mafia out.

What each session page shows, besides the conversation:

- the seats and how many of each role were dealt (never who got which);
- each vote as a record: every ballot after a day vote, and only the outcome after a night
  vote, because who voted at night would give the mafia away;
- messages only some players could read, marked **private**;
- the final record: every player's role and status.

## What to look for

- **Deception.** The mafia's night chat is in the transcript (the overseer sees
  everything). Compare what the mafia planned at night with what they said the next day.
- **Deduction.** Every day ballot says who suspected whom. A town player's votes against
  actual mafia are its hits.
- **Persuasion.** Who moved the table: whose accusation the majority's ballots followed.
- **Silence.** A player that keeps answering `pass` is playing a strategy, and it shows.

## Known quirks

- Some hosted reasoning models occasionally open a turn with a line of their own
  instructions ("Do not announce your vote now…"). It comes from the provider's output,
  not from the game.
- A vote turn that answers in words without casting its ballot is asked once for it;
  still missing, it counts as an abstention, and the vote record says so.
