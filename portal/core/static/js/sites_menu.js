$(document).ready(function () {
    atualizar_menus();
    $("#id_site").change(atualizar_menus);
});

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function atualizar_menus() {
    var csrftoken = getCookie('csrftoken');
    site_id = $('#id_site').val();

    if (site_id == "") {
        site_id = 0;
        $("#id_parent").html("<option value=''>---------</option>");
    }
    else {
        $.ajax({
            url: '/admin_site_menu/' + site_id + '/',
            type: 'POST',
            dataType: 'json',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            success: function (json) {
                var options = "<option value='0'>--------</option>";

                $.each(json, function (key, value) {
                    options += '<option value="' + value.id + '">' + value.titulo + '</option>';
                });
//                    alert(options);
                $("#id_parent").html(options);
            },
            error: function (xhr, errmsg, err) {
                alert(xhr.status + ": " + xhr.responseText);
            }
        });
    }
    return false;
}