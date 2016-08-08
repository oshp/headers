<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=UTF-8">
		<title>Headers</title>
		<script type="text/javascript" src="//code.jquery.com/jquery-1.9.1.js"></script>
		<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
		<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
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

		</script>
	</head>
	<body>
		<script src="https://code.highcharts.com/highcharts.js"></script>
		<script src="https://code.highcharts.com/highcharts-3d.js"></script>
		<script src="https://code.highcharts.com/modules/exporting.js"></script>

		<?php
		echo "<nav class=\"navbar navbar-inverse navbar-fixed-top\">";
		echo "<div class=\"navbar-header\">";
		echo "<a class=\"navbar-brand\" href=\"#\">SecureHeaders Project</a>";
		echo "</div>";
		echo "</nav>";
		echo "<br><br><br>";

		echo "<div class=\"container\">";
		?>

		<div id="container" style="height: 400px" data-highcharts-chart="0"></div>

Header: <select name="header" form="header" value="content-type">
<?php
$con = mysql_connect("localhost","root","password");

if (!$con) {
  die('Could not connect: ' . mysql_error());
}

mysql_select_db("headers", $con);

$result = mysql_query("SELECT name FROM headers.header_name ORDER BY name;");
if (!$result) {
    echo 'Could not run query: ' . mysql_error();
    exit;
}
if (mysql_num_rows($result) > 0) {
    while ($row = mysql_fetch_array($result)) {
	if ($_GET["header"] == $row[0]) {
		echo "<option value=\"" . $row[0] . "\" selected>"  . $row[0] . "</option>";
	} else {
		echo "<option value=\"" . $row[0] . "\">"  . $row[0] . "</option>";
	}
    }
}
mysql_free_result($result);
mysql_close($con);
?>
</select>
<br>
<form action="index.php" method="get" id="header">
  Top headers value:
<select name="limit" form="header">
  <option<?php if ( $_GET["limit"] == 3 ) { echo ' selected'; } ?>>3</option>
  <option<?php if ( $_GET["limit"] == 5 ) { echo ' selected'; } ?>>5</option>
  <option<?php if ( $_GET["limit"] == 10 ) { echo ' selected'; } ?>>10</option>
  <option<?php if ( $_GET["limit"] == 20 ) { echo ' selected'; } ?>>20</option>
  <option<?php if ( $_GET["limit"] == 50 ) { echo ' selected'; } ?>>50</option>
  <option<?php if ( $_GET["limit"] == 100 ) { echo ' selected'; } ?>>100</option>
</select><br>
  Include NULL headers<input type="checkbox" id="includenull" name="includenull" value="1"<?php if ( $_GET["includenull"] == 1 ) { echo ' checked'; } ?>><br>
  <input type="submit" value="Submit">
</form>

  <?php
		echo "</div>";
		echo "<nav class=\"navbar navbar-default navbar-fixed-bottom\">";
		echo "<div class=\"container\">";
		echo "<p class=\"navbar-text\">An initiative of:
		<a href=\"mailto:alexandre.fmenezes@owasp.org.br\">Alexandre Menezes</a> &
		<a href=\"mailto:ricardo.iramar@owasp.org.br\">Ricardo Iramar</a></p>";
		echo "</div>";
		echo "</nav>";
	?>

	</body>
</html>
