class ProcessingException(Exception):
    "A data-related error occuring during file processing."
    pass


TIMEOUT = 3600  # seconds
CONVERT_RETRIES = 5


class AppEnvironment:
    def __init__(self, libreoffice_path):
        self.libreoffice_path = libreoffice_path
        self.timeout = TIMEOUT
        self.convert_retries = CONVERT_RETRIES

    def __repr__(self):
        return f"<AppEnvironment {self.libreoffice_path}>"


PDF_MIME_TYPES = ["application/pdf"]

DOCUMENT_MIME_TYPES = [
    # Text documents
    "text/richtext",
    "text/rtf",
    "application/rtf",
    "application/x-rtf",
    "application/msword",
    "application/vnd.ms-word",
    "application/wordperfect",
    "application/vnd.wordperfect",
    # Presentations
    "application/vnd.ms-powerpoint",
    "application/vnd.sun.xml.impress",
    "application/vnd.ms-powerpoint.presentation",
    "application/vnd.ms-powerpoint.presentation.12",
    # MS Office files with short stream missing
    "application/CDFV2-unknown",
    "application/CDFV2-corrupt" "application/clarisworks",  # ClarisWorks_Draw
    "application/epub+zip",  # EPUB Document
    "application/macwriteii",  # MacWrite
    "application/msword",  # MS Word 2007 XML VBA
    "application/prs.plucker",  # Plucker eBook
    "application/vnd.corel-draw",  # Corel Draw Document
    "application/vnd.lotus-wordpro",  # LotusWordPro
    "application/vnd.ms-powerpoint",  # MS PowerPoint 97 Vorlage
    "application/vnd.ms-powerpoint.presentation.macroEnabled.main+xml",  # Impress MS PowerPoint 2007 XML VBA  # noqa
    "application/vnd.ms-works",  # Mac_Works
    "application/vnd.palm",  # Palm_Text_Document
    "application/vnd.sun.xml.draw",  # StarOffice XML (Draw)
    "application/vnd.sun.xml.draw.template",  # draw_StarOffice_XML_Draw_Template  # noqa
    "application/vnd.sun.xml.impress",  # StarOffice XML (Impress)
    "application/vnd.sun.xml.impress.template",  # impress_StarOffice_XML_Impress_Template  # noqa
    "application/vnd.sun.xml.writer",  # StarOffice XML (Writer)
    "application/vnd.sun.xml.writer.global",  # writer_globaldocument_StarOffice_XML_Writer_GlobalDocument  # noqa
    "application/vnd.sun.xml.writer.template",  # writer_StarOffice_XML_Writer_Template  # noqa
    "application/vnd.sun.xml.writer.web",  # writer_web_StarOffice_XML_Writer_Web_Template  # noqa
    "application/vnd.visio",  # Visio Document
    "application/vnd.wordperfect",  # WordPerfect
    "application/x-abiword",  # AbiWord
    "application/x-aportisdoc",  # PalmDoc
    "application/x-fictionbook+xml",  # FictionBook 2
    "application/x-hwp",  # writer_MIZI_Hwp_97
    "application/x-iwork-keynote-sffkey",  # Apple Keynote
    "application/x-iwork-pages-sffpages",  # Apple Pages
    "application/x-mspublisher",  # Publisher Document
    "application/x-mswrite",  # MS_Write
    "application/x-pagemaker",  # PageMaker Document
    "application/x-sony-bbeb",  # BroadBand eBook
    "application/x-t602",  # T602Document
    "image/x-cmx",  # Corel Presentation Exchange
    "image/x-freehand",  # Freehand Document
    "image/x-wpg",  # WordPerfect Graphics

    # OOXML
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.template",
    "application/vnd.openxmlformats-officedocument.presentationml.slideshow",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.openxmlformats-officedocument.presentationml.template",
    "application/vnd.openxmlformats-officedocument.presentationml.slideshow",

    # OpenDOC
    "application/vnd.oasis.opendocument.text",
    "application/vnd.oasis.opendocument.text-template",
    "application/vnd.oasis.opendocument.presentation",
    "application/vnd.oasis.opendocument.graphics",
    "application/vnd.oasis.opendocument.graphics-flat-xml",
    "application/vnd.oasis.opendocument.graphics-template"
    "application/vnd.oasis.opendocument.presentation-flat-xml",
    "application/vnd.oasis.opendocument.presentation-template",
    "application/vnd.oasis.opendocument.chart",
    "application/vnd.oasis.opendocument.chart-template",
    "application/vnd.oasis.opendocument.image",
    "application/vnd.oasis.opendocument.image-template",
    "application/vnd.oasis.opendocument.formula",
    "application/vnd.oasis.opendocument.formula-template",
    "application/vnd.oasis.opendocument.text-flat-xml",
    "application/vnd.oasis.opendocument.text-master",
    "application/vnd.oasis.opendocument.text-web",
]

MAIL_MIME_TYPES = ["application/vnd.ms-outlook"]
