$(document).ready(function() {
    $("#id_password").addClass('col-md-12')
    $("#id_password").text("")
    $("#id_password").after('<button type="button" class="btn btn-sm mr-1 mt-2 mb-2 btn-primary" data-toggle="modal" data-target="#exampleModal" id="see_password">D    ecrypt Password</button><br>')
//    $("#see_password").on('click', function(event) {
//        event.preventDefault();
//        if($('#id_password').attr("type") == "text"){
//            $('#id_password').attr('type', 'password');
//            $('#id_password i').addClass( "fa-eye-slash" );
//            $('#id_password i').removeClass( "fa-eye" );
//        }else if($('#id_password').attr("type") == "password"){
//            $('#id_password').attr('type', 'text');
//            $('#id_password').removeClass( "fa-eye-slash" );
//            $('#id_password').addClass( "fa-eye" );
//        }
//    });
    $("input[name='online']").css("transform", "scale(0.7)")
});