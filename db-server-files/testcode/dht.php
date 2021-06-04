<?php
class dhtdata{
 public $link='';
 function __construct($temp, $hum){
  $this->connect();
  $this->storeInDB($temp, $hum);
 }
 
 function connect(){
  $this->link = mysqli_connect('localhost','root','akshay99') or die('Cannot connect to the DB');
  mysqli_select_db($this->link,'esp') or die('Cannot select the DB');
 }
 
 function storeInDB($temp, $hum){
  $query = "insert into dhtdata set hum='".$hum."', temp='".$temp."'";
  $result = mysqli_query($this->link,$query) or die('Errant query:  '.$query);
 }
 
}
if($_GET['temp'] != '' and  $_GET['hum'] != ''){
 $dhtdata=new dhtdata($_GET['temp'],$_GET['hum']);
}


?>
