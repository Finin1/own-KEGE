from spire.doc import Document, DocumentObjectType
from pathlib import Path


def parse_document(document: Document) -> None:
    section = document.Sections[0]
    table = section.Tables[0]
    rows = table.Rows
    for i in range(rows.Count):
        row = rows.get_Item(i)
        first_cell = row.Cells[0]
        second_cell = row.Cells[1]

        task_number = first_cell.Paragraphs[0].Text
        task_text = second_cell.Paragraphs[0].Text

        image = None
        second_cell_par_children = second_cell.Paragraphs[0].ChildObjects
        for j in range(second_cell_par_children.Count):
            obj = second_cell_par_children.get_Item(j)
            if obj.DocumentObjectType == DocumentObjectType.Picture:
                image = obj.ImageBytes

        htm_save_path = Path("template", f"task{task_number}.htm")
        with open(htm_save_path, "w", encoding="utf-8") as htm_file:
            htm_file.write(task_text.replace("\x0b", "\n"))
            

        if image is not None:
            img_save_path = Path("static", "img", f"img{task_number}.png")
            with open(img_save_path, "wb") as img_file:
                img_file.write(image)


if __name__ == "__main__":
    # document_to_parse = Document("test.docx")
    document_to_parse = Document()
    document_to_parse.LoadFromFile("test.docx")
    parse_document(document_to_parse)