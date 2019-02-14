/**
 * Created by tarena on 18-9-6.
 */
/**
 * 功能：检查登录状态(AJAX)
 *  如果有登录信息的话，登录位置处显示 ： 欢迎 xxxx 退出
 *  如果没有登录信息的话，登录位置处显示：[登录][注册有惊喜]
 * */
function check_login(){
    $.get('/check_login/',function(data){
        var html = "";
        if(data.status == 0){
            html+="<a href='/login'>[登录]</a>,";
            html+="<a href='/register'>[注册有惊喜]</a>";
        }else if(data.status == 1){
            //用户已经处于登录状态
            user = JSON.parse(data.user)
            html+="欢迎:"+user.uname+"&nbsp;&nbsp;";
            html+="<a href='/logout/'>退出</a>";
        }
        $("#list>li:first").html(html);
    },'json');
}


function loadGoods(){
    $.get('/type_goods/',function(data){
        var html=""
        $.each(data,function(i,obj){
            html+="<div class='item'>";
            var typeObj=JSON.parse(obj.type);
                html+="<p class='title'>";
                  html+="<a href='#'>更多</a>";
                  html+="<img src='/"+typeObj.picture+"'>";
                html+="</p>"
                html+="<ul>";
                  var goodsArr=JSON.parse(obj.goods);
                  $.each(goodsArr,function(i,goods){
                      html+="<li";
                      if((i+1)%5==0)
                          html+="class='no-margin'";
                      html+=">";
                        html+="<p>";
                          html+="<img src='/"+goods.fields.picture+"'>";
                        html+="</p>";
                      html+="</li>";
                  });
                html+="</ul>"
            html+="</div>";
        });
        $("#main").html(html);

    },'json');
}

/**
 * 功能：网页加载时要执行的操作
 * */
$(function(){
    //检车登录状态 - check_login()
    check_login();
    loadGoods();
});