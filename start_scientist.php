<!DOCTYPE>
<html>
	<head>
		<meta charset="utf-8"/>
		<title>
			LOGIN
		</title>
		<style>
			.fehler {
				font-family: Arial;
				font-size: 20px;
				color: red;
				text-align: center;
				border: 1px;
				border-style: solid;
			}
			label {
				display: block;
			}
			.CenterBody {
                                width: 15%;
                                margin-left: auto;
                                margin-right: auto;
                                vertical-align: center;
                                border: 1px solid #73AD21;
				background-color: #f2f2f2;
                                padding: 100px;
                        }

			.grumpy_cat{
				display: flex;
				justify-content: center;
			}

			.text_loc{
				display: flex;
				justify-content: center;
				padding: 10px;
			}

			.insert_box{
				display: flex;
			}

			.insert_div{
				padding: 5px;
			}

			.loc_login{
				display: flex;
				justify-content: center;
				padding: 20px;
			}

			.font{
				font-family: Arial;
			}

		</style>
	</head>
	<body>
		<div>
			</br></br></br></br>
		</div>
		<div class="CenterBody">
			<?php
				if (isset($_GET['f'])) {
					echo '<div class="grumpy_cat">';
                               		echo '<img src="./graphics/grumpy-cat.jpg" style="width: 245px">';
                                	echo '</div>';
                                	echo '<div>';
                                	echo "<p class='fehler'>Permission denied!</p>";
                                	echo '</div>';
				}
			?>
			<form method="post" action="scientist_login.php">
				<div class="insert_div">
					<div class="grumpy_cat">
						<label class="font" for="text">Please insert your user name:</label>
					</div>
					<div class="text_loc">
						<input type="text" name="name" size="31" />
					</div>
				</div>

				<div class="insert_div">
					<div class="grumpy_cat">
						<label class="font" for="passwort">Please insert your password:</label>
					</div>
					<div class="text_loc">
						<input type="password" name="passwort" size="31" />
					</div>
					<div class="loc_login">
						<input type="submit" value="Login" />
					</div>
				</div>
			</form>
		</div>
	</body>
<html>
