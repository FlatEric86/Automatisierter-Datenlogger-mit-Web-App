<?php
ini_set('display_errors', 'On');
error_reporting(E_ALL | E_STRICT);
session_start();

$benutzer = ["admin" => "12345", "Scientist" => "the_answer_is_42"];

$name = $_POST["name"] ?? "";
$passwort_aktuell = $_POST["passwort"] ?? "";

if (!array_key_exists($name, $benutzer)) {
	$extra = "start_scientist.php?f=1";
}

elseif ($benutzer[$name] != $passwort_aktuell) {
$extra = "start_scientist.php?f=2";
}
else {
$extra = "choose_params.php";
$_SESSION["login"] = "ok";
$_SESSION["name"] = $name;
}
header("Location: $extra");
?>
