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

def parse(path, author, pat):
    txt = open(path, encoding="utf-8").read()
    paras = [p.strip().replace("\n", " ") for p in txt.split("\n\n")]
    out = []
    for p in paras:
        m = re.match(pat, p)
        if m:
            n = int(m.group(1))
            out.append({"id": f"{author}-{n}", "author": author, "num": n,
                        "text": m.group(2).strip(), "key": KEYS[author][n], "tell": TELLS[author][n]})
    return out

cards = parse("freud.txt", "freud", r"^(\d+)[.,]\s+(.*)$") + parse("lasch.txt", "lasch", r"^(\d+)\)\s+(.*)$")
assert len(cards) == 28, len(cards)
with open("docs/data.js", "w", encoding="utf-8") as f:
    f.write("// Generated by build_data.py from freud.txt and lasch.txt\n")
    f.write("window.CARDS = " + json.dumps(cards, ensure_ascii=False, indent=1) + ";\n")
print(len(cards), "cards written")
