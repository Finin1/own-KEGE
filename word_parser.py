from spire.doc import Document, DocumentObjectType, FileFormat, RowCollection
from pathlib import Path


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
        
        cut_off_task.HtmlExportOptions.ImageEmbedded = False
        cut_off_task.HtmlExportOptions.ImagesPath = "static\\img"
        
        path_to_save = Path("template", f"task{task_number}.html")
        cut_off_task.SaveToFile(str(path_to_save), FileFormat.Html)
        cut_off_task.Close()


if __name__ == "__main__":
    # document_to_parse = Document("test.docx")
    document_to_parse = Document()
    document_to_parse.LoadFromFile("test.docx")
    separate_word_to_tasks(document_to_parse)
