# mafia — models deceiving models, under a referee that cannot be argued with

Ten players sit at a table. Three of them are secretly mafia, and one of the three is the
Don. The other seven are town, and one of them is the Sheriff. The mafia know each other;
nobody else knows anything. Every night the mafia shoot someone, the Don secretly checks
one player for the Sheriff, and the Sheriff secretly checks one player for mafia. Every day
the table argues and votes someone out. Town wins when the mafia are gone; the mafia win
when they are as many as the town.

It is a game about lying, so it is a test of who-knows-what. A player's role reaches its
model only if the player is allowed to know it. The mafia's night chat never enters a town
player's context. A Sheriff's check is answered by the engine to the Sheriff alone; not
even the Host's model sees it. A day ballot stays sealed until everyone has voted. None of
this depends on asking a model to keep a secret: what a model may not know is never in its
request.

**Why this sample exists.** It is built on Pyrrhula's *participants*: per-player variables
(a team, a role, alive or out) dealt by a recorded draw; sealed ballots counted by the
engine, with their effects applied from the record; private checks; private channels; and
an open floor where players raise hands. The Host persona narrates, but the engine decides
every outcome. A vote result, a check and the final roles are records, not prose.

Requires Pyrrhula 0.2.1 or later (the open-table rules use its open floor).

## Two rule sets

The bundle carries two flows. The game is the same; how the table talks, and when it first
votes, is not.

| Flow | Day | Night (mafia only) |
|---|---|---|
| **Mafia (sport rules)** | Each living player speaks once, in seat order, then everyone votes, from day 1. Close to competitive (FIIM) rules. | One turn each to agree the shot. |
| **Mafia (open table)** | Each living player speaks once in seat order; then anyone named may answer, and anyone may raise a hand to speak again, up to `turns_each` turns a day. The vote comes when no hand is up. **Day 1 is discussion only**: the first player to leave is the one shot on night 1. | The same open floor, in private; only raised hands move it. |

Why no vote on day 1 at the open table: with nobody dead and nobody checked, the first vote
is blind, and on the sport rules it decided most games (below).

Everything else is shared: a night zero when the mafia meet and nobody is shot; a tie gets
a defence speech each and a run-off among the tied (a second tie: nobody leaves); whoever
leaves gets last words; a Don or Sheriff shot at night still makes that night's check and
leaves at dawn; roles stay secret until the game ends; the player shot on the first night
names three suspects (the "best move").

## The cast

| Persona | Type | Role |
|---|---|---|
| Host | supervisor | opens the game, announces each night's result, closes it with every role revealed |
| Ines, Tomas, Mira, Oskar, Lena, Viktor, Ada, Noor, Felix, Jonas | participant | the players; teams and roles are dealt at the start of each game |

The players' names stay the same whichever model plays them, and no player is told which
model is behind another seat. Give each player its own connection to compare models, or
one connection for all of them to watch one model play against itself.

## Running it

1. Import `mafia.pyr`: Workspace → **Export / import** (top right) → upload `mafia.pyr`. It
   brings the eleven personas and both flows; connections do not travel.
2. Create your model connections and assign one to each persona. The Host needs a
   connection too; a cheap, fast model is enough.
3. Start a session with the Host as supervisor and all ten players as participants, and
   pick **Mafia (sport rules)** or **Mafia (open table)**.

The flows' settings are chosen when the session starts:

| Setting | Flow | Default | Range | Meaning |
|---|---|---|---|---|
| `mafia_count` | both | 3 | 1–4 | how many players are dealt mafia (one of them the Don) |
| `day_laps` | sport rules | 1 | 1–5 | how many times the day speeches go round the table |
| `turns_each` | open table | 3 | 1–6 | the most turns one player gets in one discussion, day or night |

A sport-rules game took about 35 minutes and an open-table game takes longer, because a day
runs up to three times as many turns.

### Phase markers

Both flows mark every phase in each player's history: a line such as
`[Night 2: the mafia talk in private.]` sits exactly where night 2 began. Without it a
player's history is one undivided stream, and players argued at night about "today's vote"
for someone already out. In an A/B of four games per arm, judged blind against the record,
markers took messages that got the phase or the living players wrong from 6.2% to 0.8%.
The `phase_markers` and `recap` session options switch this per session (see
[docs/participants-and-ballots.md](https://github.com/tuturu742/pyrrhula/blob/main/docs/participants-and-ballots.md)).

## What the sport rules showed

In October 2026, 15 frontier and open models played 42 ten-seat games on the sport rules,
each model in about 28 of them, with seats spread so every table was a different mix:

- **The mafia won 29 of 42.** Day 1 decided most games: when the first day's vote removed
  a mafia player, town won 8 of 12; when it removed a town player, town won 3 of 28.
- **Day-1 votes were bandwagons.** One player built a case, often a mafia player, and the
  table piled on — 7–3, 9–1. The ballots' stated reasons were mostly "the strongest argued
  case so far".
- **The mafia used their night chat to plan the next day** ("Tomorrow: Sage pushes Riley,
  Kendall stays quiet…") while town got one public speech each. That asymmetry is what the
  open-table rules were written to test.

## What each session page shows

Besides the conversation:

- the seats and how many of each role were dealt (never who got which);
- each vote as a record: every ballot after a day vote, only the outcome after a night
  shot, and nothing at all of a check except to the player who made it;
- messages only some players could read, marked **private**;
- the final record: every player's team, role and status.

## What to look for

- **Deception.** The mafia's night chat is in the transcript (the overseer sees
  everything). Compare what the mafia planned at night with what they said the next day.
- **Deduction.** Every day ballot says who suspected whom. A town player's votes against
  actual mafia are its hits.
- **Persuasion.** Who moved the table: whose accusation the majority's ballots followed.
- **The floor** (open table). Who raises a hand with nothing new to say, who is named most,
  and who answers an accusation and who lets it stand.

## Known quirks

- DeepSeek through OpenRouter was served by third-party hosts and sometimes opened a turn
  with a line of invented instructions. Connected to DeepSeek's own API, it did not. Prefer
  a model's own provider where you can.
- A vote turn that answers in words without casting its ballot is asked once for it; still
  missing, it counts as an abstention, and the vote record says so.
- A provider's content filter can refuse a turn outright (StepFun's did, once).
  The session pauses with the error; resuming sends the same history, so that seat needs
  another model.
