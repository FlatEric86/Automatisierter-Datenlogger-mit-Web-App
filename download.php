<?php

if (scandir('./downloadfiles')) {
	if (count(scandir('./downloadfiles')) == 2){
		echo 'Sorry, the file you requested has been either delated or an error has occoured</br>Please try again by starting a new session.</br>If the problem persists, please contact the admin!';
		exit;
	}
	foreach (scandir('./downloadfiles') as $file_name){
		if ($file_name != '.' &&  $file_name != '..'){
			$dwnld_fl = $file_name;
		}
	}

	$file_path = './downloadfiles/'.$dwnld_fl;
	header("Content-type: text/csv");
	header('Content-Encoding: UTF-8');
	header("Content-Disposition: attachment; filename={$file_name}");
	header("Pragma: no-cache");
	header("Expires: 0");
	readfile('./downloadfiles/'.$dwnld_fl);

	// delate file after downloading
	unlink($file_path);
	exit;

}
else{
	echo 'Sorry, there is an error...Please contact the admin!';

}

?>
