"""Build the reader-facing S1 PDF from the package's structured source files."""
from pathlib import Path
from html import escape
import argparse, json, re
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, LongTable, TableStyle, PageBreak, KeepTogether

ap=argparse.ArgumentParser()
ap.add_argument('--font-dir',default='/System/Library/Fonts/Supplemental',help='Directory containing Arial.ttf, Arial Bold.ttf and Arial Italic.ttf')
args=ap.parse_args()
ROOT=Path(__file__).resolve().parents[1]
fonts=Path(args.font_dir)
for name,file in [('Arial','Arial.ttf'),('Arial-Bold','Arial Bold.ttf'),('Arial-Italic','Arial Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(fonts/file)))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial-Italic',boldItalic='Arial-Bold')
rows=json.loads((ROOT/'literature/table_S1_extended_evidence.json').read_text())
VERSION,DATE=re.search(r'^Version (\S+) · (.+)$',(ROOT/'literature/table_S1_extended_evidence.md').read_text(encoding='utf-8'),re.M).groups()
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='MainTitle',fontName='Arial-Bold',fontSize=16,leading=19,spaceAfter=9,textColor=colors.black))
styles.add(ParagraphStyle(name='Subhead',fontName='Arial-Bold',fontSize=12,leading=15,spaceBefore=10,spaceAfter=7,keepWithNext=True,textColor=colors.black))
styles.add(ParagraphStyle(name='Text',fontName='Arial',fontSize=10,leading=13,spaceAfter=8,textColor=colors.black))
styles.add(ParagraphStyle(name='SmallText',fontName='Arial',fontSize=9,leading=12,spaceAfter=6,textColor=colors.black))
styles.add(ParagraphStyle(name='Cell',fontName='Arial',fontSize=9,leading=11.5,textColor=colors.black))
styles.add(ParagraphStyle(name='CellHead',fontName='Arial-Bold',fontSize=9,leading=11.5,textColor=colors.black))
styles.add(ParagraphStyle(name='SourceTitle',fontName='Arial-Bold',fontSize=10,leading=13,spaceBefore=8,spaceAfter=4,keepWithNext=True,textColor=colors.black))

def P(text,style='Text'):
    return Paragraph(escape(text),styles[style])

def footer(c,d):
    c.saveState()
    c.setTitle('Supplementary Table S1 — Extended comparison of structural utilisation and related design evidence')
    c.setAuthor('Supplementary literature comparison')
    c.setFont('Arial',8);c.setFillColor(colors.HexColor('#555555'))
    c.drawString(36,22,f'Supplementary Table S1 | Version {VERSION} | {DATE}')
    c.drawRightString(756,22,str(d.page))
    c.restoreState()

story=[P('Supplementary Table S1','MainTitle'),P('Extended comparison of structural utilisation and related design evidence','Subhead'),
    P(f'Version {VERSION} · {DATE}','SmallText'),
    P('This curated comparison accompanies Section 2.2 and Table 1 in the paper “Strength to Spare, Deflection at the Limit: Governing Utilisation in 1.4 Million Structural Member Calculations”. The 22 entries report different measures and may include related datasets; their samples and outcomes are not pooled. Appraisal or redesign results do not establish directly removable material. Study IDs link to the sources and provenance notes that follow.','SmallText'),
    P('GWP = global warming potential; LCA = life-cycle assessment; RC = reinforced concrete; PT = post-tensioned. Carbon scopes and comparison limits remain source-specific.','SmallText')]
groups=list(dict.fromkeys(r['evidence_group'] for r in rows))
for gi,g in enumerate(groups,1):
    panel_rows=[r for r in rows if r['evidence_group']==g]
    batches=[panel_rows[:5],panel_rows[5:]] if gi==2 else [panel_rows]
    for bi,batch in enumerate(batches):
        if gi>1 or bi>0:story.append(PageBreak())
        title=f'Panel {chr(64+gi)} — {g}'+(' (continued)' if bi else '')
        story.append(P(title,'Subhead'))
        data=[[P(t,'CellHead') for t in ['ID and study','Country and structure','Sample and measure','Relevant finding','Comparison limit']]]
        for r in batch:
            data.append([P(r['id']+' — '+r['study'],'Cell')]+[P(r[k],'Cell') for k in ['setting','sample_and_measure','finding','comparison_limit']])
        t=LongTable(data,colWidths=[110,115,157,160,178],repeatRows=1,splitByRow=True,hAlign='LEFT')
        t.setStyle(TableStyle([
       ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E7E6E6')),
       ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F7F7F7')]),
       ('GRID',(0,0),(-1,-1),0.45,colors.HexColor('#D9D9D9')),
       ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7),
       ('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
        story += [t,Spacer(1,8)]

story += [PageBreak(),P('Sources and provenance notes','MainTitle'),
    P('Evidence entries were reviewed on 26 October 2026, with bibliographic consistency updates on 28 October 2026. Access and verification limits are stated individually. These notes and the selection section form part of Table S1. Original sources should be cited when using their findings.','SmallText')]
for r in rows:
    block=[P(r['id']+' — '+r['study'],'SourceTitle'),P(r['reference'],'SmallText')]
    for url in r['source_locator'].split(' ; '):
        label=url.replace('https://doi.org/','DOI: ')
        if 'citeseerx' in url:label='Source: primary paper copy in CiteSeerX (Emirates Journal for Engineering Research, 2006)'
        if 'fwpa.com.au' in url:label='Source: FWPA report PDF, project PNA308-1213'
        if 'construction.cam.ac.uk' in url:label='Source: University of Cambridge dissertation abstract PDF'
        block.append(Paragraph('<link href="'+escape(url,quote=True)+'" color="#174A70">'+escape(label)+'</link>',styles['SmallText']))
    block += [P('Evidence access and verification: '+r['evidence_access_and_verification'],'SmallText'),
       P('Dataset relationship: '+r['dataset_overlap_note'],'SmallText'),
       P('Main Table 1: '+r['main_table']+'. Main Section 2.2 prose: '+r['main_prose']+'.','SmallText'),Spacer(1,5)]
    story.append(KeepTogether(block))

story += [PageBreak(),P('Search and selection note','MainTitle')]
selection=(ROOT/'literature/search_and_selection_note.md').read_text()
for block in selection.split('\n\n')[2:]:
    if block.startswith('## '):story.append(P(block[3:],'Subhead'))
    elif block.startswith('- '):
        for s in block.split('\n- '):story.append(P('• '+s.removeprefix('- '),'SmallText'))
    else:story.append(P(block.replace('`',''),'Text'))

output=ROOT/'supplementary_literature.pdf'
doc=SimpleDocTemplate(str(output),pagesize=landscape(letter),rightMargin=36,leftMargin=36,topMargin=32,bottomMargin=37,
    title='Supplementary Table S1 — Extended comparison of structural utilisation and related design evidence',
    author='Supplementary literature comparison')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(output)
