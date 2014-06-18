$(document).ready(function() {
    test_check();

    $("#id_destaque").click(function () {
        test_check();
    });
});

function test_check(){
    if($("#id_destaque").is(':checked'))
        $("#id_prioridade_destaque").parent().parent().show();
    else
        $("#id_prioridade_destaque").parent().parent().hide();
}

//if (typeof jQuery != 'undefined') {
//    window.alert('funcionando')
//} else {
//    window.alert('jquery necessita ser carregado...')
//}