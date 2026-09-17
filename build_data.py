"""Parse freud.txt / lasch.txt into docs/data.js for the quiz site."""
import json, re

TELLS = {
 "freud": {
  1: "Opens by defining religion as a set of dogmas that demand credence. Clinical, classifying tone: 'psychological significance of religious ideas.'",
  2: "The Konstanz/Bodensee and Acropolis anecdote. Freud's personal travel memories used as an example of verifiable dogma.",
  3: "School dogmas can be checked: earth is a globe, Foucault's pendulum, circumnavigation. The 'way to personal conviction is still open.'",
  4: "The three answers for why religious dogmas deserve belief: ancestors believed, handed-down proofs, and it is forbidden to ask.",
  5: "The prohibition on questioning 'rouses our strongest suspicions.' Ancestors were ignorant; the writings are full of contradictions and interpolations.",
  6: "Attacks Credo quia absurdum. 'There is no appeal beyond reason.' What about people who lack the rare inner experience?",
  7: "The philosophy of 'As If' and fictions. Freud's child asking 'Is that a true story?' and turning away in disdain.",
  8: "The thesis: religious ideas are illusions, wish-fulfillments. Infantile helplessness, the father, divine providence, a moral world order, a future life.",
  9: "Defines 'illusion' vs. error vs. delusion. Aristotle's vermin, Columbus, the poor girl and the prince, the alchemists.",
  10: "Religious doctrines are all illusions, unprovable and irrefutable. 'Scientific work is our only way to the knowledge of external reality.' Intuition and trance give nothing.",
  11: "Answers the 'why should not I believe?' objection. 'Ignorance is ignorance.' Philosophers stretch the word 'God'; humble acquiescence is 'irreligious in the truest sense.'",
  12: "Closing: it would be 'very nice' if there were a God, a moral order, and a future life, but 'very odd that this is all just as we should wish it ourselves.'",
 },
 "lasch": {
  1: "Surveys 'commentary on the modern spiritual plight' (Freud, Jung, Weber). The life-cycle analogy: civilization moves from childhood faith to adult skepticism. Quotes Freud's 'men cannot remain children for ever.'",
  2: "The 'unexamined premise' that history is like individual growth. Educated classes envy naive faith but 'cannot trade places with the unenlightened masses.'",
  3: "Disillusionment as what sets the artist and intellectual apart. The 'bourgeois philistine' refuses the light; the intellectual 'looks straight into the light without blinking.'",
  4: "The 'quaint conceit' of playing off our disillusionment against ancestral innocence. History read either as 'a tragedy of lost illusions or as the progress of critical reason.'",
  5: "Short paragraph: the 'either/or' versions of the modernist myth are 'symbiotically dependent.' Disillusionment is the price of progress.",
  6: "Past vs. present as simplicity vs. sophistication. Key line: 'Disillusionment, we might say, is the characteristic form of modern pride.'",
  7: "Pride shows in both triumphal progress and nostalgia. 'Nostalgia and the idea of progress go hand in hand.'",
  8: "'Nostalgia... evokes the past only to bury it alive.' Both mourners and cheerleaders deny history's hold; 'the prevailing disbelief in ghosts.'",
  9: "The chief casualty is a proper understanding of religion, misread as 'security.' Cites Jung and Joseph Wood Krutch: medieval morality as 'an exact science,' the slide to 'moral nihilism.'",
  10: "Questions whether religion ever gave unambiguous answers. Carmina Burana: the universe ruled by Fortune, not Providence; enjoy life while you can.",
  11: "William James, The Varieties of Religious Experience. Faith 'always, in every age, arises out of a background of despair.' 'Radical evil,' 'yielding,' 'self-surrender.'",
  12: "'The modern world has no monopoly on the fear of death.' Alienation is normal; rebellion against God is natural. The Book of Job.",
  13: "Faith requires renouncing the belief that God's purposes match ours. Religion undermines 'the most important superstition of all': that humanity controls its destiny. 'Our prayers are answered only when we surrender that claim.'",
  14: "The religious critique of pride should speak to moderns. The 'central paradox': 'the secret of happiness lies in renouncing the right to be happy.'",
  15: "What makes the modern temper modern: rebellion against dependence is more pervasive. Flannery O'Connor; 'dark night of the soul'; science seems to sanction the rebellion.",
  16: "Machines and 'the illusion of mastery,' the one illusion that survives. The 'future of this illusion' is more in doubt than the future of religion.",
 },
}

# The most significant / most quotable sentences of each paragraph, verbatim.
KEYS = {
 "freud": {
  1: "religion consists of certain dogmas, assertions about facts and conditions of external (or internal) reality, which tell one something that one has not oneself discovered and which claim that one should give them credence.",
  2: "We hear there: Konstanz is on the Bodensee. A student song adds: If you don't believe it go and see. [...] I was already a man of mature years when I stood for the first time on the hill of the Athenian Acropolis, between the temple ruins, looking out on to the blue sea. A feeling of astonishment mingled with my pleasure, which prompted me to say: then it really is true, what we used to be taught at school!",
  3: "Since it is impracticable, as all concerned realize, to send every school child on a voyage round the world, one is content that the school teaching shall be taken on trust, but one knows that the way to personal conviction is still open.",
  4: "They deserve to be believed: firstly, because our primal ancestors already believed them; secondly, because we possess proofs, which have been handed down to us from this very period of antiquity; and thirdly, because it is forbidden to raise the question of their authenticity at all.",
  5: "Such a prohibition can surely have only one motive: that society knows very well the uncertain basis of the claim it makes for its religious doctrines. [...] The proofs they have bequeathed to us are deposited in writings that themselves bear every trace of being untrustworthy.",
  6: "Am I to be obliged to believe every absurdity? And if not, why just this one? There is no appeal beyond reason.",
  7: "It is to be expected that men will soon behave in like manner towards the religious fairy tales, despite the advocacy of the philosophy of \"As If.\" [...] We must ask where the inherent strength of these doctrines lies and to what circumstance they owe their efficacy, independent, as it is, of the acknowledgement of the reason.",
  8: "they are illusions, fulfillments of the oldest, strongest and most insistent wishes of mankind; the secret of their strength is the strength of these wishes. We know already that the terrifying effect of infantile helplessness aroused the need for protection - protection through love - which the father relieved",
  9: "Thus we call a belief an illusion when wish-fulfillment is a prominent factor in its motivation, while disregarding its relations to reality, just as the illusion itself does.",
  10: "Of the reality value of most of them we cannot judge; just as they cannot be proved, neither can they be refuted. [...] scientific work is our only way to the knowledge of external reality.",
  11: "Ignorance is ignorance; no right to believe anything is derived from it. No reasonable man will behave so frivolously in other matters or rest content with such feeble grounds for his opinions or for the attitude he adopts; it is only in the highest and holiest things that he allows this.",
  12: "it would indeed be very nice if there were a God, who was both creator of the world and a benevolent providence, if there were a moral world order and a future life, but at the same time it is very odd that this is all just as we should wish it ourselves.",
 },
 "lasch": {
  1: "In this analogy, civilization has passed through distinct phases, moving from a childhood of naive faith to the detached skepticism of an adult.",
  2: "Once the critical habit of mind has been fully assimilated, no one who understands its implications can find any refuge or resting place in premodern systems of thought and belief.",
  3: "The intellectual alone looks straight into the light without blinking. Disillusioned but undaunted: Such is the self-image of modernity, so proud of its intellectual emancipation that it makes no effort to conceal the spiritual price that has to be paid.",
  4: "It betrays a predisposition to read history either as a tragedy of lost illusions or as the progress of critical reason.",
  5: "It is the progress of critical reason that allegedly leads to lost illusions; disillusionment represents the price of progress.",
  6: "Disillusionment, we might say, is the characteristic form of modern pride.",
  7: "Nostalgia and the idea of progress go hand in hand. The assumption that our civilization has achieved a level of unparalleled complexity naturally gives rise to a yearning for bygone simplicity.",
  8: "Nostalgia is superficially loving in its re-creation of the past; but it evokes the past only to bury it alive. [...] Both are governed in their attitude toward the past, by the prevailing disbelief in ghosts.",
  9: "religion is consistently treated as a source of intellectual and emotional security, rather than as a challenge to complacency and pride. Its ethical teachings are misconstrued as a body of simple commandments leaving no room for ambiguity or doubt.",
  10: "What has to be questioned here is the assumption that religion ever provided a set of comprehensive and unambiguous answers to ethical questions, answers completely resistant to skepticism; or that it forestalled speculation about the meaning and purpose of life; or that religious people in the past were unacquainted with existential despair.",
  11: "the deepest variety of religious faith always, in every age, arises out of a background of despair. Religious faith asserts the goodness of being in the face of suffering and evil.",
  12: "The modern world has no monopoly on the fear of death or alienation from God. Alienation is the normal condition of human existence. Rebellion against God is the natural reaction to the discovery that the world was not made for our personal convenience.",
  13: "But the naive belief that our wishes govern the universe is precisely what religion attacks. We have no special claim on the universe, and our prayers are answered only when we surrender that claim.",
  14: "they cannot see the central paradox of religious faith: that the secret of happiness lies in renouncing the right to be happy.",
  15: "What makes the modern temper modern, then, is not that we have lost our childish sense of dependence but that the normal rebellion against dependence is more pervasive today than it used to be.",
  16: "In an age that fancies itself as disillusioned, this is the one illusion -- the illusion of mastery -- that remains as tenacious as ever.",
 },
}

# What the author argues in the paragraph, what the other author thinks about the same point,
# and whether the two converge ("converge"), diverge ("diverge"), or do both ("mixed").
ARGS = {
 "freud": {
  1: ("Freud classifies religion as dogma: claims about reality that you did not discover yourself and are asked to accept on authority. By treating religion as a set of propositions, he makes it something that can be tested like any other claim.",
      "Lasch thinks this framing is itself the modern mistake. Religion is not primarily a set of answers but 'a challenge to complacency and pride' (L¶9), and he denies it ever offered 'comprehensive and unambiguous answers' (L¶10). They diverge at the very definition.", "diverge"),
  2: ("Beliefs taken on authority are shallow until you verify them yourself. Freud's astonishment on the Acropolis shows how thin his school-taught belief had been; real conviction comes from 'go and see.'",
      "Lasch does not dispute this for geography. His objection is scope: the questions religion addresses (death, evil, dependence) are not the 'go and see' kind, and every generation faces them fresh (L¶12). They converge on how to check facts and diverge on whether religion is about facts.", "mixed"),
  3: ("Legitimate dogmas earn belief by resting on observation and reasoning, letting you retrace the process yourself, and naming their source. This sets up the test that religion will fail in paragraph 4.",
      "Lasch accepts that the 'critical habit of mind,' once learned, cannot be unlearned (L¶2), so both prize critical inquiry. But he holds that religion's knowledge is knowledge of human limits (L¶13), which no experiment can supply. Partial convergence on method, divergence on what counts as knowledge.", "mixed"),
  4: ("Religion offers three credentials, ancestral belief, ancient proofs, and a ban on questioning, and they contradict each other. If the proofs were real, the ban would be unnecessary.",
      "Lasch denies that religion ever rested on a ban on questioning: Job, the Carmina Burana, and William James's converts show doubt living inside the tradition (L¶10–12). He would agree that mere appeal to tradition is weak, since he distrusts nostalgia too (L¶7–8). Mostly divergent.", "diverge"),
  5: ("The taboo on questioning betrays that society knows its religious claims are shaky. Our ancestors were more ignorant than we are, and the scriptures they left are full of contradictions and revisions.",
      "This is the premise Lasch attacks head-on. Treating ancestors as ignorant children is the 'unexamined premise' of the life-cycle myth (L¶2) and 'the characteristic form of modern pride' (L¶6). Sharp divergence.", "diverge"),
  6: ("'I believe because it is absurd' is no argument. Reason is the final court, and a rare inner experience cannot obligate the many people who never have it.",
      "Lasch, following James, treats exactly that inner experience (despair turning into 'yielding' and 'self-surrender') as the deepest form of faith (L¶11). He does not claim it binds others, but he takes it as evidence about what faith is. They diverge on whether experience counts as knowledge.", "diverge"),
  7: ("The 'As If' defence (religion as a useful fiction) satisfies only philosophers. Ordinary people want to know whether a story is true, and Freud predicts they will soon treat religious stories like fairy tales. The real puzzle is why religion has been so powerful despite weak credentials.",
      "Lasch answers the prediction directly: sixty years on, religion's future looks more secure than the illusion of mastery (L¶16). And Freud's clear-eyed child is the very self-image Lasch mocks, the intellectual who 'looks straight into the light without blinking' (L¶3). Divergent.", "diverge"),
  8: ("The thesis. Religious ideas are illusions, fulfilments of humanity's oldest wishes. The helpless infant needs a protecting father; the adult, still helpless, projects a more powerful father onto the universe as providence, moral order, and afterlife.",
      "Lasch's paragraph 13 is the direct reversal: 'the naive belief that our wishes govern the universe is precisely what religion attacks.' Yet both start from the same fact of lifelong dependence (L¶13–14). Same premise, opposite conclusion about what religion does with it.", "mixed"),
  9: ("An illusion is defined by its motivation, not its truth. It is a belief in which wish plays a prominent part; it may even turn out true (the alchemists), unlike an error or a delusion.",
      "Lasch adopts this very tool and turns it on modernity: the 'comfortable belief' faith must renounce (L¶13) and 'the illusion of mastery' (L¶16) are wish-driven beliefs in Freud's exact sense. They converge on the method and diverge only on the target.", "converge"),
 10: ("Religious doctrines cannot be proved or refuted, but that opens no door for faith: science is the only road to knowledge, intuition and trance tell us nothing, and picking the doctrines you like is irresponsible.",
      "Lasch agrees that religion must be taken at full strength or not at all (L¶9, L¶13). But he sees scientific control over nature as the sponsor of modernity's real illusion (L¶15–16), and holds that knowledge of our limits is the most important knowledge there is. Convergence on 'no cafeteria religion,' divergence on science.", "mixed"),
 11: ("'You cannot disprove it, so why not believe' is facile; ignorance grants no right to believe. Redefining God as an abstraction is dishonest. Real religion is the search for a remedy against human insignificance; simply accepting insignificance is irreligious.",
      "Lasch shares the contempt for watered-down religion (L¶9). But he inverts the last claim: humble acceptance, 'yielding' and 'self-surrender,' is the heart of faith (L¶11, L¶13). They describe the same moment and give it opposite names. This is the most instructive contrast in the readings.", "mixed"),
 12: ("Conclusion. Psychologically, religious doctrines are illusions. It would be very nice if there were a God, a moral order, and an afterlife, but it is suspicious that reality matches our wishes so exactly, and unlikely that ignorant ancestors solved the deepest riddles.",
      "Lasch denies both halves. Faith is not what we would wish; it demands 'renouncing the right to be happy' (L¶14). And the ancestors were not naive: they knew despair, Fortune, and Job's problem (L¶10, L¶12). Divergent.", "diverge"),
 },
 "lasch": {
  1: ("Lasch surveys the commentary on the modern spiritual plight (Freud, Jung, Weber) and finds one shared image: history as a life cycle from childhood faith to adult skepticism, so religion is something humanity outgrows.",
      "Freud is the paradigm case. He calls our ancestors 'poor, ignorant, enslaved' (F¶12), says they 'believed in things we could not possibly accept today' (F¶5), and expects people to outgrow 'religious fairy tales' (F¶7). Freud holds sincerely what Lasch is describing critically.", "diverge"),
  2: ("The growth metaphor is an 'unexamined premise' that lets moderns dismiss all tradition as clinging to childhood. The educated may envy naive faith, but they cannot return to it once the critical habit of mind is learned.",
      "Freud agrees the critical habit is irreversible and thinks that is good: 'no one can be forced into unbelief,' but 'ignorance is ignorance' (F¶11). They converge on the irreversibility of criticism and diverge on whether the premise behind it has been examined.", "mixed"),
  3: ("Disillusionment has become the badge of the artist and intellectual, who alone 'looks straight into the light without blinking.' This heroic self-image is modernity's picture of itself.",
      "Freud embodies the self-image without irony: his child who asks 'Is that a true story?' and turns away in disdain (F¶7), and the 'reasonable man' who refuses feeble grounds for belief (F¶11). What Lasch calls a pose, Freud calls honesty.", "diverge"),
  4: ("The conceit of playing our disillusionment against ancestral innocence is not harmless. It forces history into two shapes: a tragedy of lost illusions or the progress of critical reason.",
      "Freud reads history in the second shape throughout: knowledge advances from school dogma to personal verification (F¶3), ancestors were more ignorant (F¶5), science slowly reveals the riddles (F¶10). Divergent.", "diverge"),
  5: ("The two shapes are one myth. It is the progress of critical reason that supposedly costs us our illusions; disillusionment is the price of progress.",
      "Freud accepts that price knowingly: 'it would indeed be very nice if there were a God,' but honesty forbids the comfort (F¶12). They converge on the description (progress costs illusions) and diverge on whether that story is true.", "mixed"),
  6: ("Past and present are divided by simplicity versus sophistication, with disillusionment as the impassable barrier. Naming the vice: disillusionment is 'the characteristic form of modern pride.'",
      "Freud would reject the word pride. For him disillusionment is plain honesty: 'do not deceive yourself' (F¶11). Where Lasch sees a spiritual fault, Freud sees the refusal of a spiritual fault, self-deception. Divergent.", "diverge"),
  7: ("Modern pride appears not only in triumphal progress but in nostalgia. Believing our civilization uniquely complex naturally produces a yearning for bygone simplicity.",
      "Freud has no nostalgia, but he does hold the other half, the assumption of unparalleled modern knowledge ('everything we have laboriously discovered about the reality of the world,' F¶10). Lasch's point applies to Freud's progressivism, not to any wistfulness. Partial.", "mixed"),
  8: ("Nostalgia buries the past alive. Mourners and celebrants of the past both assume we have outgrown childhood and both deny that history still haunts the present: 'the prevailing disbelief in ghosts.'",
      "Freud openly denies the past's authority (F¶5). Yet his own theory says the conflicts of childhood 'are never wholly overcome' (F¶8), which is a kind of belief in ghosts. Lasch's point that the past haunts the present is, oddly, something Freud's psychology supports even as his history denies it.", "mixed"),
  9: ("The chief casualty of the modern myth is a misreading of religion as security and simple commandments (Jung, Krutch), with doubt as the first step toward nihilism.",
      "Freud's paragraph 8 is the textbook case of the reading Lasch rejects: providence 'allays our anxiety,' a moral order guarantees justice, an afterlife supplies the setting. For Freud, security is what religion is for; for Lasch, that is the caricature. Divergent.", "diverge"),
 10: ("Religion never provided doubt-proof answers, and religious people of the past knew existential despair. The Carmina Burana, written by future priests, sing that Fortune rules and life has no higher purpose.",
      "Freud pictures the past as a time when questioning religion 'was visited with the very severest penalties' (F¶4) and believers were 'enslaved' (F¶12). Lasch's historical evidence is aimed squarely at that picture. Divergent on the facts of history.", "diverge"),
 11: ("Following William James, the deepest faith in every age arises from despair. Faith asserts the goodness of being in the face of evil; awareness of radical evil precedes the surrender that brings peace.",
      "Freud grants that religion responds to human suffering and insignificance (F¶8, F¶11), so they converge on the starting point. But he says private experience proves nothing to others (F¶6) and that acquiescing in insignificance is 'irreligious' (F¶11), the reverse of Lasch's 'self-surrender.'", "mixed"),
 12: ("Alienation from God is the normal human condition, not a modern one. Rebellion is the natural reaction to learning the world was not made for us, and Job already faced the suffering of the just.",
      "Freud agrees with the fact: the world does not meet our wishes, and justice has 'so often remained unfulfilled' (F¶8). They converge on the diagnosis of the human situation and diverge on the response: Freud says religion invents a father to fix it, Lasch says faith accepts it.", "mixed"),
 13: ("The central reversal. Faith requires renouncing the belief that God's purposes coincide with ours. Religion attacks the wish that our prayers govern the universe; prayers are answered only when that claim is surrendered.",
      "This is the direct answer to Freud's thesis that religion fulfils the wish for a protecting father (F¶8); 'father figure who answers all our prayers' paraphrases Freud. Yet both are suspicious of wish-driven belief (F¶9, F¶12). Divergent about religion, convergent about wish.", "diverge"),
 14: ("The religious critique of pride should speak to moderns, but they cannot imagine a God indifferent to human happiness, so they miss the paradox: the secret of happiness lies in renouncing the right to be happy.",
      "Freud assumes religion promises happiness: 'it would indeed be very nice if there were a God... a benevolent providence... a future life' (F¶12). Lasch's paradox says genuine faith promises the opposite. Divergent.", "diverge"),
 15: ("What is modern is not lost dependence but a more pervasive rebellion against it. O'Connor shows the rebellion is old; what is new is that science seems to sanction it.",
      "Freud agrees dependence is lifelong: 'this helplessness would continue through the whole of life' (F¶8). But his remedy, growing out of the clinging with science's help (F¶10), is exactly what Lasch names rebellion against dependence. Convergent on the condition, divergent on the cure.", "mixed"),
 16: ("Science's machines let us imagine ourselves masters of our fate. The illusion of mastery is the one that survives, and its future is more in doubt than religion's.",
      "Freud predicted religion's decline (F¶7) and made science the only path to knowledge (F¶10). Lasch turns Freud's title against him. Ironically, Freud's own example of an illusion that might come true is the alchemists' dream fulfilled by chemistry (F¶9), a small concession that science can serve a wish. Divergent.", "diverge"),
 },
}

def parse(path, author, pat):
    txt = open(path, encoding="utf-8").read()
    paras = [p.strip().replace("\n", " ") for p in txt.split("\n\n")]
    out = []
    for p in paras:
        m = re.match(pat, p)
        if m:
            n = int(m.group(1))
            out.append({"id": f"{author}-{n}", "author": author, "num": n,
                        "text": m.group(2).strip(), "key": KEYS[author][n], "tell": TELLS[author][n],
                        "argument": ARGS[author][n][0], "other": ARGS[author][n][1], "stance": ARGS[author][n][2]})
    return out

cards = parse("freud.txt", "freud", r"^(\d+)[.,]\s+(.*)$") + parse("lasch.txt", "lasch", r"^(\d+)\)\s+(.*)$")
assert len(cards) == 28, len(cards)
with open("docs/data.js", "w", encoding="utf-8") as f:
    f.write("// Generated by build_data.py from freud.txt and lasch.txt\n")
    f.write("window.CARDS = " + json.dumps(cards, ensure_ascii=False, indent=1) + ";\n")
print(len(cards), "cards written")
