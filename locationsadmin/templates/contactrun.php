<?php
require './config.php';
 ?>
<!DOCTYPE html>
<html>
<head>
	<title></title>
</head>
<body>
<?php

// echo "<pre>";
// print_r ($connection);
// echo "</pre>";



// echo "<pre>";
// print_r ($_POST);
// echo "</pre>";


if($_SERVER['REQUEST_METHOD']== "POST")
{
    //Something had posted
    $fullname = $_POST["fullname"];
    $contact = $_POST["contact"];
    $enquiry = $_POST["enquiry"];
    $email = $_POST["email"];
    $message = $_POST["message"];

    //save to database
    

    if(!empty($fullname) && !empty($contact) &&  !is_numeric($enquiry) && !empty($email))
    {
        
        $query = "INSERT INTO sbmcontactlist(`fullname` , `mobilenumber`, `enquiry`, `email`, `message`) VALUES('".$fullname."', '".$contact."', '".$enquiry."', '".$email."', '".$message."') ";
       $row2= mysqli_query($connection,$query);
       
      //  echo "<pre>";
      //  print_r ($query);
      //  echo "</pre>";
       
      //  echo "<pre>";
      //  print_r ($row2);
      //  echo "</pre>";exit;
       
       
       if($row2 > 0){
        // echo 'in';exit;
        // echo "Detail Added successfully";
          $url = 'https://www.neevsofttechnologies.com/api/MessageApi/Home/companyleadmnmnt';
            $Data=[
            "person"=>$fullname,
            "Company_name" => "School of Bollywood Music",
            "Enquiry" => $enquiry,
            "message" => $message,
            //"subject"=>"$Subject",
            "email" => $email,
            'contact' => $contact,
            "email_to" => "schoolofbollywoodmusic.in@gmail.com",
            "appid" => "4"];
            $Ch = curl_init();
            $Config = [];
            
                $Config = [
                    CURLOPT_URL => $url,
                    CURLOPT_POST => true,
                    CURLOPT_POSTFIELDS => $Data,
                    CURLOPT_RETURNTRANSFER => True
                ];
           
            curl_setopt_array($Ch,$Config);
            $Result = curl_exec($Ch);
            curl_close($Ch);
            // echo "<pre>";
            // print_r ($Result);
            // echo "</pre>";exit;
            
            
      }
        else{
          $data = array(
              'status' => 'error',
              'msg' => 'Something went wrong !',
          );
      }
    }


    }


// echo "<br> writing Confirmed";

?>
<div class="alert"><div>
<script>
var el = document.getElementsByClassName("alert")[0];
var count = 1;
setInterval(function (){
  if(count<1){
    window.location = "thanks.html";
  }
  else{
  el.innerHTML = "Redirection in "+ count + "s";
  count--;
}
}, 1000);

</script>
</body>
</html>