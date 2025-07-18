import logging
from pathlib import Path

import pytest

from fpdf import FPDF, FPDFException
from fpdf.drawing import DeviceRGB
from fpdf.enums import (
    TableBordersLayout,
    TableBorderStyle,
    TableCellFillMode,
    TableCellStyle,
    TextEmphasis,
)
from fpdf.fonts import FontFace
from test.conftest import LOREM_IPSUM, assert_pdf_equal

HERE = Path(__file__).resolve().parent

TABLE_DATA = (
    ("First name", "Last name", "Age", "City"),
    ("Jules", "Smith", "34", "San Juan"),
    ("Mary", "Ramos", "45", "Orlando"),
    ("Carlson", "Banks", "19", "Los Angeles"),
    ("Lucas", "Cimon", "31", "Angers"),
)

MULTILINE_TABLE_DATA = (
    ("Extract", "Text length"),
    (LOREM_IPSUM[:200], str(len(LOREM_IPSUM[:200]))),
    (LOREM_IPSUM[200:400], str(len(LOREM_IPSUM[200:400]))),
    (LOREM_IPSUM[400:600], str(len(LOREM_IPSUM[400:600]))),
    (LOREM_IPSUM[600:800], str(len(LOREM_IPSUM[600:800]))),
    (LOREM_IPSUM[800:1000], str(len(LOREM_IPSUM[800:1000]))),
    (LOREM_IPSUM[1000:1200], str(len(LOREM_IPSUM[1000:1200]))),
)

MULTI_HEADING_TABLE_DATA = (
    ("Fruits", "Dairy"),
    ("Apple", "Banana", "Cherry", "Cheese", "Milk", "Yogurt"),
    ("1", "2", "3", "4", "5", "6"),
    ("2", "3", "4", "5", "6", "7"),
    ("3", "4", "5", "6", "7", "8"),
)


def test_table_simple(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table() as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum)
    assert_pdf_equal(pdf, HERE / "table_simple.pdf", tmp_path)


def test_table_with_no_row():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table():
        pass


def test_table_with_no_column():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table() as table:
        for _ in TABLE_DATA:
            table.row()


def test_table_with_syntactic_sugar(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(TABLE_DATA):
        pass
    assert_pdf_equal(pdf, HERE / "table_simple.pdf", tmp_path)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table() as table:
        table.row(TABLE_DATA[0])
        table.row(TABLE_DATA[1])
        table.row(TABLE_DATA[2])
        table.row(TABLE_DATA[3])
        table.row(TABLE_DATA[4])
    assert_pdf_equal(pdf, HERE / "table_simple.pdf", tmp_path)


def test_table_with_fixed_col_width(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(TABLE_DATA, col_widths=pdf.epw / 5):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_fixed_col_width.pdf", tmp_path)


def test_table_with_fixed_col_width_and_align(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(TABLE_DATA, col_widths=pdf.epw / 5, align="L"):
        pass
    with pdf.table(TABLE_DATA, col_widths=pdf.epw / 5, align="C"):
        pass
    with pdf.table(TABLE_DATA, col_widths=pdf.epw / 5, align="R"):
        pass
    pdf.add_page()
    with pdf.table(TABLE_DATA, width=150, col_widths=(1, 1, 1, 1), align="L"):
        pass
    with pdf.table(TABLE_DATA, width=150, col_widths=(1, 1, 1, 1), align="C"):
        pass
    with pdf.table(TABLE_DATA, width=150, col_widths=(1, 1, 1, 1), align="R"):
        pass
    pdf.add_page()
    with pdf.table(TABLE_DATA, col_widths=(1, 1, 1, 1), align="L"):
        pass
    with pdf.table(TABLE_DATA, col_widths=(1, 1, 1, 1), align="C"):
        pass
    with pdf.table(TABLE_DATA, col_widths=(1, 1, 1, 1), align="R"):
        pass
    pdf.add_page()
    with pdf.table(TABLE_DATA, width=150, col_widths=(1, 1, 1, 1), align="L"):
        pass
    with pdf.table(TABLE_DATA, width=150, col_widths=(1, 1, 1, 1), align="C"):
        pass
    with pdf.table(TABLE_DATA, width=150, col_widths=(1, 1, 1, 1), align="R"):
        pass
    pdf.add_page()
    with pdf.table(TABLE_DATA, width=150, col_widths=37.5, align="L"):
        pass
    with pdf.table(TABLE_DATA, width=150, col_widths=37.5, align="C"):
        pass
    with pdf.table(TABLE_DATA, width=150, col_widths=37.5, align="R"):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_fixed_col_width_and_align.pdf", tmp_path)


def test_table_with_varying_col_widths(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(TABLE_DATA, col_widths=(30, 30, 10, 30)):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_varying_col_widths.pdf", tmp_path)


def test_table_with_invalid_col_widths():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pytest.raises(ValueError):
        with pdf.table(TABLE_DATA, col_widths=(20, 30, 50)):
            pass


def test_table_with_fixed_row_height(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(TABLE_DATA, line_height=2.5 * pdf.font_size):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_fixed_row_height.pdf", tmp_path)


def test_table_with_multiline_cells(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table() as table:
        for data_row in MULTILINE_TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum)
    assert pdf.pages_count == 2
    assert_pdf_equal(pdf, HERE / "table_with_multiline_cells.pdf", tmp_path)


def test_table_with_multiline_cells_and_fixed_row_height(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(line_height=2.5 * pdf.font_size) as table:
        for data_row in MULTILINE_TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum)
    assert pdf.pages_count == 2

    assert_pdf_equal(
        pdf, HERE / "table_with_multiline_cells_and_fixed_row_height.pdf", tmp_path
    )


def test_table_with_fixed_width(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(TABLE_DATA, width=150):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_fixed_width.pdf", tmp_path)


def test_table_with_invalid_width():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pytest.raises(ValueError):
        with pdf.table(TABLE_DATA, width=200):
            pass


def test_table_without_headings(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(TABLE_DATA, first_row_as_headings=False):
        pass
    assert_pdf_equal(pdf, HERE / "table_without_headings.pdf", tmp_path)


def test_table_with_multiline_cells_and_without_headings(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(first_row_as_headings=False) as table:
        for data_row in MULTILINE_TABLE_DATA + MULTILINE_TABLE_DATA[1:]:
            row = table.row()
            for datum in data_row:
                row.cell(datum)
    assert pdf.pages_count == 4
    assert_pdf_equal(
        pdf,
        HERE / "table_with_multiline_cells_and_without_headings.pdf",
        tmp_path,
    )


def test_table_with_headings_styled(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    blue = DeviceRGB(r=0, g=0, b=1)
    grey = 128
    headings_style = FontFace(
        emphasis=TextEmphasis.I | TextEmphasis.U, color=blue, fill_color=grey
    )
    with pdf.table(TABLE_DATA, headings_style=headings_style):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_headings_styled.pdf", tmp_path)


def test_table_with_multiline_cells_and_split_over_3_pages(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table() as table:
        for data_row in MULTILINE_TABLE_DATA + MULTILINE_TABLE_DATA[1:]:
            row = table.row()
            for datum in data_row:
                row.cell(datum)
    assert pdf.pages_count == 4
    assert_pdf_equal(
        pdf, HERE / "table_with_multiline_cells_and_split_over_3_pages.pdf", tmp_path
    )


def test_table_with_cell_fill(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    greyscale = 200
    with pdf.table(TABLE_DATA, cell_fill_color=greyscale, cell_fill_mode="ROWS"):
        pass
    pdf.ln()
    lightblue = (173, 216, 230)
    with pdf.table(TABLE_DATA, cell_fill_color=lightblue, cell_fill_mode="COLUMNS"):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_cell_fill.pdf", tmp_path)


class EvenOddCellFillMode:
    @staticmethod
    def should_fill_cell(i, j):
        return i % 2 and j % 2


def test_table_with_cell_fill_custom_class(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    lightblue = (173, 216, 230)
    with pdf.table(
        TABLE_DATA, cell_fill_color=lightblue, cell_fill_mode=EvenOddCellFillMode()
    ):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_cell_fill_custom_class.pdf", tmp_path)


def test_table_with_internal_layout(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(TABLE_DATA, borders_layout="INTERNAL"):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_internal_layout.pdf", tmp_path)


def test_table_with_minimal_layout(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    pdf.set_draw_color(100)  # dark grey
    pdf.set_line_width(1)
    with pdf.table(TABLE_DATA, borders_layout="MINIMAL"):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_minimal_layout.pdf", tmp_path)


def test_table_with_single_top_line_layout(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    pdf.set_draw_color(50)  # very dark grey
    pdf.set_line_width(0.5)
    with pdf.table(TABLE_DATA, borders_layout="SINGLE_TOP_LINE"):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_single_top_line_layout.pdf", tmp_path)


def test_table_with_single_top_line_layout_and_page_break(tmp_path):  # PR #912
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    pdf.set_draw_color(50)  # very dark grey
    pdf.set_line_width(0.5)
    data = list(MULTILINE_TABLE_DATA)
    # Reducing the text content on the 3rd line
    # so that there is an even number of rows on the 1st page:
    data[2] = (data[2][0][:-30], data[2][1])
    with pdf.table(
        borders_layout="SINGLE_TOP_LINE", cell_fill_color=230, cell_fill_mode="ROWS"
    ) as table:
        for data_row in data:
            row = table.row()
            for datum in data_row:
                row.cell(datum)
    assert_pdf_equal(
        pdf, HERE / "table_with_single_top_line_layout_and_page_break.pdf", tmp_path
    )


def test_table_with_page_break_and_headings_repeated(tmp_path):  # issue 1151
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    pdf.cell(text="repeat_headings=1:", new_y="NEXT")
    with pdf.table(
        MULTILINE_TABLE_DATA,
        repeat_headings=1,
    ):
        pass
    pdf.cell(text='repeat_headings="NONE":', new_y="NEXT")
    with pdf.table(
        MULTILINE_TABLE_DATA,
        repeat_headings="NONE",
    ):
        pass
    pdf.cell(text='repeat_headings="ON_TOP_OF_EVERY_PAGE":', new_y="NEXT")
    with pdf.table(
        MULTILINE_TABLE_DATA,
        repeat_headings="ON_TOP_OF_EVERY_PAGE",
    ):
        pass
    assert_pdf_equal(
        pdf, HERE / "table_with_page_break_and_headings_repeated.pdf", tmp_path
    )


def test_table_with_custom_border_layout(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font(family="helvetica", size=11)

    # generate a custom layout with most of the available features: changes in thickness, color,
    # and dash
    class CustomLayout(TableBordersLayout):
        def cell_style_getter(
            self,
            row_idx,
            col_idx,
            col_pos,
            num_heading_rows,
            num_rows,
            num_col_idx,
            num_col_pos,
        ):
            return TableCellStyle(
                left=(
                    TableBorderStyle(thickness=2)
                    if col_idx == 0
                    else TableBorderStyle(thickness=1.0, color=(0, 255, 125))
                ),
                bottom=(
                    TableBorderStyle(thickness=2) if row_idx == num_rows - 1 else False
                ),
                right=(
                    TableBorderStyle(thickness=2)
                    if col_idx == num_col_idx - 1
                    else False
                ),
                top=(
                    TableBorderStyle(thickness=2)
                    if row_idx in (0, num_heading_rows)
                    else (
                        True
                        if (row_idx - num_heading_rows) % 2 == 0
                        else TableBorderStyle(color=(255, 0, 0), dash=2)
                    )
                ),
            )

    with pdf.table(rows=TABLE_DATA, borders_layout=CustomLayout()):
        pass

    assert_pdf_equal(pdf, HERE / "table_with_custom_layout.pdf", tmp_path)


def test_table_align(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(TABLE_DATA, text_align="CENTER"):
        pass
    pdf.ln()
    with pdf.table(TABLE_DATA, text_align=("CENTER", "CENTER", "RIGHT", "LEFT")):
        pass
    assert_pdf_equal(pdf, HERE / "table_align.pdf", tmp_path)


def test_table_capture_font_settings(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    black = (0, 0, 0)
    lightblue = (173, 216, 230)
    with pdf.table(headings_style=FontFace(color=black, emphasis="B")) as table:
        for row_num, data_row in enumerate(TABLE_DATA):
            with pdf.local_context(text_color=lightblue):
                row = table.row()
                for col_num, datum in enumerate(data_row):
                    font_style = FontFace(
                        emphasis="I" if row_num > 0 and col_num == 0 else None
                    )
                    row.cell(datum, style=font_style)
    assert_pdf_equal(pdf, HERE / "table_capture_font_settings.pdf", tmp_path)


def test_table_with_ttf_font(caplog, tmp_path):  # issue 749
    caplog.set_level(logging.ERROR)  # hides fonttool warnings
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font(fname=HERE / "../fonts/cmss12.ttf")
    pdf.set_font("cmss12", size=16)
    with pdf.table(TABLE_DATA, first_row_as_headings=False):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_ttf_font.pdf", tmp_path)


def test_table_with_ttf_font_and_headings(caplog, tmp_path):
    caplog.set_level(logging.ERROR)  # hides fonttool warnings
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Roboto", fname=HERE / "../fonts/Roboto-Regular.ttf")
    pdf.add_font("Roboto", style="BI", fname=HERE / "../fonts/Roboto-BoldItalic.TTF")
    pdf.set_font("Roboto", size=16)
    with pdf.table(TABLE_DATA, headings_style=FontFace(emphasis="IB")):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_ttf_font_and_headings.pdf", tmp_path)


def test_table_with_ttf_font_and_headings_but_missing_bold_font():
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Quicksand", fname=HERE / "../fonts/Quicksand-Regular.otf")
    pdf.set_font("Quicksand", size=16)
    with pytest.raises(FPDFException) as error:
        with pdf.table(TABLE_DATA):
            pass
    assert (
        str(error.value)
        == "Using font 'quicksand' with emphasis 'B' in table headings require the corresponding font style to be added using add_font()"
    )


def test_table_with_cell_overflow(tmp_path):
    pdf = FPDF()
    pdf.set_font("Times", size=30)
    pdf.add_page()
    with pdf.table(width=pdf.epw / 2, col_widths=(1, 2, 1)) as table:
        row = table.row()
        row.cell("left")
        row.cell("center")
        row.cell("right")  # triggers header cell overflow on last column
        row = table.row()
        row.cell("A1")
        row.cell("A2")
        row.cell("A33333333")  # triggers cell overflow on last column
        row = table.row()
        row.cell("B1")
        row.cell("B2")
        row.cell("B3")
    assert_pdf_equal(pdf, HERE / "table_with_cell_overflow.pdf", tmp_path)


def test_table_with_gutter(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table(TABLE_DATA, gutter_height=3, gutter_width=3):
        pass
    pdf.ln(10)
    with pdf.table(
        TABLE_DATA, borders_layout="SINGLE_TOP_LINE", gutter_height=3, gutter_width=3
    ):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_gutter.pdf", tmp_path)


def test_table_with_gutter_and_width(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    pdf.cell(text="Without gutter:", new_y="NEXT")
    pdf.ln()
    with pdf.table(TABLE_DATA, width=150):
        pass
    pdf.ln()
    pdf.cell(text="With gutter:", new_y="NEXT")
    pdf.ln()
    with pdf.table(TABLE_DATA, width=150, gutter_height=3, gutter_width=3):
        pass
    assert_pdf_equal(pdf, HERE / "table_with_gutter_and_width.pdf", tmp_path)


def test_table_with_colspan_and_gutter(tmp_path):  # issue 808
    pdf = FPDF()
    pdf.set_font("Times", size=30)
    pdf.add_page()
    with pdf.table(col_widths=(1, 2, 1, 1), gutter_height=5, gutter_width=5) as table:
        row = table.row()
        row.cell("0")
        row.cell("1")
        row.cell("2")
        row.cell("3")
        row = table.row()
        row.cell("A1")
        row.cell("A2", colspan=2)
        row.cell("A3")
        row = table.row()
        row.cell("B1", colspan=2)
        row.cell("B2")
        row.cell("B3")
    assert_pdf_equal(pdf, HERE / "table_with_colspan_and_gutter.pdf", tmp_path)


def test_table_with_capitalized_font_family_and_emphasis():  # issue 828
    pdf = FPDF()
    pdf.add_page()
    with pdf.table(
        TABLE_DATA, headings_style=FontFace(family="Helvetica", emphasis="ITALICS")
    ):
        pass


def test_table_with_no_headers_nor_horizontal_lines(tmp_path):  # discussion 924
    pdf = FPDF()
    pdf.set_font("Helvetica")
    pdf.add_page()
    with pdf.table(
        TABLE_DATA,
        cell_fill_color=200,
        cell_fill_mode="ROWS",
        text_align="LEFT",
        borders_layout="NO_HORIZONTAL_LINES",
        first_row_as_headings=False,
    ):
        pass
    assert_pdf_equal(
        pdf, HERE / "table_with_no_headers_nor_horizontal_lines.pdf", tmp_path
    )


def test_table_page_break_with_table_in_header(tmp_path):  # issue 943
    class PDF(FPDF):
        def header(self):
            with self.table() as t:
                r = t.row()
                r.cell("headertext")

    pdf = PDF()
    pdf.set_font("helvetica", style="B", size=8)
    pdf.add_page()
    with pdf.table() as table:
        for _ in range(1, 15):
            for data_row in TABLE_DATA:
                table.row(data_row)
    assert_pdf_equal(pdf, HERE / "table_page_break_with_table_in_header.pdf", tmp_path)


def test_table_with_multiple_headings_and_pagebreak(tmp_path):
    pdf = FPDF()
    pdf.set_font("Times", size=12)
    pdf.add_page()
    pdf.set_y(240)
    with pdf.table(
        num_heading_rows=2,
    ) as table:
        for j, rowdata in enumerate(MULTI_HEADING_TABLE_DATA):
            if j == 0:
                # row with colspan
                row = table.row()
                for cell in rowdata:
                    row.cell(text=cell, colspan=3)
            else:
                table.row(cells=rowdata)
    assert_pdf_equal(
        pdf,
        HERE / "table_with_multiple_headings_and_pagebreak.pdf",
        tmp_path,
    )


def test_table_num_heading_rows_and_first_row_as_headings():
    pdf = FPDF()
    pdf.set_font("Times", size=12)
    pdf.add_page()
    with pytest.raises(ValueError):
        with pdf.table(TABLE_DATA, first_row_as_headings=True, num_heading_rows=0):
            pass
    with pytest.raises(ValueError):
        with pdf.table(TABLE_DATA, first_row_as_headings=False, num_heading_rows=2):
            pass


def test_table_with_multiple_headings_and_no_horizontal_lines(tmp_path):
    pdf = FPDF()
    pdf.set_font("Times", size=12)
    pdf.add_page()
    with pdf.table(
        borders_layout="NO_HORIZONTAL_LINES",
        num_heading_rows=2,
    ) as table:
        for j, rowdata in enumerate(MULTI_HEADING_TABLE_DATA):
            if j == 0:
                # row with colspan
                row = table.row()
                for cell in rowdata:
                    row.cell(text=cell, colspan=3)
            else:
                table.row(cells=rowdata)
    assert_pdf_equal(
        pdf,
        HERE / "table_with_multiple_headings_and_no_horizontal_lines.pdf",
        tmp_path,
    )


def test_table_with_minimal_layout_and_multiple_headings(tmp_path):
    pdf = FPDF()
    pdf.set_font("Times", size=12)
    pdf.add_page()
    pdf.set_draw_color(100)  # dark grey
    pdf.set_line_width(1)
    with pdf.table(borders_layout="MINIMAL", num_heading_rows=2) as table:
        for j, rowdata in enumerate(MULTI_HEADING_TABLE_DATA):
            if j == 0:
                # row with colspan
                row = table.row()
                for cell in rowdata:
                    row.cell(text=cell, colspan=3)
            else:
                table.row(cells=rowdata)
    assert_pdf_equal(
        pdf, HERE / "table_with_minimal_layout_and_multiple_headings.pdf", tmp_path
    )


def test_table_with_single_top_line_layout_and_multiple_headings(tmp_path):
    pdf = FPDF()
    pdf.set_font("Times", size=12)
    pdf.add_page()
    with pdf.table(
        borders_layout="SINGLE_TOP_LINE",
        num_heading_rows=2,
    ) as table:
        for j, rowdata in enumerate(MULTI_HEADING_TABLE_DATA):
            if j == 0:
                # row with colspan
                row = table.row()
                for cell in rowdata:
                    row.cell(text=cell, colspan=3)
            else:
                table.row(cells=rowdata)

    assert_pdf_equal(
        pdf,
        HERE / "table_with_single_top_line_layout_and_multiple_headings.pdf",
        tmp_path,
    )


def test_table_with_no_horizontal_lines_layout(tmp_path):
    pdf = FPDF()
    pdf.set_font("Times", size=12)
    pdf.add_page()
    with pdf.table(
        TABLE_DATA,
        borders_layout="NO_HORIZONTAL_LINES",
        num_heading_rows=1,
    ):
        pass
    assert_pdf_equal(
        pdf,
        HERE / "table_with_no_horizontal_lines_layout.pdf",
        tmp_path,
    )


def test_table_with_heading_style_overrides(tmp_path):
    pdf = FPDF()
    pdf.set_font(family="helvetica", size=10)
    pdf.add_page()

    with pdf.table(
        headings_style=FontFace(emphasis="B", size_pt=18), num_heading_rows=2
    ) as table:
        # should be Helvetica bold size 18
        table.row().cell("Big Heading", colspan=3)
        second_header = table.row()
        # should be Helvetica bold size 14:
        second_header_style_1 = FontFace(size_pt=14)
        second_header.cell("First", style=second_header_style_1)
        # should be Times italic size 14
        second_header_style_2_3 = FontFace(family="times", emphasis="I", size_pt=14)
        second_header.cell("Second", style=second_header_style_2_3)
        second_header.cell("Third", style=second_header_style_2_3)
        # should be helvetica normal size 10
        table.row(("Some", "Normal", "Data"))

    assert_pdf_equal(pdf, HERE / "table_with_heading_style_overrides.pdf", tmp_path)


def test_table_with_set_fill_color(tmp_path):  # issue 963
    pdf = FPDF()
    pdf.set_font("helvetica", size=10)
    pdf.add_page()
    with pdf.table(first_row_as_headings=False) as table:
        row = table.row()
        pdf.set_fill_color(200)
        pdf.set_fill_color(200, 200, 200)
        row.cell("Hello")
    assert_pdf_equal(pdf, HERE / "table_with_set_fill_color.pdf", tmp_path)


def test_table_with_fill_color_set_beforehand(tmp_path):  # issue 932
    pdf = FPDF()
    pdf.set_font("Helvetica")
    pdf.set_fill_color((126, 217, 87))  # green
    pdf.add_page()
    with pdf.table(
        cell_fill_color=(200, 200, 200),  # light grey
        cell_fill_mode="COLUMNS",
        headings_style=FontFace(fill_color=(255, 255, 255)),  # white
    ) as table:
        for i, data_row in enumerate(TABLE_DATA):
            if i == 2:
                style = FontFace(fill_color=(250, 128, 114))  # salmon
            else:
                style = None
            row = table.row(style=style)
            for j, datum in enumerate(data_row):
                if i == 2 and j == 2:
                    style = FontFace(fill_color=(50, 50, 50))  # very dark grey
                else:
                    style = None
                row.cell(datum, style=style)
    assert_pdf_equal(pdf, HERE / "table_with_fill_color_set_beforehand.pdf", tmp_path)


def test_table_with_links(tmp_path):  # issue 1031
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=16)
    with pdf.table() as table:
        for i, data_row in enumerate(TABLE_DATA):
            row = table.row()
            for j, datum in enumerate(data_row):
                if j == 2 and i > 0:
                    row.cell(text=datum, link="https://py-pdf.github.io/fpdf2/")
                else:
                    row.cell(datum)
    assert_pdf_equal(pdf, HERE / "table_with_links.pdf", tmp_path)


def test_table_with_varying_col_count(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica")
    # test table with reducing number of rows
    with pdf.table() as table:
        for i, data_row in enumerate(TABLE_DATA):
            subset = data_row[:-i] if i else data_row
            table.row(subset)
    pdf.ln(3)
    # table with less columns in first row
    with pdf.table(first_row_as_headings=False) as table:
        for i, data_row in enumerate(TABLE_DATA[1:], start=1):
            subset = data_row[:i]
            table.row(subset)

    assert_pdf_equal(pdf, HERE / "table_with_varying_col_count.pdf", tmp_path)


def test_table_cell_fill_mode(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica")
    light_sky_blue = (150, 200, 255)
    headings_style = FontFace(fill_color=128)  # grey
    for mode in ("ROWS", "COLUMNS", "EVEN_ROWS", "EVEN_COLUMNS"):
        pdf.cell(text=f"cell_fill_mode=TableCellFillMode.{mode}:")
        pdf.ln(10)
        with pdf.table(
            TABLE_DATA,
            headings_style=headings_style,
            cell_fill_mode=getattr(TableCellFillMode, mode),
            cell_fill_color=light_sky_blue,
        ):
            pass
        pdf.ln()
    assert_pdf_equal(pdf, HERE / "table_cell_fill_mode.pdf", tmp_path)


def test_table_with_very_long_text():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica")
    with pytest.raises(ValueError) as error:
        with pdf.table() as table:
            row = table.row()
            row.cell(LOREM_IPSUM)
            # Adding columns to have the content of the 1st cell to overflow:
            row.cell("")
            row.cell("")
    assert (
        str(error.value)
        == "The row with index 0 is too high and cannot be rendered on a single page"
    )
    with pytest.raises(ValueError) as error:
        with pdf.table() as table:
            row = table.row()
            row.cell("")
            row.cell("")
            row.cell(LOREM_IPSUM)
    assert (
        str(error.value)
        == "The row with index 0 is too high and cannot be rendered on a single page"
    )


def test_table_cell_border_none(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border="None")
    assert_pdf_equal(pdf, HERE / "test_table_cell_border_none.pdf", tmp_path)


def test_table_cell_different_borders(tmp_path):
    pdf = FPDF()
    pdf.set_font("Times", size=20)
    pdf.add_page()
    pdf.cell(
        0,
        10,
        "border = left",
    )
    pdf.ln(20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border="left")
    pdf.add_page()
    pdf.cell(0, 10, "border = right")
    pdf.ln(20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border="right")
    pdf.add_page()
    pdf.cell(0, 10, "border = top")
    pdf.ln(20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border="top")
    pdf.add_page()
    pdf.cell(0, 10, "border = bottom")
    pdf.ln(20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border="bottom")
    pdf.add_page()
    pdf.cell(0, 10, "border = [left, right]")
    pdf.ln(20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border=3)
    pdf.add_page()
    pdf.cell(0, 10, "border =[left, top]")
    pdf.ln(20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border=5)
    pdf.add_page()
    pdf.cell(0, 10, "border =[left, bottom]")
    pdf.ln(20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border=9)
    pdf.add_page()
    pdf.cell(0, 10, "border =[right, top]")
    pdf.ln(20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border=6)
    pdf.add_page()
    pdf.cell(0, 10, "border =[right, bottom]")
    pdf.ln(20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border=10)
    pdf.add_page()
    pdf.cell(0, 10, "border =[top, bottom]")
    pdf.ln(20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border=12)
    pdf.add_page()
    pdf.cell(0, 10, "border =[left, right, top]")
    pdf.ln(20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border=7)
    pdf.add_page()
    pdf.cell(0, 10, "border =[left, right, bottom]")
    pdf.ln(20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border=11)
    pdf.add_page()
    pdf.cell(0, 10, "border =[left, right, top, bottom]")
    pdf.ln(20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border=15)
    assert_pdf_equal(pdf, HERE / "test_table_cell_different_borders.pdf", tmp_path)


def test_table_cell_border_all(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=20)
    with pdf.table(gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                print(datum, end=" ")
                row.cell(datum, border="all")
    assert_pdf_equal(pdf, HERE / "test_table_cell_border_all.pdf", tmp_path)


def test_table_cell_border_inherit(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=20)
    pdf.cell(0, 10, "border = 'inherit' and borders_layout = 'none'")
    pdf.ln(20)
    with pdf.table(borders_layout="none", gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border="inherit")
    pdf.add_page()
    pdf.cell(0, 10, "border = 'inherit' and borders_layout = 'all'")
    pdf.ln(20)
    with pdf.table(borders_layout="all", gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                print(datum, end=" ")
                row.cell(datum, border="inherit")
    pdf.add_page()
    pdf.cell(0, 10, "border = 'inherit' and borders_layout = 'horizontal_lines'")
    pdf.ln(20)
    with pdf.table(
        borders_layout="horizontal_lines", gutter_height=3, gutter_width=3
    ) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border="inherit")
    pdf.add_page()
    pdf.cell(0, 10, "border = 'inherit' and borders_layout = 'internal' ")
    pdf.ln(20)
    with pdf.table(borders_layout="internal", gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border="inherit")
    pdf.add_page()
    pdf.cell(0, 10, "border = 'inherit' and borders_layout = 'minimal'")
    pdf.ln(20)
    with pdf.table(borders_layout="minimal", gutter_height=3, gutter_width=3) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border="inherit")
    pdf.add_page()
    pdf.cell(0, 10, "border = 'inherit' and borders_layout = 'no_horizontal_lines'")
    pdf.ln(20)
    with pdf.table(
        borders_layout="no_horizontal_lines", gutter_height=3, gutter_width=3
    ) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border="inherit")
    pdf.add_page()
    pdf.cell(0, 10, "border = 'inherit' and borders_layout = 'single_top_line'")
    pdf.ln(20)
    with pdf.table(
        borders_layout="single_top_line", gutter_height=3, gutter_width=3
    ) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum, border="inherit")
    assert_pdf_equal(pdf, HERE / "test_table_cell_border_inherit.pdf", tmp_path)


def test_table_min_row_height(tmp_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=20)
    with pdf.table(min_row_height=30) as table:
        table.row(("A", "B"))
        table.row(("C", "D"), min_height=50)
    assert_pdf_equal(pdf, HERE / "table_min_row_height.pdf", tmp_path)
