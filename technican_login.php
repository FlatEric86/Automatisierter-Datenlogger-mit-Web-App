<?php
ini_set('display_errors', 'On');
error_reporting(E_ALL | E_STRICT);
session_start();

$benutzer = ["admin" => "12345", "Techniker_1" => "passwd"];

$name = $_POST["name"] ?? "";
$passwort_aktuell = $_POST["passwort"] ?? "";

if (!array_key_exists($name, $benutzer)) {
	$extra = "start_technican.php?f=1";
}

elseif ($benutzer[$name] != $passwort_aktuell) {
$extra = "start_technican.php?f=2";
}
else {
$extra = "show_measurements.php";
$_SESSION["login"] = "ok";
$_SESSION["name"] = $name;
}
header("Location: $extra");
?>
