#!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import call # para chamar comando do sistema operacional
import sys # para passar argumentos
import pyPdf, re # pesquisar no pdf
import os # para criar diretório

# http://www.linuxjournal.com/content/tech-tip-extract-pages-pdf
# http://blog.evaldojunior.com.br/aulas/python/2009/02/15/curso-de-python-aula-13-passando-argumentos.html

# 2. Pessoa Física Beneficiária dos Rendimentos
# 2. PESSOA JURÍDICA FORNECEDORA DO BEM OU PRESTADORA DO SERVIÇO

string = ur'FORNECEDORA DO BEM OU PRESTADORA'
CNPJ_REGEXP='[0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\/?[0-9]{4}\-?[0-9]{2}'
CPF_REGEx='[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}\-?[0-9]{2}'
qtde_paginas = 1
param = sys.argv[1:]
if len(param) == 1:
    ano = input("Qual o ano de referência desejado? ")
    path = os.path.join("../../media/dirf/" + str(ano) + "/")
    if not os.path.exists(path):
        os.mkdir(path)
        print u"diretório " + path + u" criado"
    else:
        print u"diretório " + path + u" já existe"
    pdfDoc = pyPdf.PdfFileReader(file(param[0], "rb"))
    for i in range(0, pdfDoc.getNumPages()):
        content = ""
        content += pdfDoc.getPage(i).extractText().encode('utf-8')
        search = re.search(string, content, re.MULTILINE)
        if search is not None:
            if (i + qtde_paginas) > pdfDoc.getNumPages():
                pagina_final = pdfDoc.getNumPages()
            else:
                pagina_final = (i + qtde_paginas)
            cnpj = re.findall(CNPJ_REGEXP, content)
            print u"gerando arquivo da página " + str(i+1) + u" até " + str(pagina_final)
            if len(cnpj) == 2: # espera-se dois cnpjs por relatório
                output = call(["pdftk", "A="+(param[0]), "cat", "A"+str(i+1)+"-"+str(pagina_final), "output", path + cnpj[1].replace("-", "").replace(".", "").replace("/", "")+".pdf"])
            else:
                print u"Erro ao recuperar CNPJ do solicitante"
                break
else:
    print u"forma de execução: python splitpdf.py <arquivo>.pdf"
