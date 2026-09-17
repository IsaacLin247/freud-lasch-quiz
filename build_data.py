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

def parse(path, author, pat):
    txt = open(path, encoding="utf-8").read()
    paras = [p.strip().replace("\n", " ") for p in txt.split("\n\n")]
    out = []
    for p in paras:
        m = re.match(pat, p)
        if m:
            n = int(m.group(1))
            out.append({"id": f"{author}-{n}", "author": author, "num": n,
                        "text": m.group(2).strip(), "tell": TELLS[author][n]})
    return out

cards = parse("freud.txt", "freud", r"^(\d+)[.,]\s+(.*)$") + parse("lasch.txt", "lasch", r"^(\d+)\)\s+(.*)$")
assert len(cards) == 28, len(cards)
with open("docs/data.js", "w", encoding="utf-8") as f:
    f.write("// Generated by build_data.py from freud.txt and lasch.txt\n")
    f.write("window.CARDS = " + json.dumps(cards, ensure_ascii=False, indent=1) + ";\n")
print(len(cards), "cards written")
