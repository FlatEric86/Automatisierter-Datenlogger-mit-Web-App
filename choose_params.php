<!DOCTYPE html>
<html>
	<style>
		.base_plan {
			height: 550px;
			background-position: center;
			background-repeat: no-repeat;
			border-style: solid;
			display: block;
			margin-left:auto;
			margin-right:auto;
			width:48%;
			padding: 30px;
		}
		.font_1 {
			font-family: "Areal", "sans-serif";
			font-size: 1.5em;
		}
		.font_2 {
			font-family: "Areal", "sans-serif";
			font-size: 1em;
			text-align: justify;
		}

		.font_head {
			font-family: "Areal", "sans-serif";
			font-size: 1.5em;
			text-align: center;
		}

		.atb_logo {
			background-repeat: no-repeat;
			background-attachement: fixed;
		}

		.btn {
			background-color: Blue;
		       	border: none;
			text-align: center;
			color: white;
			padding: 12px 12px;
			coursor: pointer;
			font-size; 20px;
			margin: auto;
			display: block;
		}
		.btn:hover{
			backgroundcolor: RoyalBlue;
		}

		input[type="submit"]:hover{
			background: RoyalBlue;
		}

	</style>

	
	<body>
		<div>
			<p class="font_head"> Here you can define the data output by selecting the desired gage and it's gas measurements you want to study</p>
			</br></br></br>
		</div>
		<div>
			<img src='./graphics/dummerstorf_barn_base_plan.png' class="base_plan">
		</div>

		</br></br></br></br></br></br></br></br></br>
		<p><h3 class="font_1">Parameter and gage selection</h3></br></br></p>
			<form action=make_csv_table.php method="post">
				<div>
					<p class="font_2">
						In first section you can select the gage loacation.
						Please note, you can only choose one of each gages in a session.</br>
						For making a table of measurements of another gage, please just open a new session.
					</p>
					</br>
					<input type="radio" name="gage_id" value="gage_1">
					<label for="gage_id"> Gage 1 </label>
					<input type="radio" name="gage_id" value="gage_2">
					<label for="gage_id"> Gage 2 </label>
					<input type="radio" name="gage_id" value="gage_3">
					<label for="gage_id"> Gage 3 </label>
					<input type="radio" name="gage_id" value="gage_4">
					<label for="gage_id"> Gage 4 </label>
					<input type="radio" name="gage_id" value="gage_5">
					<label for="gage_id"> Gage 5 </label>
					<input type="radio" name="gage_id" value="gage_6">
					<label for="gage_id"> Gage 6 </label>
					<input type="radio" name="gage_id" value="gage_7">
					<label for="gage_id"> Gage 7 </label>
					<input type="radio" name="gage_id" value="gage_8">
					<label for="gage_id"> Gage 8 </label>
					<input type="radio" name="gage_id" value="gage_9">
					<label for="gage_id"> Gage 9 </label>
					<input type="radio" name="gage_id" value="gage_10">
					<label for="gage_id"> Gage 10 </label>
					<input type="radio" name="gage_id" value="gage_11">
					<label for="gage_id"> Gage 11 </label>
					<input type="radio" name="gage_id" value="gage_12">
					<label for="gage_id"> Gage 12 </label>
				</div>

				<div>
					</br></br>

				</div>
					<p class="font_2">
						Please select the measure parameters you want to get into the CSV-file output. 
                                                Note, it is recommend, that you select the parameter "Status" in any case. 
                                                This column has included the gage state. It may occour, 
                                                that the state refers to a timepoint is unequal to the base value "OK". 
                                                This can be induced by maintenance work or errors of the gage. 
                                                You should by using a filtering, discard all values of an row if the gage state is unequal to "OK" in it. 
					</p>
				<div>
					<input type="checkbox" name="H2O" value="H2O">
					<label>H2O</label>
					</br>
					<input type="checkbox" name="CO2" value="CO2">
					<label>CO2</label>
					</br>
					<input type="checkbox" name="N2O" value="N2O">
					<label>N2O</label>
					</br>
					<input type="checkbox" name="NH3" value="NH3">
					<label>NH3</label>
					</br>
					<input type="checkbox" name="CH4" value="CH4">
					<label>CH4</label>
					</br>
					<input type="checkbox" name="Cetan" value="Cetan">
					<label>Cetan</label>
					</br>
					<input type="checkbox" name="Ethanol" value="ethanol">
					<label>Ethanol</label>
					</br>
					<input type="checkbox" name="Formaldehyd" value="Formaldehyd">
					<label>Formaldehyd</label>
					</br>
					<input type="checkbox" name="Acetaldehyd" value="Acetaldehyd">
					<label>Acetaldehyd</label>
					</br>
					<input type="checkbox" name="Ameisensäure" value="Ameisensäure">
					<label>Ameisensäure</label>
					</br>
					<input type="checkbox" name="Essigsäure" value="Essigsäure">
					<label>Essigsäure</label>
					</br>
					<input type="checkbox" name="Milchsäure" value="Milchsäure">
					<label>Milchsäure</label>
					</br>
					<input type="checkbox" name="Status" value="Status">
					<label>Status</label>
				</div>

				<div>
					</br></br>
				</div>

				<div>
					<input class="btn" type="submit" value="submit file download request">
				</div>

				<div>
					</br></br></br></br></br>
				</div>

			</form> 
	</body>

</html>

