"""

    MICROSERVIÇO PARA EXTRAÇÃO DE TEXTOS DE PDF'S DO TIPO TEXTO.
    O INPUT PODE SER:

    1) DIRETÓRIO CONTENDO VÁRIOS PDFS
    2) DIRETÓRIO ABSOLUTO DE UM ÚNICO PDF
    3) PDF EM FORMATO BASE64.

    # Arguments
        input_pdf_path              - Required : Caminho do arquivo a ser lido (String)

    # Returns
        text                        - Required : Texto do PDF enviado (String)

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "08/09/2021"


import io
from inspect import stack
from os import path, makedirs

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


class Extract_PDF_Text:

    """

        MICROSERVIÇO PARA EXTRAÇÃO DE TEXTOS DE PDF'S DO TIPO TEXTO.
        O INPUT PODE SER:

        1) DIRETÓRIO CONTENDO VÁRIOS PDFS
        2) DIRETÓRIO ABSOLUTO DE UM ÚNICO PDF
        3) PDF EM FORMATO BASE64.

        # Arguments
            input_pdf_path              - Required : Caminho do arquivo a ser lido (String)

        # Returns
            text                        - Required : Texto do PDF enviado (String)

    """

    def __init__(self):

        # 1 - LISTA DE TODOS OS TIPOS DE FORMATOS DE ARQUIVOS ACEITOS PARA EXTRAÇÃO DE TEXTO
        self.list_file_formats_accepted = ["pdf", "txt"]

        # 2 - DEFININDO O LOCAL DEFAULT DE SAVE DOS TXTS
        self.path_default = "model_output"

        # 3 - DEFININDO O NOME DEFAULT DE SAVE DOS TXTS
        self.nome_default = "resultado.txt"


    @staticmethod
    def create_path(dir):

        """

            FUNÇÃO PARA CRIAR UM PATH;

            # Arguments
                dir                      - Required : Diretório a ser criado (String)

            # Returns
                validador                - Required : Validador de execução da função (Boolean)

        """

        # INICIANDO O VALIDADOR DA FUNÇÃO
        validador = False

        try:
            makedirs(dir)
        except Exception as ex:
            print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

        return validador


    @staticmethod
    def verify_path(dir):

        """

            FUNÇÃO PARA VERIFICAR SE UM DIRETÓRIO (PATH) EXISTE.

            # Arguments
                dir                      - Required : Diretório a ser verificado (String)

            # Returns
                validador                - Required : Validador de execução da função (Boolean)

        """

        # INICIANDO O VALIDADOR DA FUNÇÃO
        validador = False

        try:
            validador = path.exists(dir)
        except Exception as ex:
            print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

        return validador


    def get_path_save_txt(self, path_save_txt_input):

        # VERIFICANDO SE NÃO FOI ENVIADO CAMINHO PARA SAVE DO TXT
        if path_save_txt_input is None:

            path_save_txt = path.join(self.path_default, path_save_txt_input.split("\\")[-1] + ".txt")

        elif path_save_txt_input.find(".txt") != -1:

            path_save_txt = path.join(self.path_default, path_save_txt_input.split("\\")[-1])

        return path_save_txt


    def save_txt(self, text, path_save_txt, nome_save_txt = None):

        """

            FUNÇÃO PARA ESCREVER/SALVAR O ARQUIVO TEXTO.

            # Arguments
                path_save_txt              - Required : Diretório do arquivo a ser escrito (String)
                text                       - Required : Texto que será escrito (String)

            # Returns
                validador                  - Required : Validador de execução da função (Boolean)

        """

        # INICIANDO O VALIDADOR DA FUNÇÃO
        validador = False

        # VERIFICANDO SE O PATH EXISTE
        validador_path = Extract_PDF_Text.verify_path(text, path_save_txt, nome_save_txt)

        if not validador_path:
            validador = Extract_PDF_Text.create_path(text, path_save_txt, nome_save_txt)

            if validador:

                # REALIZANDO A ABERTURA DO ARQUIVO (MESMO QUE NÃO EXISTENTE)
                with open(path_save_txt, "w", encoding="utf-8") as text_file:

                    try:
                        text_file.write(text)

                        validador = True

                    except Exception as ex:
                        print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

        return validador


    @staticmethod
    def read_txt(path_txt):

        """

            FUNÇÃO PARA LER ARQUIVO TXT.

            # Arguments
                path_txt                   - Required : Diretório do arquivo .txt (String)

            # Returns
                text                       - Required : Texto obtido do arquivo .txt (String)

        """

        try:
            with open(path_txt, "r") as text_file:

                text = text_file.read()

        except Exception as ex:
            print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

        return text


    @staticmethod
    def convert_pdf_to_text(fname, pages=None):

        """

            FUNÇÃO PARA CONVERTER PDF EM TEXTO.

            # Arguments
                fname                      - Required : Nome do arquivo (String)
                pages                      - Required : Página específica para
                                                        se fazer a leitura (Int)

            # Returns
                text                       - Required : Texto extraído do arquivo (String)

        """

        # VERIFICA SE HÁ UMA PÁGINA ESPECÍFICA PARA EXTRAIR
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)

        try:
            output = io.StringIO()

            # ARMAZENA RECURSOS COMPARTILHADOS
            manager = PDFResourceManager()

            # CONFIGURA A VARIÁVEL DE AUXÍLIO NA CONVERSÃO
            converter = TextConverter(manager, output, laparams=LAParams())

            # PROCESSA O CONTEÚDO DA PÁGINA
            interpreter = PDFPageInterpreter(manager, converter)

            # ABRINDO O ARQUIVO
            infile = open(fname, 'rb')

            # ITERA CADA PÁGINA DO PDF E REALIZA A CONVERSÃO
            for page in PDFPage.get_pages(infile, pagenums):
                interpreter.process_page(page)

        except Exception as ex:
            print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

        finally:
            infile.close()

            converter.close()

        try:
            # ARMAZENA O TEXTO EXTRAÍDO DO PDF
            text = output.getvalue()

        except Exception as ex:
            print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))


        finally:
            output.close()

        return text


    def validate_pdf(self, filename):

        """

            FUNÇÃO VERIFICADORA SE O ARQUIVO ENVIADO É DO TIPO PDF.

            RETORNA TRUE CASO O ARQUIVO ENVIADO SEJA PDF.

            # Arguments
                filename                   - Required : Caminho do arquivo a ser verificado (String)

            # Returns
                validador                  - Required : Validador de execução da função (Boolean)

        """

        # INICIANDO O VALIDADOR DA FUNÇÃO
        validador = False

        try:
            # OBTENDO O FORMATO DO ARQUIVO
            file_format = str(filename).split('\\')[-1].split('.')[-1]

            # VERIFICANDO SE O FORMATO DO ARQUIVO É ACEITO
            if file_format in self.list_file_formats_accepted:

                validador = True

        except Exception as ex:
            print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

        return validador


    def orchestra_extract_text(self, arq_dir, txt_dir, nome_save):

        """

            FUNÇÃO ORQUESTRADORA DE CONVERSÃO DE PDF PARA ARQUIVO TEXTO.

            # Arguments
                arq_dir                    - Required : Diretório do arquivo pdf (String)
                txt_dir                    - Required : Diretório para salvar
                                                        o arquivo txt (String)
                nome_save                  - Optional : Nome para salvar o arquivo (String)

            # Returns
                text                       - Required : Texto extraído do arquivo (String)

        """

        verified_arq = Extract_PDF_Text.validate_pdf(self, arq_dir)

        if verified_arq:

            # CONVERSÃO DE PDF PARA TEXTO
            try:
                text = Extract_PDF_Text.convert_pdf_to_text(arq_dir)
            except PDFTextExtractionNotAllowed:
                print("NÃO FOI POSSÍVEL EXTRAIR PDFTextExtractionNotAllowed")
            except PDFSyntaxError:
                print("NÃO FOI POSSÍVEL EXTRAIR PDFSyntaxError")
            except Exception as ex:
                print("NÃO FOI POSSÍVEL EXTRAIR: {}".format(str(ex)))

        else:
            try:
                text = Extract_PDF_Text.read_txt(arq_dir)
            except Exception as ex:
                print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

        # SALVANDO O TEXTO EM ARQUIVO TXT
        validador = Extract_PDF_Text.save_txt(self, txt_dir, text)

        return text

