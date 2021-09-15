from os import path, getcwd

from pytest import mark
import pytest

from extract_text import Extract_PDF_Text


def test_envia_pdf():

    entrada = r'C:\Users\Emerson\Desktop\brainIAcs\SINISTROS_EXTRAIR_INFOS\CODES\extract_pdf_text\TESTS\fixtures\pdfs\Truque_Kernel.pdf'
    esperado = str

    local_save_txt = path.join(path.abspath(r'..'), "model_result")
    nome_save = "123.txt"

    result = Extract_PDF_Text().orchestra_extract_text(entrada, local_save_txt, nome_save)

    assert type(result) == esperado


test_envia_pdf()
