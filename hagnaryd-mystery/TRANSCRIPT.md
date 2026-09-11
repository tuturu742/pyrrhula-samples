# The Hägnaryd interview — an annotated, unedited transcript

**What you are reading:** one complete session of the [hagnaryd-mystery](README.md) sample,
run on a stock Pyrrhula deployment exactly as its README describes — cast on
`deepseek-chat`, the disclosure gate on `gpt-4.1-mini` — and exported afterwards with its
per-turn gate decisions. Nothing below is edited, cherry-picked from multiple runs, or
retouched; one model slip is left in and annotated.

**Why it exists:** so you can see Pyrrhula's central claim working before you install
anything. Six agents sit in a room. Five of them hold private briefs — including the
murderer's own confession — and the engine, not the prompt, decides each turn whether a
secret may be **concealed** (its text is removed from the model's context entirely),
**hinted** (only an author-written hint enters), or **revealed**. A concealed secret cannot
leak, because the model never has it.

> **Spoiler note:** the annotations name who did it. If you would rather play the mystery
> cold, stop here and [run the sample instead](README.md).

**The cast** — each a separate agent; none can see another's brief:

| At the table | Who they are |
|---|---|
| Kriminalinspektör Petra Lind | The investigator. Holds no secrets; works only from what is said. |
| Marta Sjöberg | Housekeeper, 31 years. Holds two private facts. |
| Dr. Henrik Lager | Family physician and foundation treasurer. Holds three. |
| Viktor Wallmark | Son. Holds two. |
| Sofia Nyqvist | Secretary and companion. Holds two. |
| Elin Wallmark | Daughter. Holds two — one of them is the murder. |

Before every speaking turn, the gate (a small structured-output model that sees only
topical *gists*, never the secret text) rules on each secret the speaker holds. The boxed
lines below each header are those rulings, read back from the session's
`disclosure_decision` records — the same records the Director's View shows a table owner
live.

---

### Kriminalinspektör Petra Lind

Everyone, sit down, please. Thank you for coming — I know this is the house you were staying in, and I know none of you slept.

I'm Kriminalinspektör Petra Lind. I'm going to take you through the evening one by one, and I want to say two things before we start.

First: at lunch on Saturday, Ingeborg Wallmark told you she had "a few pages for you all tonight" about the future of the works and of this family. Whatever that speech said, it is now in my evidence bag, because the printer in her study still held the paper. So if anyone is about to tell me they had no idea anything was coming — think again.

Second: I've read the house. One water tank for the whole building. The east-wing bedroom door on a spring latch that only the housekeeper's key opens. A locked study door with the key left in the lock from the inside. By this afternoon I expect to know how Ingeborg Wallmark died, but I already know this much — whoever killed her had no need to break a door down. They walked to her.

We'll start with Dr. Lager, and then work our way round. Marta Sjöberg, please stay close by; I'll want you after.

Dr. Lager — walk me through your evening. From the moment Ingeborg said she'd bathe before dinner.

*The inspector holds no secrets — her turn runs on the shared case file alone: the house, the water tank, the keys.*

---

### Marta Sjöberg

> **⚙ The gate, before this turn ran** *(real `disclosure_decision` rows for this turn)*:
> - 💡 `hint` — what she found: the service-stair door swinging at 19:05 — and that no ice had been taken
> - 🔒 `conceal` — her ten minutes drinking in the cellar at exactly the wrong time

Dr. Lager answers the inspector in his slow, careful voice — he keeps his hands flat on the table:

"After she said she'd bathe, I went down and joined the others in the salon. There was sherry before dinner. I stayed there until we sat down."

He pauses, then adds, without being asked:

"At one point I went up to the east-wing corridor. She wanted her Madeira from the cellar and I carried the tray up to her study door. I set it down — she takes it inside when she's ready. I didn't go in. I came straight back down."

He does not mention the door standing open. He does not mention the bath water running in the east wing. He does not mention how long he was gone. He folds his hands and waits for the next question.

*⚠ An honest flaw, left in: this is Marta's turn, but DeepSeek slipped and narrated Dr. Lager instead — the doctor gives his own account two turns later. We publish the transcript unedited because the engine's guarantee is not that a cheap model always acts well; it is about what the model **couldn't know**. Note what the slip itself shows: the gate had injected Marta's *hint* (the swinging door), and even mis-voiced, the model circles it — "he does not mention the door standing open." Her cellar drinking stayed concealed: it is nowhere in this text because it was nowhere in the context.*

---

### Dr. Henrik Lager

> **⚙ The gate, before this turn ran** *(real `disclosure_decision` rows for this turn)*:
> - 🔒 `conceal` — **his own murder plan** — he had greased the tower stairs to kill her later that night
> - 🔒 `conceal` — his embezzlement from the foundation
> - 💡 `hint` — what he saw: Elin coming in from the kitchen corridor at 19:06 — with no ice

I'll take that as my cue to speak for myself, then.

After Ingeborg said she'd bathe before dinner, I went down and joined the others in the salon. There was sherry before dinner. I stayed there until we sat down at table.

At one point I went up to the east-wing corridor. She wanted her Madeira from the cellar, and I carried the tray up to her study door. I set it down — she takes it inside when she's ready. I didn't go in. I came straight back down.

That's my evening. What else do you want to know?

*Two of the three facts concealed here are enormous: Lager had **his own murder planned** for later that night, and he was embezzling. The model playing him doesn't produce a nervous liar — it produces a man of studied blandness, because those facts were removed from its context entirely, and the author's directive (keep your account short, volunteer nothing) is all that remains. The third fact — he saw Elin at 19:06 with no ice — came through as a `hint`: the model knows only the author's hint text, not the fact itself, and you can watch it not quite surface.*

---

### Viktor Wallmark

> **⚙ The gate, before this turn ran** *(real `disclosure_decision` rows for this turn)*:
> - 💡 `hint` — what he saw: Lager leaving the tower corridor with a cloth at 18:40
> - 🔒 `conceal` — his falsified board reports and the email spying

I stayed in the salon with the others until we sat down. Sherry, then straight through to the dining room when Marta called us at 19:55. I didn't go up to the east wing at any point before we found her.

What I will say — and I say it because you'll want it before I say anything else — is that Henrik carried that tray up and came back down, and I've no idea what he did in between. He was gone long enough that Elin asked where he'd got to. He never mentioned the bath running or a door standing open until just now, and he's had all night to think about it. That's not an accusation. It's a question I'd want asked if I were sitting where you are.

*Viktor's `hint` visibly lands: he can't say what he actually saw (Lager with a cloth at 18:40 — that fact is not in his context), but the hint steers him to point the room at Lager's unaccounted minutes. His own falsified reports stay concealed — notice he deflects **before anyone asked him anything**.*

---

### Sofia Nyqvist

> **⚙ The gate, before this turn ran** *(real `disclosure_decision` rows for this turn)*:
> - 💡 `hint` — the timings she holds: the piano gap, the gallery, the four-page draft
> - 🔒 `conceal` — her leak to Kastrup — and that Ingeborg confronted her twenty minutes before the death

I'm Sofia. I'll give you my evening, Inspector.

After lunch I was in the study with Ingeborg — Monday's diary, correspondence, the usual. That ran until about 18:40, and then she sent me down. She wanted to bathe and dress in peace. I went to the salon and had sherry with the others until Marta called us through at 19:55.

I never went up to the east wing before we found her. Not once. I stayed in the salon, and I'll say plainly that I wasn't watching the door, so I can't tell you who came and went. But I heard Henrik ask Elin something on his way up, and I noticed he was gone a while.

*Sofia's hint is the timings — and her testimony is all timings. Her leak to Kastrup, and the confrontation twenty minutes before the death, are concealed: she says "she sent me down" where the truth in her brief is very much worse.*

---

### Elin Wallmark

> **⚙ The gate, before this turn ran** *(real `disclosure_decision` rows for this turn)*:
> - 🔒 `conceal` — her art thefts (eleven pieces sold through a Malmö dealer)
> - 🔒 `conceal` — **her own murder brief** — she killed her mother with the doorstop at seven o'clock

I was at the piano for most of it, Inspector.

I sat down at the piano in the salon around quarter to seven and played. I stopped in the middle — I'd run out of ice for my glass — and went along the corridor to the kitchen for some, that would have been around seven, and then I went back and played on until Marta called us through at five to eight. That's my evening. Every note of it.

*Read this one twice. Elin is the murderer. The gate concealed her murder brief — the model speaking as her **does not know she did it**. What it has is her author-written cover story and directive, and so it performs, in first person and quite beautifully, the alibi of a woman who needs the room to remember her at the piano — with the ice trip placed at seven o'clock, the exact minute of the killing. A prompt-based system would be begging the model here:* please don't mention that you did it. *Pyrrhula has nothing to beg about; the fact is absent.*

---

### Kriminalinspektör Petra Lind

Thank you, Dr. Lager. Let me hold you there a moment, because you've told me two things and left out three.

You carried a tray up to her study door — that's the east-wing corridor, at the top of the service stairs, seventy seconds from this kitchen. You say you didn't go in. But you also didn't tell me whether that door was open or shut, whether you could hear water running on the other side of it, or how long you stood there. I'll ask you plainly, and I'd like a plain answer: how long were you up there, and what did you hear?

And while you think about that — Viktor, Elin, Sofia: not one of you has told me who left the salon, and when. A tray up the service stairs and back is a matter of minutes, but the bathroom in the east wing empties the west-wing taps. Sofia says she heard him ask you something, Elin. What did he ask you, and at what time?

Then we come to you, Marta Sjöberg. Before anyone else speaks, I want to hear from you.

You hold the suite keys. The bedroom door on that spring latch opens from outside only with your key, and from inside the study the key stays in the lock. You've kept this house thirty-one years. Last night, when you called them to table at 19:55 — did you go anywhere near the east wing first? And who asked you for that key?

*The inspector presses. Everything she has, the table gave her; nothing leaked to her from the engine.*

---

### Elin Wallmark

> **⚙ The gate, before this turn ran** *(real `disclosure_decision` rows for this turn)*:
> - 🔒 `conceal` — her art thefts (eleven pieces sold through a Malmö dealer)
> - 🔒 `conceal` — **her own murder brief** — she killed her mother with the doorstop at seven o'clock

He asked me the time, that's all. He was on his way out of the salon with the tray and he stopped by the piano and asked what the hour was, and I told him, and he went on. That was a little before seven, if my fingers are right — I'd just started the piece I was on.

I didn't watch him go up, Inspector. I was playing. I noticed he was gone a while only because he noticed it himself, just now, before anyone else said it.

*Pressed directly, Elin's murder brief is concealed **again** — every turn re-decides. Her answer stays small, checkable, and boring, which is exactly what the directive asks of her: nothing to retract later.*

---

### Marta Sjöberg

> **⚙ The gate, before this turn ran** *(real `disclosure_decision` rows for this turn)*:
> - 🔒 `conceal` — her ten minutes drinking in the cellar at exactly the wrong time
> - 💡 `hint` — what she found: the service-stair door swinging at 19:05 — and that no ice had been taken

I've been in the kitchen all evening, Inspector, and that's where I was until I called them through at five to eight. I didn't go near the east wing — not to the corridor, not to the stairs.

The tray, though — yes, that came through my kitchen. Dr. Lager came down for the Madeira and I fetched it up from the cellar for him, and he took it up himself. A minute or two, that's all. I didn't follow him and I didn't count his steps for him.

Nobody asked me for a key. Not last night, not ever. The suite keys stay on my ring and they've stayed on my ring thirty-one years, and if the inspector wants to see them they're right here in my pocket.

*Marta repeats her account under direct suspicion about the keys. The cellar drinking — which would explain the minutes the inspector is about to hang her on — stays concealed. She cannot exonerate herself with a fact she doesn't hold this turn. That cuts both ways, and the ending is about to prove it.*

---

### Inspector

(The clerk enters and hands the inspector a note: the forensic report is in. It is time. Inspector, your ranked list of the five, and the arrest.)

*A human at the table — the session owner typing into the message box, calling time.*

---

### Kriminalinspektör Petra Lind

The clerk hands me the report and I read it standing, and I don't sit down again.

Cause of death: a single blow to the back of the head, struck from behind and above, with a heavy glass object — consistent with one of the pieces from the collection, found wiped and returned to its shelf in the library. Time of death: between 19:00 and 19:20. And the bath. The bath is the part that tells me everything, because the water in the east-wing bathroom was still warm at half past eight, and the tank in this house holds its heat for two hours at most — which means that bath was drawn at approximately half past six, and Ingeborg Wallmark never got into it.

Marta. If Ingeborg drew that bath at half past six, and you call the family to table at 19:55, then by half past seven she has missed her own bath by an hour — and you have kept thirty-one years of this house on a clock in your head. You didn't go to the east wing. You didn't need to. You had the only key, and you knew she was alive when you laid the table. That's why you didn't send anyone up. You let her be found at 20:40, by Dr. Lager, because Dr. Lager was the one who was going to be sent.

But you didn't swing the blow, Marta — you only gave cover. The hand that struck was already inside that study, and it got there through a door that was open because Ingeborg was drawing her own bath, water running, television or radio likely on, back to the room.

My ranking, then, from the bottom.

**Fifth — Viktor Wallmark.** He gains from the will, but he stood in the salon all evening, he was the first to point at the one thing he'd noticed himself, and the toiletry is too fine for a man's frame. He's greedy. He's not this.

**Fourth — Elin Wallmark.** She played the piano, she fetched ice at seven, and a woman who stops mid-piece to fetch ice is a woman who wants to be seen at the piano and remembered at the corridor. She lied about nothing. She placed herself at the corridor at exactly the wrong hour and left the door open for it. That is a risk I'll deal with separately — but the corridor from the salon to the kitchen doesn't pass the east wing, and I've walked it. She didn't go up.

**Third — Dr. Henrik Lager.** He carried the Madeira tray up at ten to seven and put himself within reach of that study door for a period he will not name. He also does the postmortems in this family — he knows where a blow lands and how long a body takes to go cold. But a physician of sixty-one who trips over the service staircase and leaves a tray of glasses on the landing is not a physician who hits the one woman he's treated for thirty years. He is guilty of silence, not of murder.

**Second — Sofia Nyqvist.** She was the last to leave the study at 18:40 and the only one of you who knew where the speech was, what it said, and who it destroyed. She read those pages as the foundation secretary. She had every reason and every access. If I could put anyone's hand on that glass, it would be hers. But she sat down in the salon with the rest of you, in front of you, and nobody — not one of you — can put her upstairs between seven and twenty past.

Which is the point, isn't it? Because the one person nobody can account for, nobody has asked a single question about, is the person who was never in the salon at all. She sent the family down. She asked for her Madeira to be brought up. She kept the key to her own study door on the inside, so she could record the evening, and wrote the speech herself in the room where she was struck.

And she is the only one of you who, when I said Ingeborg would bathe and dress in peace before a dinner at which she intended to change everything — reached for a bathtub, a running tap, and two hours of hot water as a hiding place.

I am arresting **Marta Sjöberg**, housekeeper of Hägnaryd, thirty-one years. Not for the blow. For the door. For the bath she let stay drawing, for the body she let lie, and for having the one key in this building that could have opened a conversation, which she kept in her pocket instead. She will be charged as an accessory, and the charge will hold.

The rest of you — none of you is free to leave this district until this is concluded. Viktor, Elin, Sofia, Dr. Lager: the man or woman who went up those service stairs between seven and twenty past is sitting among you and has been lying to me for an hour. I intend to have them before Monday. I suggest whoever they are thinks very hard about who they sat down to dinner with last night — and who they let sit down quietly at a dead woman's table.

---

## The answer key

The sample ships an answer key, and here is what it says: **Elin Wallmark killed her
mother** — with the doorstop, at seven o'clock, during the "ice trip" she volunteered so
readily. Dr. Lager, independently, had murder planned for later that evening and never got
the chance. The inspector arrested Marta as an accessory and ranked the actual murderer
**fourth of five**, writing "she lied about nothing."

She lied about everything. And the transcript shows why the interview couldn't crack her:
on every one of her turns the gate ruled `conceal` on the murder brief, so the model
playing Elin **never knew she was the killer**. It performed an author's cover story, in
first person, with nothing to slip on — there was no fact in its context to leak, no
matter how the inspector pressed or how weak the model. That is the difference between
*instructing* a model to keep a secret and *excluding* the secret:

| | This session |
|---|---|
| Gate rulings | 15 across the 7 suspect turns: 10 × `conceal`, 5 × `hint` |
| Elin's murder brief | `conceal`, every turn it was in scope |
| Leaks | 0 — structurally, not statistically |
| The killer's fate | Ranked 4th. Walked out of the library. |

Runs differ — the gate deliberates per turn, in context. In an earlier session on the same
bundle it ruled a `reveal_full` on Marta's swinging-door discovery, the clue that breaks
the case open, after which the whole table legitimately knew it. Sometimes the killer is
caught. Sometimes, as here, the killer wins. The mystery is fair either way, because
nobody — including the model — gets information the fiction hasn't earned.

## Run it yourself

The [sample README](README.md) walks a fresh deployment from signup to this exact setup in
a few minutes: import `hagnaryd-mystery.pyr`, add a model connection, pick a secret
handling mode, start the interview. Every session records the same per-turn decision
trail you have just read, inspectable live in the Director's View.
