from docx import Document

def extract_text(docx_path):

    text = ""

    try:

        doc = Document(docx_path)

        for para in doc.paragraphs:

            text += para.text + "\n"

    except Exception as e:

        print(e)

    return text