$( document ).ready(function() {
  
  console.log("ready");
$("#params input[type=checkbox]").click(function(){
    if ($(this).attr("checked") == "checked"){
    	alert($(this).attr("value"))
    	$.ajax({
		    type: 'POST',
		    url: '../../data',
		    crossDomain: true,
		    data: '{"some":"json"}',
		    dataType: 'json'
		});

    } else {
      $(this + " input").attr("checked") = "";
    }
 
  });

});