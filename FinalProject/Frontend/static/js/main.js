$( document ).ready(function() {
  console.log("Inside jquery");

  var someGlobalArray = new Array;

  $("input[type='checkbox']").click(function() {
    console.log("I am here");
      someGlobalArray=[];
      $('#category:checked').each(function() {
          someGlobalArray.push($(this).val());
      });
      console.log(someGlobalArray);
        var data = {
      data: JSON.stringify({
                        "value":someGlobalArray
                  })
   };
$.ajax({
   url:"/data",
   type: 'POST',
   data: data,
  success: function(msg){
              var myDiv = $('.analyse_right'); // The place where you want to inser the template
              myDiv.html("");
              myDiv.html(msg);
            }
});
  });

 

});