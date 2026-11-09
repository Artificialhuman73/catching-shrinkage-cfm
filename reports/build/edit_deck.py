"""Adds the 'why' explanations to the project deck: example captions, a mechanism slide, and a takeaway conclusion."""
import copy
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

src, out = sys.argv[1], sys.argv[2]
NUM = {}
p = Presentation(src)
S = list(p.slides)
s7, s8, s10, s12 = S[6], S[7], S[9], S[11]
NUM.update({id(s7): 7, id(s8): 8, id(s10): 10, id(s12): 12})
NAMES = {(7, 4): "Text 2", (7, 6): "Shape 3", (7, 7): "Text 4", (7, 8): "Text 5", (7, 9): "Text 6", (8, 5): "Text 2", (8, 6): "Text 3",
         (8, 25): "Slide Number Placeholder 0", (10, 5): "Text 2", (10, 6): "Shape 3", (12, 2): "Text 0", (12, 5): "Text 3", (12, 9): "Text 8"}


def by_id(s, i):
    """Shape lookup by name: shape ids repeat on some slides (a table shares id 8 with a text box)."""
    return next(sh for sh in s.shapes if sh.name == NAMES[(NUM[id(s)], i)])

# Style templates taken from existing shapes
BOX_TEAL = by_id(s7, 6)._element    # light teal rounded box
BOX_PINK = by_id(s10, 6)._element   # light pink rounded box
HEAD = by_id(s7, 7)._element        # 19pt bold accent heading
BODY = by_id(s7, 8)._element        # 15pt body text
BULLETS = by_id(s8, 6)._element     # 15pt bulleted list
NOTE = by_id(s7, 9)._element        # small italic footnote
SLDNUM = by_id(s8, 25)._element
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def next_id(slide):
    return max(sh.shape_id for sh in slide.shapes) + 1


def place(slide, tmpl, x, y, w, h, name):
    el = copy.deepcopy(tmpl)
    el.find(".//{*}cNvPr").set("id", str(next_id(slide)))
    el.find(".//{*}cNvPr").set("name", name)
    off, ext = el.find(f".//{A}off"), el.find(f".//{A}ext")
    off.set("x", str(int(Inches(x)))); off.set("y", str(int(Inches(y))))
    ext.set("cx", str(int(Inches(w)))); ext.set("cy", str(int(Inches(h))))
    slide.shapes._spTree.append(el)
    return slide.shapes[-1]


def set_paras(shape, paras):
    """Replace text, one paragraph per item, keeping the first paragraph's formatting.
    An item may be a string or a list of (text, bold) runs."""
    txb = shape._element.find(".//{*}txBody")
    ps = txb.findall(f"{A}p")
    proto = copy.deepcopy(ps[0])
    for q in ps:
        txb.remove(q)
    for item in paras:
        q = copy.deepcopy(proto)
        runs = q.findall(f"{A}r")
        for r in runs[1:]:
            q.remove(r)
        r0 = runs[0]
        q.remove(r0)
        end = q.find(f"{A}endParaRPr")
        for text, bold in ([(item, None)] if isinstance(item, str) else item):
            r = copy.deepcopy(r0)
            if bold is not None:
                r.find(f"{A}rPr").set("b", "1" if bold else "0")
            r.find(f"{A}t").text = text
            end.addprevious(r) if end is not None else q.append(r)
        txb.append(q)


def text(slide, tmpl, x, y, w, h, paras, name):
    sh = place(slide, tmpl, x, y, w, h, name)
    set_paras(sh, paras)
    return sh


# ---- Slide 7: make the big number concrete ----
set_paras(by_id(s7, 4), ["largest gap between CausalPFN's answer and the exactly expected one, over 40 datasets",
                         [("Example: an answer of 5.0 becomes exactly 50.0 when every outcome is multiplied by 10", True)]])
by_id(s7, 4).height = Inches(1.2)
set_paras(by_id(s7, 8), ["CausalPFN rescales each treatment group before the network sees it, so these changes are undone by "
                         "arithmetic, even when a group exceeds the 1,024-row context. The network never has to do anything, so "
                         "passing says nothing about whether it handles confounding. This is also why our round 1–3 test could not fail.",
                         [("What this means: ", True), ("auditing these models needs effects that vary from person to person, "
                                                        "like the planted self-test (Result 3).", False)]])

# ---- Slide 8: concrete 0%, and a 'why' box ----
set_paras(by_id(s8, 5), ["of runs more than 10% off at true effects of 4 and above, across all 4 simulators",
                         [("Example: with a true effect of 128, every answer fell between 126.6 and 129.4", True)]])
by_id(s8, 5).height = Inches(1.15)
b = by_id(s8, 6)
b.top, b.height = Inches(3.65), Inches(1.45)
set_paras(b, ["At effects of 1–2 it is 3–10% off, mostly away from zero: it corrects confounding only part of the way",
              [("Shrinkage hypothesis not supported on these simulators", True)]])
place(s8, BOX_TEAL, 8.15, 5.05, 4.7, 1.65, "Why box")
text(s8, HEAD, 8.35, 5.15, 4.3, 0.4, ["Why it cannot shrink"], "Why head")
text(s8, BODY, 8.35, 5.55, 4.35, 1.1, ["The network only sees rescaled numbers, so a big effect looks the same as a "
                                       "small one. The size is put back by arithmetic (next slide)."], "Why body")

# ---- New slide after 8: the mechanism ----
content = next(l for l in p.slide_layouts if l.name == "CONTENT")
ns = p.slides.add_slide(content)
ids = p.slides._sldIdLst
el = ids[-1]
ids.remove(el)
ids.insert(8, el)
ns.shapes.title.text if ns.shapes.title else None
title_ph = next(sh for sh in ns.placeholders)
title_ph.text = "Why CausalPFN cannot shrink a large effect"
text(ns, BODY, 0.6, 1.25, 12.1, 0.45,
     ["What CausalPFN does to one dataset, step by step (illustrative numbers, true effect 128)"], "Subtitle")

steps = [
    ("1  Raw data", "Treated people average 140, untreated average 12. The 128 gap is mostly the effect, plus some "
                    "confounding.", BOX_TEAL),
    ("2  Rescale each group", "Subtract each group's average and divide by its spread. Now every dataset looks "
                              "the same size, whether the effect is 1 or 128.", BOX_TEAL),
    ("3  Network corrects", "The transformer works only on these rescaled numbers and corrects for confounding. "
                            "This is the only learned step, so it is the only source of error.", BOX_PINK),
    ("4  Put the scale back", "Multiply by the spread and add each group's average back. The answer returns to "
                              "real units by plain arithmetic.", BOX_TEAL),
]
x, w, gap = 0.6, 2.75, 0.37
for k, (head, body, box) in enumerate(steps):
    xi = x + k * (w + gap)
    place(ns, box, xi, 1.9, w, 2.75, f"Step {k + 1} box")
    text(ns, HEAD, xi + 0.2, 2.05, w - 0.4, 0.45, [head], f"Step {k + 1} head")
    text(ns, BODY, xi + 0.2, 2.6, w - 0.35, 1.95, [body], f"Step {k + 1} body")
    if k < 3:
        arr = ns.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(xi + w + 0.05), Inches(3.05), Inches(gap - 0.1), Inches(0.4))
        arr.fill.solid(); arr.fill.fore_color.rgb = RGBColor(0x5A, 0x67, 0x73); arr.line.fill.background()
        arr.name = f"Arrow {k + 1}"

text(ns, HEAD, 0.6, 4.95, 6.0, 0.4, ["What this explains"], "Explains head")
text(ns, BULLETS, 0.6, 5.4, 6.0, 1.4,
     ["Large effects come out right (within 1.1% at 128): the network never sees the raw size, so it has nothing to pull toward zero",
      "Errors show up at small effects (3–10% at 1–2), where the leftover confounding is a bigger share of the answer"],
     "Explains body")
text(ns, HEAD, 6.95, 4.95, 5.8, 0.4, ["It also explains"], "Also head")
text(ns, BULLETS, 6.95, 5.4, 5.8, 1.4,
     ["Why the easy checks on Result 1 pass exactly: rescaling undoes them",
      "Why our round 1–3 test could not fail: a “no shrinkage” answer was built in"],
     "Also body")
text(ns, NOTE, 0.6, 6.85, 11.5, 0.4,
     ["Simplified from the per-group rescaling in causalpfn 0.1.5 (icl_model.py). Step 1 numbers are illustrative."], "Footnote")
num = copy.deepcopy(SLDNUM)
num.find(".//{*}cNvPr").set("id", str(next_id(ns)))
num.find(f".//{A}t").text = "9"
ns.shapes._spTree.append(num)

# ---- Slide 10 (now 11): what it means ----
by_id(s10, 5).height = Inches(1.05)
place(s10, BOX_TEAL, 0.6, 5.75, 6.2, 0.95, "Meaning box")
text(s10, BODY, 0.8, 5.85, 5.85, 0.8,
     [[("What this means: ", True), ("a detector is only as good as its reference. Most false alarms came from AIPW, "
                                     "not CausalPFN, so check the reference before blaming the model.", False)]], "Meaning")

# ---- Slide 12 (now 13): lead with the takeaway ----
t = by_id(s12, 2)
t.top, t.height = Inches(0.45), Inches(1.0)
sub = text(s12, BODY, 0.7, 1.55, 11.9, 1.3,
           ["CausalPFN does not shrink large effects: it rescales the data, so the effect's size never passes through "
            "the network. Its real weak spot is small effects, and the classic AIPW reference can be wrong too. We built "
            "tests that can tell these apart."], "Takeaway")
for r in sub._element.iter(f"{A}rPr"):
    r.set("sz", "1800")
    fill = r.find(f"{A}solidFill")
    fill.clear()
    fill.append(fill.makeelement(f"{A}srgbClr", {"val": "E6EDF3"}))
set_paras(by_id(s12, 5), ["Large effects are not shrunk: rescaling passes the size through",
                          "3–10% error at small effects, from partial adjustment",
                          "The AIPW reference caused most false alarms",
                          "Easy self-checks pass trivially and prove nothing"])
by_id(s12, 9).text_frame  # unchanged 'Next'

p.save(out)
print("saved", out)
