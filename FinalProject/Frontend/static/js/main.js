$( document ).ready(function() {

  $("form").click(function() {
    console.log("I am inside click");
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
    console.log("Got a reply back");
              var myDiv = $('.answers'); // The place where you want to inser the template
              myDiv.html("");
              myDiv.html(msg);
           }
});
  });

});