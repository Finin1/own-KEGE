import re
from os import listdir
from pathlib import Path
from spire.doc import Document, DocumentObjectType, FileFormat, RowCollection


def parse_document_to_txt(document: Document) -> None:
    section = document.Sections[0]
    table = section.Tables[0]
    rows = table.Rows
    for i in range(rows.Count):
        row = rows.get_Item(i)
        first_cell = row.Cells[0]
        second_cell = row.Cells[1]

        task_number = first_cell.Paragraphs[0].Text
        

        image = None
        second_cell_par_children = second_cell.Paragraphs[0].ChildObjects
        for j in range(second_cell_par_children.Count):
            obj = second_cell_par_children.get_Item(j)
            if obj.DocumentObjectType == DocumentObjectType.Picture:
                image = obj.ImageBytes

        htm_save_path = Path("template", f"task{task_number}.htm")
        paragraphs = second_cell.Paragraphs
        with open(htm_save_path, "w", encoding="utf-8") as htm_file:
            for i in range(paragraphs.Count):
                task_text = paragraphs.get_Item(i).Text
                htm_file.write(task_text.replace("\x0b", "\n") + "\n")

        if image is not None:
            img_save_path = Path("static", "img", f"img{task_number}.png")
            with open(img_save_path, "wb") as img_file:
                img_file.write(image)


def separate_word_to_tasks(document: Document) -> None:
    section = document.Sections[0]
    table = section.Tables[0]
    rows = table.Rows
    for i in range(rows.Count):
        row = rows.get_Item(i)
        task_number = row.Cells[0].Paragraphs[0].Text 
        
        cut_off_task = Document()
        section = cut_off_task.AddSection()
        new_table = section.AddTable()
        new_table.AddRow()
        new_table.Rows.Insert(0, row.Clone())
        
        path_to_img = Path("..", "static", "img")
        cut_off_task.HtmlExportOptions.ImageEmbedded = False
        cut_off_task.HtmlExportOptions.ImagesPath = str(path_to_img)
        
        path_to_save = Path("template", f"task{task_number}.html")
        cut_off_task.SaveToFile(str(path_to_save), FileFormat.Html)
        cut_off_task.Close()


def remove_red_watermarks():
    tasks = listdir("template")
    for task in tasks:
        path_to_task = Path("template", task)
        with open(path_to_task, "r", encoding="utf-8") as html_file:
            old_html = html_file.readline()
        
        watermark_code = '''<p style="margin-top:0pt; margin-bottom:0pt; font-size:12pt"><span style="font-family:'Times New Roman'; color:#ff0000">Evaluation Warning: The document was created with Spire.Doc for Python.</span></p>'''
        old_html = old_html.replace(watermark_code, "")
        
        with open(path_to_task, "w", encoding="utf-8") as html_file:
            html_file.write(old_html) 


def remove_task_numbers():
    tasks = listdir("template")
    for task in tasks:
        path_to_task = Path("template", task)
        with open(path_to_task, "r", encoding="utf-8") as html_file:
            old_html = html_file.readline()
        
        column_tags_pattern = r"<td.*?>.*?<\/td>"
        column_tags = re.findall(column_tags_pattern, old_html)
        number_tag = column_tags[0]
        old_html = old_html.replace(number_tag, "")
        
        with open(path_to_task, "w", encoding="utf-8") as html_file:
            html_file.write(old_html)


def parse_document(path_to_document: Path) -> None:
    document_to_parse = Document()
    document_to_parse.LoadFromFile(str(path_to_document))
    separate_word_to_tasks(document_to_parse)
    remove_red_watermarks()
    remove_task_numbers()


if __name__ == "__main__":
    # document_to_parse = Document("test.docx")
    path_to_document = Path("test.docx")
    parse_document(path_to_document)
