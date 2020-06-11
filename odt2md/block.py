from dataclasses import dataclass, field, replace
from odt2md.util import ns
from typing import List
import lxmlx.event as ev
from uuid import uuid4
import regex


@dataclass
class ImageBlock:
    name: str
    href: str

@dataclass
class InlineImage:
    name: str
    href: str

@dataclass
class Span:
    styles: list
    text: str

@dataclass
class Footnote:
    id: str
    citation: str
    body: list = field(default_factory=list)

@dataclass
class FootnoteRef:
    styles: list
    id: str
    citation: str

@dataclass
class TextBlock:
    para_style: str
    spans: List[Span] = field(default_factory=list)
    footnotes: List[Footnote] = field(default_factory=list)


def parse_blocks(para):
    assert para.tag == ns.text('p'), para.tag
    para_style = para.attrib[ns.text('style-name')]
    yield from extract_spans(ev.scan(para), para_style)

_ignore = {ns.text('p'), ns.text('soft-page-break'), ns.text('toc-mark')}

def extract_spans(events, para_style):

    inline_styles = [para_style]

    block = TextBlock(para_style=para_style)
    text = []

    def flush():
        if text:
            block.spans.append(
                Span(styles=inline_styles[:], text=''.join(text))
            )
            text.clear()

    frameName = None
    for e,p in ev.with_peer(events):
        if e['type'] == ev.ENTER:
            if e['tag'] in _ignore:
                continue
            if e['tag'] == ns.text('span'):
                # flush text outside of span, if any
                flush()
                span_style = e['attrib'][ns.text('style-name')]
                inline_styles.append(span_style)
            elif e['tag'] == ns.text('line-break'):
                flush()
                if block.spans:
                    yield from normalize_block(block)
                block = TextBlock(para_style=para_style)
            elif e['tag'] in (ns.text('s'), ns.text('tab')):
                text.append(' ')
            elif e['tag'] == ns.text('note'):
                flush()
                fnote_id = generate_footnote_id()
                fnote = parse_footnote(fnote_id, ev.subtree(events))
                block.footnotes.append(fnote)
                block.spans.append(FootnoteRef(inline_styles[:], fnote_id, fnote.citation))
            elif e['tag'] == ns.drawing('frame'):
                frameName = e['attrib'].get(ns.drawing('name'))
            elif e['tag'] == ns.drawing('image'):
                flush()
                if block.spans:
                    yield from normalize_block(block)
                block = TextBlock(para_style=para_style)

                href = e['attrib'].get(ns.xlink('href'))
                yield ImageBlock(name=frameName, href=href)
            else:
                assert False, e['tag']
        elif e['type'] == ev.EXIT:
            if p['tag'] in _ignore or p['tag'] in (
                ns.text('line-break'), ns.text('s'), ns.text('tab'), ns.text('note')
            ):
                continue
            elif p['tag'] == ns.drawing('frame'):
                frameName = None
                continue
            elif p['tag'] == ns.drawing('image'):
                continue
            assert p['tag'] == ns.text('span'), p['tag']
            flush()
            inline_styles.pop()
        elif e['type'] == ev.TEXT:
            text.append(e['text'])

    flush()
    if block.spans:
        yield from normalize_block(block)

def parse_footnote(id_, events):
    xml = ev.unscan(
        [{'type': ev.ENTER, 'tag': 'FNOTE'}] +
        list(events) +
        [{'type': ev.EXIT}]
    )
    citation = xml.find('./' + ns.text('note-citation'))
    assert citation is not None

    fnote = Footnote(id=id_, citation=citation.text)

    body = xml.find('./' + ns.text('note-body'))
    assert body is not None

    for para in body.findall('./'+ns.text('p')):
        fnote.body.extend(parse_blocks(para))

    return fnote

def generate_footnote_id():
    return str(uuid4())


def normalize_spans(spans):
    if not spans:
        return []

    def norm_text(s):
        if type(s) is Span:
            return replace(s, text=regex.sub(r'\s+', ' ', s.text))
        else:
            return s

    # normalize inner whitespace
    spans = [norm_text(s) for s in spans]

    # remove any leading whitespace
    if spans[0].text.startswith(' '):
        spans[0] = replace(spans[0], text=spans[0].text.lstrip())

    # remove trailing whitespace
    if spans[-1].text.endswith(' '):
        spans[-1] = replace(spans[-1], text=spans[-1].text.rstrip())

    # remove empty spans
    spans = [s for s in spans if (type(s) is not Span) or s.text]

    prev = None
    for s in spans:
        if type(s) is not Span:
            prev = None
            yield s
        elif prev is not None:
            if prev.text.endswith(' ') and s.text.startswith(' '):
                yield replace(s, text=s.text.lstrip())
            else:
                yield s
        else:
            yield s

def normalize_block(block):
    block = replace(block, spans=list(normalize_spans(block.spans)))
    if block.spans:
        yield block

def merge_aliased_spans(spans, alias):

    spans = [s.replace(style=alias(s.style)) if type(s) is Span else s for s in spans]

    def merge(tomerge):
        return Span(style=tomerge[0].style, text=''.join(s.text for s in tomerge))

    tomerge = []
    for s in spans:
        if type(s) is not Span:
            if tomerge:
                yield merge(tomerge)
                tomerge.clear()
            yield s
        elif tomerge:
            if tomerge[-1].style != s.style:
                yield merge(tomerge)
                tomerge.clear()
            tomerge.append(s)
        else:
            tomerge.append(s)

    if tomerge:
        yield merge(tomerge)

def parse_odt(xml):
    body_text = xml.find('.//'+ns.office('body')+'/'+ns.office('text'))

    for para in body_text.findall('.//'+ns.text('p')):
        yield from parse_blocks(para)
