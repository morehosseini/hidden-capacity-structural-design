"""Build the reader-facing Supplementary Note S2 PDF from its Markdown source."""
from pathlib import Path
from html import escape
import argparse, re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, LongTable, TableStyle, KeepTogether, Spacer

ap=argparse.ArgumentParser()
ap.add_argument('--font-dir',default='/System/Library/Fonts/Supplemental',help='Directory containing Arial.ttf, Arial Bold.ttf and Arial Italic.ttf')
args=ap.parse_args()
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'methods/supplementary_note_S2_data_and_methods.md'
fonts=Path(args.font_dir)
for name,file in [('Arial','Arial.ttf'),('Arial-Bold','Arial Bold.ttf'),('Arial-Italic','Arial Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(fonts/file)))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial-Italic',boldItalic='Arial-Bold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='MainTitle',fontName='Arial-Bold',fontSize=15,leading=18,spaceAfter=6,textColor=colors.black))
styles.add(ParagraphStyle(name='Version',fontName='Arial',fontSize=9,leading=12,spaceAfter=10,textColor=colors.HexColor('#555555')))
styles.add(ParagraphStyle(name='Subhead',fontName='Arial-Bold',fontSize=11.5,leading=14,spaceBefore=10,spaceAfter=6,keepWithNext=True,textColor=colors.black))
styles.add(ParagraphStyle(name='Text',fontName='Arial',fontSize=9.5,leading=12.5,spaceAfter=7,textColor=colors.black))
styles.add(ParagraphStyle(name='TableTitle',fontName='Arial-Bold',fontSize=9.5,leading=12.5,spaceBefore=4,spaceAfter=4,keepWithNext=True,textColor=colors.black))
styles.add(ParagraphStyle(name='Cell',fontName='Arial',fontSize=8.5,leading=10.5,textColor=colors.black))
styles.add(ParagraphStyle(name='CellRight',parent=styles['Cell'],alignment=2))
styles.add(ParagraphStyle(name='CellHead',fontName='Arial-Bold',fontSize=8.5,leading=10.5,textColor=colors.black))

SUP=str.maketrans('⁻⁰¹²³⁴⁵⁶⁷⁸⁹','−0123456789')

def inline(t):
    t=escape(t,quote=False)
    t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
    t=re.sub(r'\*(.+?)\*',r'<i>\1</i>',t)
    # Arial has no superscript digits: set them as raised text
    return re.sub(r'[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+',lambda m:'<super>'+m.group(0).translate(SUP)+'</super>',t)

VERSION,DATE=re.search(r'^Version (\S+) · (.+)$',SRC.read_text(encoding='utf-8'),re.M).groups()

def footer(c,d):
    c.setTitle('Supplementary Note S2 — Data and methods details')
    c.setAuthor('Supplementary material')
    c.setFont('Arial',8);c.setFillColor(colors.HexColor('#555555'))
    c.drawString(54,30,f'Supplementary Note S2 | Version {VERSION} | {DATE}')
    c.drawRightString(558,30,str(d.page))

# column widths (points, 504 in total) and horizontal cell padding for each table
WIDTHS={'S2':[150,354],'S3':[150,62,62,230],'S4':[150,110,50,94,100],'S5':[150,112,58,60,64,60],
        'S6':[84,96,108,96,120],'S7':[54,70,55,40,55,40,55,40,55,40]}
PAD={'S7':3}

def table(lines,title):
    rows=[[cell.strip() for cell in l.strip().strip('|').split('|')] for l in lines]
    align=['r' if s.strip().endswith(':') else 'l' for s in rows[1]]
    body=[rows[0]]+rows[2:]
    tid=re.search(r'Table (S\d+)',title).group(1)
    widths=WIDTHS[tid]
    assert len(widths)==len(rows[0]) and sum(widths)==504, tid
    data=[[Paragraph(inline(c),styles['CellHead' if i==0 else ('CellRight' if align[j]=='r' else 'Cell')]) for j,c in enumerate(r)] for i,r in enumerate(body)]
    t=LongTable(data,colWidths=widths,repeatRows=1)
    pad=PAD.get(tid,6)
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEABOVE',(0,0),(-1,0),0.8,colors.black),
        ('LINEBELOW',(0,0),(-1,0),0.5,colors.black),('LINEBELOW',(0,-1),(-1,-1),0.8,colors.black),
        ('TOPPADDING',(0,0),(-1,-1),2.5),('BOTTOMPADDING',(0,0),(-1,-1),2.5),
        ('LEFTPADDING',(0,0),(-1,-1),pad),('RIGHTPADDING',(0,0),(-1,-1),pad)]))
    head=[Paragraph(inline(title),styles['TableTitle'])] if title else []
    return ([KeepTogether(head+[t])] if len(body)<10 else head+[t])+[Spacer(1,7)]

story=[];pending_title=None;tbl=[]
for line in SRC.read_text(encoding='utf-8').splitlines()+['']:
    if line.startswith('|'):
        tbl.append(line);continue
    if tbl:
        story+=table(tbl,pending_title);tbl=[];pending_title=None
    if not line.strip():
        continue
    if line.startswith('# '):
        story.append(Paragraph(inline(line[2:]),styles['MainTitle']))
    elif line.startswith('## '):
        story.append(Paragraph(inline(line[3:]),styles['Subhead']))
    elif line.startswith('Version '):
        story.append(Paragraph(inline(line),styles['Version']))
    elif re.fullmatch(r'\*\*Table S\d.*\*\*',line.strip()):
        pending_title=line.strip()
    else:
        story.append(Paragraph(inline(line),styles['Text']))

out=ROOT/'supplementary_methods.pdf'
SimpleDocTemplate(str(out),pagesize=letter,leftMargin=54,rightMargin=54,topMargin=54,bottomMargin=54).build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
