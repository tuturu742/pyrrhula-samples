# The Hägnaryd Case

A closed-house murder for six agents: one investigator and five suspects, one of whom did
it. Everyone is lying about something; the question is which lies matter.

**Why this sample exists.** Every character holds private information the others cannot
see — not because their prompt asks them to keep quiet, but because the text is *not in
their context*. The murderer's account of the killing exists in exactly one agent's
context, and no amount of clever questioning by another agent can pull it out of the
system, because it was never there to pull.

Two people in this house planned to kill Ingeborg Wallmark that evening. Only one of them
did.

---

## Before you start

You need:

- a Pyrrhula deployment you can sign up on,
- an API key from a model provider (this was built and tested on **DeepSeek**, which costs
  very little for a run like this).

Six agents talking is not free. Run a few turns first and check what your provider
charges.

---

## Step 1 — Sign up

Open Pyrrhula and register. Pick any organization name.

When you land, you are in a workspace called **Default Workspace**, and your role in it is
**steward** — the seat that can both build the room and inspect it. You will need both
halves here.

## Step 2 — Choose the Tabletop RPG workflow

**Do this before importing.** Go to **Workflows** and select **Tabletop RPG**.

This loads the personality dials the cast uses (how deceptive each character is, how
readily their secrets surface under pressure). If you import first, the dials arrive with
nothing to attach to and the cast will be flat.

## Step 3 — Add your model connection

Go to **Personas → Model profiles → New**, and fill in:

- **Name**: `DeepSeek` (anything you like)
- **Provider**: `deepseek`
- **Model**: `deepseek-chat`
- **API key**: your key

Save. This is the only place your key lives; it is never written into a bundle.

## Step 4 — Import the case

Go to your workspace, open **Export / Import**, and upload
[`hagnaryd-mystery.pyr`](hagnaryd-mystery.pyr).

The report should tell you it imported:

- **6 personas** — `lind` (the investigator) and `viktor`, `elin`, `lager`, `sofia`,
  `marta`
- **11 secrets** — the private briefs
- **1 flow** — "The Hägnaryd Case"
- **1 knowledge attachment** — the shared setting
- the vocabulary, *bound to the one already here* rather than duplicated

It will also say each persona was "bound to placeholder (connection did not travel)".
That is correct — that is step 5.

## Step 5 — Point the cast at your connection

Go to the workspace's **Personas** page. Open each of the six and set its **model profile**
to the connection you made in step 3. Save.

## Step 6 — Turn on the disclosure gate

On the workspace page, find the **Secrets gate** card and switch it **on**.

This is what decides, per turn, whether a character's own secret may surface — as a hint,
as a full reveal, or not at all. With it off, held secrets never enter context at all:
still leak-proof, but the suspects have nothing to hide and the case is not a case.

In the same card, paste this as the **conduct rules**:

```
Speak only as your own character, in first person. Never write another character's
dialogue, thoughts, or actions, and never repeat or summarise what someone else just said
as if it were your own account. Do not prefix your reply with your name or anyone else's.
Keep replies under 180 words, in short paragraphs of two to four sentences with a blank
line between them. Do not invent people, evidence, or events beyond your briefing and what
has been said at this table.

Never repeat another person's words as your own. If the previous speaker just said
something, do NOT restate it -- react to it, contradict it, or answer the question you
were actually asked. Your reply must be different in substance from every message above
it; copying the last message is the worst possible answer.
```

## Step 7 — Start the interview

Create a new session in the workspace:

- **Flow**: `The Hägnaryd Case`
- **Supervisor**: `Kriminalinspektör Petra Lind`
- **Participants**: the other five
- **Agenda**: paste this —

```
The group interview in the library at Hägnaryd Manor, 09:00 Sunday. Kriminalinspektör
Petra Lind questions the five about the evening Ingeborg Wallmark was killed in her study.
Each answers in character. In the final round the inspector delivers a ranked list of the
five suspects and names the person she would arrest.
```

Then run it.

---

## What you should see

**The cast knows the house.** Ask about the layout or the evening and you get the service
staircase, the gallery, the 19:30 dinner, the body found at 20:40. That comes from the
shared setting handbook, which every agent retrieves.

**Each suspect runs their own cover story.** These are not improvised — they come from
each character's private brief. In a verified run the very first answers were:

> **Dr. Henrik Lager:** "You asked about my phone, didn't you. […] I keep it on silent,
> always have. As for the message, I did not see it until well after dinner."

> **Elin Wallmark:** "I was next to the piano from half past six, working through some
> pieces. I did step out once — just past seven, to the kitchen for ice."

Lager's line is his brief's instruction for what to say if the text message comes up.
Elin's is her alibi, word for word. Neither agent was told to say it by the agenda; it is
in their context and in nobody else's.

**Nobody can see anyone else's brief.** Open the **Secrets** page and you will see all
eleven, each held by exactly one character. That holder list is what the system enforces:
Viktor's context contains Viktor's two secrets and no others.

## Playing it out

The investigator has two lab requests she can spend, listed at the end of her dossier
(recover the speech file, phone records, the pre-dinner clothing, the tower stairs, prints
in the suite, the safe, the guest rooms, phone searches). The case is solvable: six
independent items converge on one person, and no single one of them convicts.

If you want to check your table's answer, the solution is not in this repository on
purpose — the bundle contains only what the *characters* know. The investigator's dossier
is in her brief; you can read it on her persona page if you want to referee.

## Things worth knowing

- **The gate fails closed.** If the gate's model call fails, every secret is concealed
  for that turn and the reason is recorded. With DeepSeek you will see exactly that:
  `deepseek-chat` rejects the structured-output format the gate asks for, so the gate
  conceals every time. The characters still act on their briefs — concealment keeps the
  *motivation* and removes only the plaintext — but you will not see hints or in-character
  reveals until you point the gate at a model that supports structured output.
- **Cost.** Six agents, plus one extra small call per secret-holding turn while the gate
  is on.
