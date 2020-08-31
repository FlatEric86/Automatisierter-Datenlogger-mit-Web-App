<html>
	<head>
		<meta name="viewport" content="width=1024" />

	<title>
		Messergebnisse
	</title>
	</head>
	<style>
		body{
			background-color: #dbdbdb;
		}	
		.style_class_headline {
		background: backgroundcolor="blue"
		}
		.font_{
			font-family: Arial;
			font-size: 35px;
			text-decoration: underline;
			color: DarkGreen;
		}

		.font_headline{
			font-family: Arial;
			font-size: 50px;
			text-align: center;
		}
	</style>
	<body>
		<p class="font_headline"></br>Gas concentration measurements of the last 2 weeks.</p></br>
		<p>If there are no graphics or not all graphics of all gages, it may be, that the backend is still
		   in progress to rendering these graphics.
	           Please refresh this site in 30 seconds. If the Problem persists, please contact the admin.

		<?php

		$chartsDir = "./CHARTS";
		#$chartsDir = "/media/sql_db_at_usb/WEBAPP/CHARTS";

		$dict = ['gage_1'=>'Gage location 1',
		 	'gage_2'=>'Gage location 2',
			'gage_3'=>'Gage location 3',
			'gage_4'=>'Gage location 4',
			'gage_5'=>'Gage location 5',
			'gage_6'=>'Gage location 6',
			'gage_8'=>'Gage location 7',
			'gage_9'=>'Gage location 8',
			'gage_10'=>'Gage location 9',
			'gage_11'=>'Gage location 11',
			'gage_12'=>'Gage location 12',
		];


		if (is_dir($chartsDir)) {
			$sub_dirs = scanDir($chartsDir);
			foreach ($sub_dirs as $sub_dir) {
				if ($sub_dir != '.' and $sub_dir != '..') {
					// print a headline 
					echo '<p class="font_">'.$dict[$sub_dir].'</p>';
					$Files = scanDir($chartsDir.'/'.$sub_dir);
					foreach ($Files as $file) {
						if ($file != '.' and $file != '..') {
							#echo $chartsDir.'/'.$sub_dir.'/'. $file.'</br>';
							$path = $chartsDir.'/'.$sub_dir.'/'.$file;
							echo '<div>';
							echo "<img src=".$path.">";
							echo "</div>";
						}
					}
				}
			}
		}
		?>
	</body>
</html>

