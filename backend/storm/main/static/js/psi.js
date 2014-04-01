var $items;

function showRSS(str)
      {
          if (str.length==0) { 
            document.getElementById("psi").innerHTML="";
            return;
          }
          
        xmlhttp = new XMLHttpRequest();

        xmlhttp.onreadystatechange = function() {
          if (xmlhttp.readyState==4 && xmlhttp.status==200){
              document.getElementById("psi").innerHTML=xmlhttp.responseText;
          }
        }
        xmlhttp.open("GET","getrss.php?q="+str,true);
        xmlhttp.send();
      }

showRSS("psi");

$(function(){
 $("#psi").append(items);
 });