<html>
	<meta charset="utf8">
	<title>
		CSV_FILE_DOWNLOAD
	</title>
	<style>
		body {
			font-family: Consolas, monace, monospace;
			font-size: 10px;
			font-style: normla;
		}

		.warning_1 {
			font-family: Arial, san-serif;
			font-size: 50px;
			color: red;
			text-align: center;
		}

		.oumpf {
			display: flex;
			justify-content: center;
		}

		.btn {
			background-color: Blue;
			border: none;
			color: white;
			padding: 12px 12px;
			coursor: pointer;
			font-size: 20px;
			margin: auto;
			display: block;
		}

		.btn:hover {
			background-color: RoyalBlue;
		}

		.download_text{
			text-align: center;
			font-family: Arial;
			font-size: 2em;
		}

	</style>
	<body>

		<?php



		// parameter name space	
		$PARAM_NAMES = [  'H2O'
				, 'CO2'
				, 'N2O'
				, 'NH3'
				, 'CH4'
				, 'Cetan'
				, 'Ethanol'
				, 'Formaldehyd'
				, 'Acetaldehyd'
				, 'Aceton'
				, 'Ameisensäure'
				, 'Essigsäure'
				, 'Milchsäure'
				, 'Status'
		];


		// get parameter selection by evaluating the handled user entries
		$PARAM_SELECTION = [];
		foreach ($PARAM_NAMES as $param_nm) {
			if (isset($_POST[$param_nm])) {
				array_push($PARAM_SELECTION, $param_nm);	
			}
		}

		if (empty($_POST['gage_id']) && count($PARAM_SELECTION) == 0) {
			echo '<div class="warning_1">';
			echo '</br></br></br></br>';
			echo "You have not selected any parameters...";
			echo '</div>';
			exit(1);
		}


		if (empty($_POST['gage_id'])) {
			echo '<div class="warning_1">';
			echo '</br></br></br></br>';
			echo "Please select a gage...";
			echo '</div>';
			echo '<div class="oumpf">';
			echo '<img src="./graphics/startrek-picard-facepalm-700x341.jpg"/>';
			echo '</div>';
			exit(1);
		}




		if (count($PARAM_SELECTION) == 0) {
			echo '<div class="warning_1">';
			echo '</br></br></br></br>';
			echo "You didn't chosen any parameters!";
			echo '</div>';
			echo '<div class="oumpf">';
			echo '<img src="./graphics/startrek-picard-facepalm-700x341.jpg"/>';
			echo '</div>';
			exit(1);
		}

		/* main part | iterates over the parameter selection and gets the corresponded entries from the 
		 data base and write them to an html based text output */
		if ($db = mysqli_connect("localhost", "webserver", "ZitrON3Nkuchen", "dummerstorf")) {
			$sql = "SELECT * FROM ".$_POST['gage_id'];
			if ($ALL_DATA=mysqli_query($db, $sql)) {

				// create file_path to csv download
				$csv_path = './downloadfiles/'.$_POST['gage_id'];
				$csv_file_name = $_POST['gage_id'];
//-- line 100 --//
				$i = 1;
				foreach($PARAM_SELECTION as $param_name) {
					if ($i == count($PARAM_SELECTION)) {
						$csv_path = $csv_path.'_'.$param_name.'.csv';
						$csv_file_name.'_'.$param_name.'.csv';
					}
					else {
						$csv_path = $csv_path.'_'.$param_name;
						$csv_file_name.'_'.$param_name;
					}
					$i += 1;
				}
				// </>

				// do instancing a file object represents the CSV output
				$CSV_FILE_OBJ = fopen($csv_path, 'w');



				// print CSV header
				//echo 'Date/Time,';
				fwrite($CSV_FILE_OBJ, 'Date/Time,');

				$i = 1;
				foreach ($PARAM_SELECTION as $param_name) {
					if ($i == count($PARAM_SELECTION)) {
						//echo $param_name.'</br>';
						fwrite($CSV_FILE_OBJ, $param_name." \r\n");
					}
					else {
						//echo $param_name.',';
						fwrite($CSV_FILE_OBJ, $param_name.',');
					}
					$i += 1;
				}
				// </>

				// main loop for getting the data base entries and output
				while ($row = mysqli_fetch_assoc($ALL_DATA)) {
					//echo $row['Date_Time'].',';
					fwrite($CSV_FILE_OBJ, $row['Date_Time'].',');

					$i = 1;
					foreach ($PARAM_SELECTION as $param_name) {
						if ($i == count($PARAM_SELECTION)) {
							if (isset($_POST[$param_name])) {
								//echo $row[$param_name].'</br>';
								fwrite($CSV_FILE_OBJ, $row[$param_name]." \r\n");
							}
						}
						else {
							if (isset($_POST[$param_name])) {
								//echo $row[$param_name].',';
								fwrite($CSV_FILE_OBJ, $row[$param_name].",");
							}
						}
						$i += 1;
					}
				}
			}
		}
		fclose($CSV_FILE_OBJ);

		////////////////////////////////// CSV FILE DOWLOAD SECTION //////////////////////////////////
		echo '</br></br></br></br></br></br></br></br></br>';
		echo '<div class="download_text">';
		echo 'Your requested CSV-file has been created.</br>Please download the CSV-file.</br></br></br></br></br>';
		echo '</div>';
		echo '<form action=download.php?file="{$csv_path}">';
		//echo '<a class="btn" href=download.php?file="'.$csv_path.'" >DOWNLOAD TABLE</a>';
		echo '<button class="btn" style="center"><i class="fa fa-download"></i>Download CSV-file</button>';
		echo '</form>';

		?>
	</body>
</html>
