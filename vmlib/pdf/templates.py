from time import gmtime, strftime
import pathlib
from pkg_resources import resource_filename as resource
import pandas as pd
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.fonts import tt2ps
from reportlab.lib.colors import black
from reportlab.platypus import SimpleDocTemplate, Paragraph, \
                               Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, StyleSheet1, ListStyle
from reportlab.lib.units import cm
from reportlab.lib import utils, colors
from reportlab.rl_config import canvas_basefontname as _baseFontName
_baseFontNameB = tt2ps(_baseFontName, 1, 0)
_baseFontNameI = tt2ps(_baseFontName, 0, 1)
_baseFontNameBI = tt2ps(_baseFontName, 1, 1)


class Geo2x_a4():

    def __init__(self, outfile):
        self.outfile = outfile
        self.doc = SimpleDocTemplate(outfile,
                                     pagesize=A4,
                                     rightMargin=30,
                                     leftMargin=30,
                                     topMargin=30,
                                     bottomMargin=30,
                                     )
        self.flowables = []
        self.styles = self.styles()
        self.width, self.height = A4

    def create_text(self, text, style='Normal'):
        par = Paragraph(text, self.styles[style])
        self._add_flowable(par)

    def create_spacer(self, height=1):
        self._add_flowable(Spacer(1, height))

    def create_page_break(self):
        self._add_flowable(PageBreak())

    def _get_image(self, path, align='CENTER', width=14, height=6):
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        if width:
            return Image(path, width=width*cm, height=(width*aspect)*cm,
                         hAlign=align)
        elif height:
            return Image(path, width=(height/aspect)*cm, height=height*cm,
                         hAlign=align)

    def create_image(self, path, align='CENTER', width=14, height=6,
                     caption=False):
        im = self._get_image(path, align, width, height)
        self._add_flowable(im)
        if caption:
            self.create_text(caption, 'caption')

    def styles(self):
        styles = StyleSheet1()
        styles.add(ParagraphStyle(name='Normal',
                                  fontName=_baseFontName,
                                  fontSize=10,
                                  leading=12)
                   )
        styles.add(ParagraphStyle(name='BodyText',
                                  parent=styles['Normal'],
                                  spaceBefore=6)
                   )
        styles.add(ParagraphStyle(name='Italic',
                                  parent=styles['BodyText'],
                                  fontName=_baseFontNameI)
                   )
        styles.add(ParagraphStyle(name='caption',
                                  fontName=_baseFontNameI,
                                  alignment=TA_CENTER,
                                  fontSize=8,
                                  leading=12,
                                  spaceAfter=12)
                   )
        styles.add(ParagraphStyle(name='Heading1',
                                  parent=styles['Normal'],
                                  fontName=_baseFontNameB,
                                  fontSize=18,
                                  leading=22,
                                  spaceAfter=6),
                   alias='h1')
        styles.add(ParagraphStyle(name='Title',
                                  parent=styles['Normal'],
                                  fontName=_baseFontNameB,
                                  fontSize=22,
                                  alignment=TA_LEFT,
                                  textTransform='uppercase',
                                  spaceAfter=18),
                   alias='title')
        styles.add(ParagraphStyle(name='Subtitle',
                                  parent=styles['Normal'],
                                  fontName=_baseFontNameB,
                                  fontSize=18,
                                  leading=22,
                                  alignment=TA_LEFT,
                                  spaceAfter=12),
                   alias='subtitle')
        styles.add(ParagraphStyle(name='Heading2',
                                  parent=styles['Normal'],
                                  fontName=_baseFontNameB,
                                  fontSize=14,
                                  leading=18,
                                  spaceBefore=12,
                                  spaceAfter=6),
                   alias='h2')
        styles.add(ParagraphStyle(name='Heading3',
                                  parent=styles['Normal'],
                                  fontName=_baseFontNameBI,
                                  fontSize=12,
                                  leading=14,
                                  spaceBefore=12,
                                  spaceAfter=6),
                   alias='h3')
        styles.add(ParagraphStyle(name='Heading3_right',
                                  parent=styles['Normal'],
                                  fontName=_baseFontNameBI,
                                  fontSize=12,
                                  leading=14,
                                  alignment=TA_RIGHT,
                                  spaceBefore=12,
                                  spaceAfter=6),
                   alias='h3r')
        styles.add(ParagraphStyle(name='Bold_right',
                                  parent=styles['Normal'],
                                  fontName=_baseFontNameB,
                                  fontSize=12,
                                  leading=14,
                                  alignment=TA_RIGHT,
                                  spaceBefore=0,
                                  spaceAfter=2),
                   alias='br')
        styles.add(ParagraphStyle(name='Heading4',
                                  parent=styles['Normal'],
                                  fontName=_baseFontNameBI,
                                  fontSize=10,
                                  leading=12,
                                  spaceBefore=10,
                                  spaceAfter=4),
                   alias='h4')
        styles.add(ParagraphStyle(name='Heading5',
                                  parent=styles['Normal'],
                                  fontName=_baseFontNameB,
                                  fontSize=9,
                                  leading=10.8,
                                  spaceBefore=8,
                                  spaceAfter=4),
                   alias='h5')
        styles.add(ParagraphStyle(name='Heading6',
                                  parent=styles['Normal'],
                                  fontName=_baseFontNameB,
                                  fontSize=7,
                                  leading=8.4,
                                  spaceBefore=6,
                                  spaceAfter=2),
                   alias='h6')
        styles.add(ParagraphStyle(name='Bullet',
                                  parent=styles['Normal'],
                                  firstLineIndent=0,
                                  spaceBefore=3),
                   alias='bu')
        styles.add(ParagraphStyle(name='Definition',
                                  parent=styles['Normal'],
                                  firstLineIndent=0,
                                  leftIndent=36,
                                  bulletIndent=0,
                                  spaceBefore=6,
                                  bulletFontName=_baseFontNameBI),
                   alias='df')
        styles.add(ParagraphStyle(name='Code',
                                  parent=styles['Normal'],
                                  fontName='Courier',
                                  fontSize=8,
                                  leading=8.8,
                                  firstLineIndent=0,
                                  leftIndent=36,
                                  hyphenationLang=''))
        styles.add(ListStyle(name='UnorderedList',
                             parent=None,
                             leftIndent=18,
                             rightIndent=0,
                             bulletAlign='left',
                             bulletType='1',
                             bulletColor=black,
                             bulletFontName='Helvetica',
                             bulletFontSize=12,
                             bulletOffsetY=0,
                             bulletDedent='auto',
                             bulletDir='ltr',
                             bulletFormat=None,
                             start=None,
                             ),
                   alias='ul')
        styles.add(ListStyle(name='OrderedList',
                             parent=None,
                             leftIndent=18,
                             rightIndent=0,
                             bulletAlign='left',
                             bulletType='1',
                             bulletColor=black,
                             bulletFontName='Helvetica',
                             bulletFontSize=12,
                             bulletOffsetY=0,
                             bulletDedent='auto',
                             bulletDir='ltr',
                             bulletFormat=None,
                             start=None,
                             ),
                   alias='ol')
        return styles

    def _table_styles(self, label):
        if label == 'log':
            ts = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 6),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONT', (0, 0), (-1, 0), 'Times-Bold'),
            ])
        return ts

    def create_table(self, df, type):
        # Prepare df
        df = df.round(1)
        df = df.astype(str)
        df.replace(['0', '0.0'], '', inplace=True)
        # Specific format for daily log
        if type == 'log':
            # Rename columns
            old_columns = df.columns
            new_columns = [x[8::] for x in old_columns]
            columns = dict(zip(old_columns, new_columns))
            df = df.rename(columns=columns)
            # Remove multiIndex
            df.reset_index(inplace=True)
            df = df.rename(columns={'level_0': 'Project', 'level_1': 'Cat.'})
            # Split table
            d1 = df.iloc[:, :17]
            t1 = [d1.columns[:, ].values.astype(str).tolist()] + \
                 d1.values.tolist()
            table1 = Table(t1)
            d2 = df.iloc[:, 17:]
            headers = df.iloc[:, :2]
            d2 = pd.concat([headers, d2], axis=1, join_axes=[d2.index])
            t2 = [d2.columns[:, ].values.astype(str).tolist()] + \
                 d2.values.tolist()
            table2 = Table(t2)
            # Create table style
            style = self._table_styles('log')
            table1.setStyle(style)
            table2.setStyle(style)
            self._add_flowable(table1)
            self.create_spacer(10)
            self._add_flowable(table2)

    def _addNone(self, canvas, doc):
        pass

    def _addPageNumber(self, canvas, doc):
        text = f'Page {canvas.getPageNumber()}'
        canvas.drawRightString(self.width-1*cm, 1*cm, text)

    def _earth(self, canvas, doc):
        earth = pathlib.Path(resource('vmlib.ressources.images',
                                      'Geo2X_earth.jpg'))
        canvas.drawImage(earth,
                         -3*cm, -3*cm,
                         15*cm, 15*cm,
                         preserveAspectRatio=True)

    def _add_flowable(self, flowable):
        self.flowables.append(flowable)

    def create_title_page(self, title, subtitle, img, author):
        self.create_spacer(40)
        self.create_text(title, 'title')
        self.create_text(subtitle, 'subtitle')
        self.create_text(author, 'h4')
        # Image
        if img:
            self.create_spacer(30)
            self.create_image(img, align='CENTER', width=None, height=9,
                              caption=None)
            self.create_spacer(30)
        else:
            self.create_spacer(315)
        # Date
        self.create_text(strftime("%Y-%m-%d", gmtime()), 'h3r')
        # Logo et adresse
        self.create_spacer(30)
        logo = pathlib.Path(resource('vmlib.ressources.images',
                                     'Logo_Geo2X.jpg'))
        self.create_image(logo, align='RIGHT', width=None,
                          height=2, caption=None)
        self.create_spacer(15)
        self.create_text('Geo2X SA', 'br')
        self.create_text('Rue de Chamblon 34', 'br')
        self.create_text('1400 Yverdon-les-Bains', 'br')
        self.create_text('Switzerland', 'br')
        self.create_text('www.geo2x.com', 'br')
        self.create_text('+41 (0)21 881 48 00', 'br')
        self.create_text('info@geo2x.com', 'br')
        self.create_page_break()

    def save(self):
        self.doc.build(self.flowables,
                       onFirstPage=self._earth,
                       onLaterPages=self._addPageNumber)
