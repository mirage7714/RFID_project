$(function () {
    $('#btnGate').click(function (e) {
        $.ajax({
            beforeSend: function(){
                var id = "#btnGate"; 
				var left = ($(window).outerWidth(true) - 190) / 2; 
				var top = ($(window).height() - 35) / 2; 
				var height = $(window).height() * 2; 
				$("<div class=\"datagrid-mask\"></div>").css({ display: "block", width: "100%", height: height }).appendTo(id); 
				$("<div class=\"datagrid-mask-msg\"></div>").html("正在加载,请稍候...").appendTo(id).css({ display: "block", left: left, top: top }); 
            },
            url: '/query_gate',
            type: 'POST',
            dataType: 'json',
            success: function () {
                $(".datagrid-mask").remove(); 
				$(".datagrid-mask-msg").remove(); 
            }
        });
    });
});

