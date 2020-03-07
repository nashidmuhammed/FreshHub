
$(function() {
    $(document).ready(function() {
    console.log("ready function")

    });

$(function() {
    $('.gt_otp').click(function() {
    console.log("readyyy")
    var email = $('#user_email').val();
    var name = $('#name').val();
        $.ajax({
            url: 'send_otp',
            data: {email:eamil, name:name },
            type: 'POST',
            success: function(data) {
                if(data.user == 0){
                $('#div_pass').show();
                $('#div_repass').show();
                $('#div_otp').show();
                $('#div_get').hide();
                $('#div_reg').show();
                alert("OTP send to your email...please check and verify?")
                }
                else if(data.user == 1){
                alert("Invalid header found.");
                }
                else{
                alert("Invalid Email");
                }

            },
            error: function(error) {
                console.log(error);
            }
        });
    });