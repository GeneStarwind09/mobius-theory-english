# Context and translation notes

**Full-story spoilers follow.**

## Sources and scope

The primary context source was the installed game's own six subtitle files and its Unity story, branch, evidence, interaction, ending and minigame configuration files. The official [Steam listing](https://store.steampowered.com/app/1925830/MOBIUS_THEORY/) establishes the premise: a romantic mystery about reporter Li Weishi, his fiancée Zhao Yidie, an apparently contradictory account of his break-up with Lin Jianhe, and an abandoned time-travel experiment. This is the 2022 game from 乐谷游戏, not the unrelated 2025 television drama *Mobius*.

The installed build has five chapters, with Chapter 4 split across two videos. Its extra video files have no shipped SRT companions. The patch translates the supplied subtitle corpus; it does not claim a fresh audio transcription of every video or a frame-by-frame translation of on-screen props.

## Characters and terminology

| Chinese | English | Context |
|---|---|---|
| 李未时 | Li Weishi | Reporter and player character. Weishi in familiar dialogue. |
| 赵倚蝶 / 赵依蝶 | Zhao Yidie | Weishi's fiancée in the initial timeline. The second spelling occurs as a source inconsistency. |
| 小蝶 | Xiaodie | Yidie's affectionate nickname, retained consistently. |
| 林见鹤 | Lin Jianhe | Weishi's first love, a TV presenter. Jianhe in familiar dialogue. |
| 鹤姐 | Jianhe | Affectionate/respectful address, rendered by name rather than the literal “Sister Crane”. |
| 徐言 | Xu Yan | Weishi's colleague, central to the hidden chronology. |
| 徐哥 | Xu | Familiar respectful address for Xu Yan; no biological brother implied. |
| 景宇彬教授 | Professor Jing Yubin / Professor Jing | Associated with the time-machine research. |
| 高时宇 / 高先生 | Gao Shiyu / Mr Gao | Shiwo Group chairman, linked to arranging Jianhe's care. |
| 时涡集团 | Shiwo Group | Organisation name retained in pinyin; no official English name found. |
| 美康疗养院 | Meikang Care Home | Yidie's workplace and the institution caring for Jianhe. |
| 怀表 | pocket watch | Essential time-travel device; not confused with the separate digital wristwatch clue. |
| 时间线 | timeline | A particular sequence of consequences. |
| 轮回 | loop | Recurrence produced by the game's time travel; avoids suggesting religious reincarnation without textual grounds. |
| 宿命 | fate | The apparently unavoidable outcome; distinguished from the mechanism of a loop. |
| 特斯拉 / 费城实验 | Tesla / Philadelphia Experiment | Elements of the game's fictional scientific/conspiracy premise. |

Names retain Chinese family-name-first order. English uses a contemporary conversational register, with restrained swearing where the source warrants it. “Wife”, “fiancée”, “girlfriend” and “ex” follow the timeline of the scene; a seemingly wrong relationship can be an intended clue rather than an error.

## Story interpretation

In the starting present, Weishi plans to marry Yidie. Discovering Jianhe's disability brings conflicting versions of their earlier break-up into view. His investigation leads to the laboratory and time travel to Valentine's Day, 14 February 2019. Changing that day changes both his relationships and who suffers the accident. The same car and the 25-minute interval connect the apparently separate collisions.

Xu presents himself as a helper, but the final chapter reveals his prior relationship with Yidie, his connection to Jianhe, and his willingness to make others bear the cost of his desired future. Multiple temporal versions of Xu appear together: “two days ahead” and “three days ahead” are deliberately distinct. The pocket watch in the locked room, Xu's access to Weishi's home, and the Gao interview support that reveal. The translation preserves these clues without naming the culprit earlier than the source does.

The principal branches explore choosing Jianhe, choosing Yidie, trying to maintain incompatible relationships across time, and sacrificing Weishi's own continuity to save both women. The fourth ending's question about whether the traveller survives his past self's death remains uncertain in the English, as in the source. The final “short-sighted” exchange retains both the literal eyesight remark and its figurative sting.

## Motifs and adaptation decisions

Jianhe's name contains 鹤, “crane”, and Yidie's contains 蝶, “butterfly”. These motifs recur in scene and ending titles, so the translation retains them: **The Lone Butterfly's Dance**, **The Wounded Crane's Cry**, **Fallen Wings**, and **The Price of Defying Fate**. The USB clues use the same ending names consistently. The Lovers in Death ending alludes to the Butterfly Lovers in Chinese; the English title conveys the tragic shared death without adding an explanatory subtitle.

The green-plant remark is a joke about the Chinese association between “wearing a green hat” and being cheated on. Its evidence text makes that association explicit rather than leaving an unintelligible literal line. The porcelain-deer/router pun is adapted to “deer-coration”. The album's “dog food” slang becomes a joke about excessive displays of romance. References and dialogue are localised without adding spoilers or changing puzzle values.

Some scene titles allude to classical poetry. “A Fan in Autumn” retains the image of love discarded when its season passes. “This Lantern Festival” retains the festival reference and the contrast with a remembered meeting.

## Subtitle treatment

Every original cue is accounted for in `Translation-Review.csv`. Chapter 5 cues 30 and 31 contain the same bathroom line, with cue 30 lasting only 20 milliseconds. They become one English cue covering their combined interval. Other cue start times remain unchanged. End times may be extended into available silence by up to 500 milliseconds for readability; no cue is extended past the next cue's start.

Lines are wrapped to 42 characters, with at most two lines per cue. The computed maximum reading rate is at most 25 characters per second. This mechanical check supports readability but does not replace watching the subtitles against the performances. A whole-game audiovisual and branch playthrough is still needed before calling the release publication-ready.
