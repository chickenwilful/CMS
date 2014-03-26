<?php
//get the q parameter from URL
$q=$_GET["q"];

//find out which feed was selected
if($q=="psi"){
  $xml=("http://app2.nea.gov.sg/data/rss/nea_psi.xml");
}
  
$xmlDoc = new DOMDocument();
$xmlDoc->load($xml);

//get and output "<item>" elements
$x=$xmlDoc->getElementsByTagName('item');

for ($i=0; $i<=2; $i++) {
  $item_time=$x->item($i)->getElementsByTagName('pubDate')
  ->item(0)->childNodes->item(0)->nodeValue;
  $item_psi=$x->item($i)->getElementsByTagName('psi')
  ->item(0)->childNodes->item(0)->nodeValue;

  echo ($item_time.": ".$item_psi. "<br>");
}
?>