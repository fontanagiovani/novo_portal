/**
 * Created by eldio on 01/09/14.
 */
$(document).ready(function() {
    test_pregao_srp();
    test_possui_contrato();

    $("#id_pregao_srp").click(function () {
        test_pregao_srp();
    });
    $("#id_possui_contrato").click(function () {
        test_possui_contrato();
    });
});

function test_pregao_srp(){
    if($("#id_pregao_srp").is(':checked'))
        $("#id_validade_ata_srp").parent().parent().show();
    else
        $("#id_validade_ata_srp").parent().parent().hide();
}

function test_possui_contrato(){
    if($("#id_possui_contrato").is(':checked')) {
        $("#id_vigencia_contrato_inicio").parent().parent().show();
        $("#id_vigencia_contrato_fim").parent().parent().show();
    }
    else {
        $("#id_vigencia_contrato_inicio").parent().parent().hide();
        $("#id_vigencia_contrato_fim").parent().parent().hide();
    }
}


//if (typeof jQuery != 'undefined') {
//    window.alert('funcionando')
//} else {
//    window.alert('jquery necessita ser carregado...')
//}