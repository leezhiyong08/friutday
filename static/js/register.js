/**
 * Created by tarena on 19-1-10.
 */

function checkUphone(){
    var value=$("[name='uphone']").val();
    window.flag=false;
    if (value.trim().length == 11){
        $.ajax({
            url:"/check_uphone/",
            type:'post',
            // data:'uphone='+value,
            data:{
                uphone:value,
                csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()
            },
            async:false,
            dataType:'json',
            success:function(data){
                $("#uphone-show").html(data.text);
                if (data.status==1)
                    window.flag=true;
                else
                    window.flag=false;
            }
        });

    }else{
        $("#uphone-show").html('手机号码位数不正确');
        window.flag = false;
    }
    return window.flag;
}

$(function(){
    $("[name='uphone']").blur(function(){
        alert(checkUphone());
    })
});





