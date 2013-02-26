$(document).ready(function(){ 
$("img.a").hover(
function() {
$(this).stop().animate({"opacity": "0"}, "normal");
},
function() {
$(this).stop().animate({"opacity": "1"}, "normal");
});  
});