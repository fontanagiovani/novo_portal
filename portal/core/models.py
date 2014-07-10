# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Menu(MPTTModel):
    class Meta:
        ordering = ('titulo',)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='pai', verbose_name='Nivel 1')
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    url  =  models.CharField(max_length=250, blank=True,)

    def __unicode__(self):
        return self.titulo


class Selecao(models.Model):

    TIPO_BASE = (
        ('Vestibulares e Seleção',(
            ('VEST',u'Vestibulares'),
            ('SISU',u'SISU'),
            ('STEC',u'SISUTEC'),
            ('EXSE',u'Exames de Seleção'),
            ('PRSE',u'Processo Seletivo'),
            ('TREX',u'Transferência Externa')
            )
        ),
        ('Concursos Publicos',(
            ('DOCE',u'Docentes'),
            ('TEAD',u'Técnicos-administrativos'),
            ('AMBS',u'Concurso Misto')
            )
        ),
        ('Processos Seletivos',(
            ('PRTE',u'Professores substitutos e/ou temporários'),
            ('PEAD',u'Processos Seletivos - EAD'),
            ('PPRO',u'Processsos Seletivos - PRONATEC'),
            ('ROID',u'Remoção Interna - Docentes'),
            ('ROIT',u'Remoção Interna - TAEs')
            )
        )
    )

    STATUS = (
        ('ABT','Aberto'),
        ('AND','Em Andamento'),
        ('FNZ','Finalizado')
    )

    class Meta:
        ordering = ('titulo','status','data_abertura_edital')

    tipo = models.CharField(max_length=4, choices=TIPO_BASE)
    titulo = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    url  =  models.CharField(max_length=250, blank=True,)
    status = models.CharField(max_length=3, choices=STATUS)
    data_abertura_edital = models.DateTimeField(verbose_name=u'Data de Abertura do Edital')
    data_abertura_inscricoes = models.DateTimeField(verbose_name=u'Data de Abertura de Inscrições')
    data_encerramento_inscricoes = models.DateTimeField(verbose_name=u'Data de Fechamento das Incrições')
    data_publicacao = models.DateTimeField(verbose_name=u'Data de publicação')

    def __unicode__(self):
        return self.titulo