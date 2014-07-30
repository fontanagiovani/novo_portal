# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Menu(MPTTModel):
    class Meta:
        ordering = ('ordem',)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name='Nivel 1')
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    url = models.CharField(max_length=250, blank=True,)
    ordem = models.IntegerField(default=None, null=True, blank=True, verbose_name=u'Ordem do Menu', unique=False)

    def __unicode__(self):
        return self.titulo

    def parent_show(self):
        if self.parent == None:
            return ""
        return self.parent

    def ordem_menu_show(self):
        if self.ordem == None:
            return ""
        return self.ordem

    def ordenacao(self, menus):
        for menu in menus:
            pass


class TipoSelecao(MPTTModel):
    class Meta:
        ordering = ('titulo',)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name='Tipo pai')
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __unicode__(self):
        return self.titulo


class Selecao(models.Model):

    # TIPO_BASE = (
    #     ('Vestibulares e Seleção',(
    #         ('VEST',u'Vestibulares'),
    #         ('SISU',u'SISU'),
    #         ('STEC',u'SISUTEC'),
    #         ('EXSE',u'Exames de Seleção'),
    #         ('PRSE',u'Processo Seletivo'),
    #         ('TREX',u'Transferência Externa')
    #         )
    #     ),
    #     ('Concursos Publicos',(
    #         ('DOCE',u'Docentes'),
    #         ('TEAD',u'Técnicos-administrativos'),
    #         )
    #     ),
    #     ('Processos Seletivos',(
    #         ('PRTE',u'Professores substitutos e/ou temporários'),
    #         ('PEAD',u'Processos Seletivos - EAD'),
    #         ('PPRO',u'Processsos Seletivos - PRONATEC'), ,
    #         ('ROID',u'Remoção Interna - Docentes'),
    #         ('ROIT',u'Remoção Interna - TAEs')
    #         )
    #     )
    # )

    STATUS = (
        ('ABT','Aberto'),
        ('AND','Em Andamento'),
        ('FNZ','Finalizado')
    )

    class Meta:
        ordering = ('titulo','status','data_abertura_edital')

    tipo = TreeForeignKey('TipoSelecao')
    titulo = models.CharField(max_length=100)
    url = models.CharField(max_length=250,)
    status = models.CharField(max_length=3, choices=STATUS)
    data_abertura_edital = models.DateTimeField(verbose_name=u'Data de Abertura do Edital')
    data_abertura_inscricoes = models.DateTimeField(verbose_name=u'Data de Abertura de Inscrições')
    data_encerramento_inscricoes = models.DateTimeField(verbose_name=u'Data de Fechamento das Incrições')
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')

    def __unicode__(self):
        return self.titulo
