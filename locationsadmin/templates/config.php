<?php
$host = "182.50.133.78"; // Put the host here
$username = "sbm_user"; // Put your username here for database
$password = "Sl!mSh@dy"; // the password if requires
$database = "sbm_sobmp"; // database name (naming it managerDB is recommended!)
$connection = mysqli_connect($host, $username, $password, $database) or die("<div style=\"color:red; font-size:50px; fonr-family:cursive ,arial;\"><span>No Connection, Returns Died.</span> <div style=\"color:teal;\">Error Info : ".mysqli_connect_error()."</div></div>");


// echo "<pre>";
// print_r ($connection);
// echo "</pre>";

if(!$connection)
{
    die("failed to connect!");
}
?>