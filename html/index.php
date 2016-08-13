<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>SecureHeaders Project</title>
	<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>

<body>
	<?php
	  echo "<br><br><br>";
		echo "<nav class=\"navbar navbar-inverse navbar-fixed-top\">";
		echo "<div class=\"container-fluid\">";
		  echo "<div class=\"navbar-header\">";
		    echo "<button type=\"button\" class=\"navbar-toggle collapsed\" data-toggle=\"collapse\" data-target=\"#navbar\" aria-expanded=\"false\" aria-controls=\"navbar\">";
		      echo "<span class=\"sr-only\">Toggle navigation</span>";
		      echo "<span class=\"icon-bar\"></span>";
		      echo "<span class=\"icon-bar\"></span>";
		      echo "<span class=\"icon-bar\"></span>";
		    echo "</button>";
		    echo "<a class=\"navbar-brand\" href=\"#\">SecureHeaders</a>";
		  echo "</div>";
		  echo "<div id=\"navbar\" class=\"navbar-collapse collapse\">";
		    echo "<ul class=\"nav navbar-nav navbar-right\">";
		      echo "<li class=\"active\"><a href=\"/secureheaders\">Home</a></li>";
		      echo "<li><a href=\"https://www.owasp.org/index.php/OWASP_Secure_Headers_Project\">About</a></li>";
		    echo "</ul>";
		  echo "</div>";
		echo "</div>";
		echo "</nav>";

		echo "<div class=\"container-fluid\">";
			echo "<div class=\"row\">";
				echo "<div class=\"container col-sm-9 col-sm-offset-1 col-md-10 col-md-offset-1 main\">";

				  # highcharts
				  echo "<div class=\"row img-responsive placeholders\">";
						echo "<div class=\"col-xs-12 col-sm-8 col-sm-offset-2 placeholder\" id=\"container\" data-highcharts-chart=\"0\"></div>";
					echo "</div>";

					echo "<nav class=\"navbar navbar-default\">";
					echo "<div class=\"container-fluid col-xs-12 col-sm-7 col-sm-offset-3\">";

					echo "<div class=\"navbar-header\">";
      			echo "<button type=\"button\" class=\"collapsed navbar-toggle\" data-toggle=\"collapse\" data-target=\"#index-navbar-collapse-1\" aria-expanded=\"false\">";
        			echo "<span class=\"sr-only\">Toggle navigation</span>";
        			echo "<span class=\"icon-bar\"></span>";
        			echo "<span class=\"icon-bar\"></span>";
        			echo "<span class=\"icon-bar\"></span>";
      			echo "</button>";
      		echo "<a href=\"#\" class=\"navbar-brand\">Search:</a>";
    			echo "</div>";

					echo "<div class=\"collapse navbar-collapse\" id=\"index-navbar-collapse-1\">";
					echo "<form action=\"index.php\" method=\"get\" id=\"header\" class=\"form-inline navbar-form\" role=\"form\">";
						echo "<div class=\"form-group\">";
								echo "<select class=\"dropdown form-control\" name=\"header\" form=\"header\" value=\"content-type\">";
									echo "<option>Select an HTTP Header</option>";

							$con = mysql_connect("localhost","root","password");
							if (!$con) {
							  die('Could not connect: ' . mysql_error());
							}
							mysql_select_db("headers", $con);
							$result = mysql_query("SELECT sql_cache name FROM header_name ORDER BY name;");
							if (!$result) {
							    echo 'Could not run query: ' . mysql_error();
							    exit;
							}
							if (mysql_num_rows($result) > 0) {
								while ($row = mysql_fetch_array($result)) {
									if ($_GET["header"] == $row[0]) {
										echo "<option value=\"". $row[0] . "\" selected>"  . $row[0] . "</option>";
									} else {
										echo "<option value=\"". $row[0] . "\">"  . $row[0] . "</option>";
									}
								}
							}
							mysql_free_result($result);
							mysql_close($con);

								echo "</select>";
						echo "</div>";

						echo "<div class=\"form-group\">";
								echo "<select class=\"dropdown form-control\" id=\"limit\" name=\"limit\" form=\"header\">";
									echo "<option>Top headers value</option>";
									echo "<option>3</option>";
									echo "<option>5</option>";
									echo "<option>10</option>";
									echo "<option>20</option>";
									echo "<option>50</option>";
									echo "<option>100</option>";
								echo "</select>";
						echo "</div>";

						echo "<div class=\"form-group\">";
								echo "<select class=\"dropdown form-control\" id=\"includenull\" name=\"includenull\">";
									echo "<option value=\"0\">Not null</option>";
									echo "<option value=\"1\">Include null</option>";
								echo "</select>";
						echo "</div>";

						echo " <button type=\"submit\" class=\"btn btn-primary\">Submit</button>";
						echo "</form>";
						echo "</div>";

						echo "</div>";
						echo "</nav>";

				echo "</div>";
		echo "</div>";
	echo "</div>";

	echo "<nav class=\"navbar navbar-default navbar-static-bottom\">";
		echo "<div class=\"container\">";
			echo "<p class=\"navbar-text\">An initiative of:
				<a href=\"mailto:alexandre.fmenezes@owasp.org.br\">Alexandre Menezes</a> &
				<a href=\"mailto:ricardo.iramar@owasp.org.br\">Ricardo Iramar</a></p>";
		echo "</div>";
	echo "</nav>";
	?>
</body>
</html>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="https://code.highcharts.com/highcharts.js"></script>
<script src="https://code.highcharts.com/highcharts-3d.js"></script>
<script src="https://code.highcharts.com/modules/exporting.js"></script>
<script type="text/javascript">
	$.getJSON('data.php?header=<?php echo $_GET["header"] ?>&limit=<?php if ( $_GET["limit"] == '' ) { echo 10; } else { echo $_GET["limit"]; } ?>&includenull=<?php echo $_GET["includenull"] ?>', function (data) {
    $('#container').highcharts({
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45,
                beta: 0
            }
        },
        title: {
            text: 'Header <?php echo $_GET["header"] ?>'
        },
        tooltip: {
		formatter: function() {
			return '<b>'+ this.point.name +'</b> = '+ this.point.y;
		}
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 35,
	                point: {
	                    events: {
	                        click: function () {
	                            location.href = 'headers.php?header=<?php echo $_GET["header"] ?>&value=' + encodeURIComponent(this.name.substring(1, this.name.length-1));
	                        }
	                    }
	                },
                        dataLabels: {
                            enabled: true,
                            color: '#000000',
                            connectorColor: '#000000',
                            formatter: function() {
                                return '<b>'+ this.point.name.substring(0, 100) +'</b> = '+ this.percentage.toFixed(2) +' %';
                            }
                        }
            }
        },
				credits: {
            enabled: false
        },
        series: [{
            type: 'pie',
            name: 'Headers',
            data: data
        }]
    });
	});

	$.urlParam = function(name){
		var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
		return results[1] || 0;
	}

	if ($.urlParam('includenull') == 1) {
		$('#includenull').val(1);
	}
	if ($.urlParam('limit') != 'Top headers value') {
		$('#limit').val($.urlParam('limit'));
	}

	</script>
