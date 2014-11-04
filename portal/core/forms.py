# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils.safestring import mark_safe


class SiteDetalheFormset(BaseInlineFormSet):
    # pass
    def clean(self):
        """Check that at least one service has been entered."""
        super(SiteDetalheFormset, self).clean()

        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
            for cleaned_data in self.cleaned_data):
            raise forms.ValidationError(u'Você deve preencher os dois campos abaixo.')


class TinyMCEEditor(forms.Textarea):

    class Media:
        js = (
            'js/tinymce/tinymce.min.js',
        )

    def render(self, name, value, attrs=None):
        rendered = super(TinyMCEEditor, self).render(name, value, attrs)
        return rendered + mark_safe(u'''
        <script type="text/javascript">
            tinyMCE.init({
                // selector:'textarea',
                mode: "textareas",
                //plugins: [
                //    "hr link image charmap paste print preview anchor pagebreak searchreplace visualblocks
                // visualchars code fullscreen",
                //    "insertdatetime media nonbreaking save table emoticons template textcolor wordcount",
                //],
                plugins: [
                    "hr link paste image preview pagebreak searchreplace visualblocks visualchars code fullscreen",
                    "media table wordcount",
                ],
                toolbar: "undo redo removeformat blockquote subscript superscript formatbar | " +
                    "bold italic underline strikethrough | alignleft aligncenter alignright alignjustify " +
                    "| bullist numlist outdent indent | link image media | visualblocks preview fullscreen",

                language: 'pt_BR',
                content_css: '/static/css/base.css,/static/css/detalhe.min.css,/static/css/tinymce.css',
                height: 360,
                width: 1040,
                visualblocks_default_state: true,
                plugin_preview_width : '1040',
                paste_as_text: true,
                relative_urls : false,

                style_formats: [
                    {title: 'Headers', items: [
                        {title: 'h1', block: 'h1'},
                        {title: 'h2', block: 'h2'},
                        {title: 'h3', block: 'h3'},
                    ]},
                    {title: 'Blocks', items: [
                        {title: 'p', block: 'p'},
                        {title: 'div', block: 'div'},
                    ]},
                    {title: 'Adic. margem lateral à imagem', selector: 'img', styles: {
                        'margin': '5px 10px 5px 10px'
                    }},
                ],

                file_browser_callback: function(input_id, input_value, type, win){
                var cmsURL = '/admin/filer/folder/?_popup=1';

                tinymce.activeEditor.windowManager.open({
                    file: cmsURL,
                    width: 1000,  // Your dimensions may differ - toy around with them!
                    height: 500,
                    resizable: 'yes',
                    scrollbars: 'yes',
                    inline: 'yes',  // This parameter only has an effect if you use the inlinepopups plugin!
                    close_previous: 'no'
                }, {
                    window: win,
                    input: input_id,
                });
                return false;
                },
            });
        </script>''')