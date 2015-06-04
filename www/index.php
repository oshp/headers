<!DOCTYPE HTML>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Headers</title>
        <script type="text/javascript" src="js/jquery-1.11.1.min.js"></script>
        <script type="text/javascript">
        $(document).ready(function() {
            var options = {
                chart: {
                    renderTo: 'container',
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false
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
                                return '<b>'+ this.point.name +'</b> = '+ this.percentage.toFixed(2) +' %';
                            }
                        }
                    }
                },
                series: [{
                    type: 'pie',
                    name: 'Browser share',
                    data: []
                }]
            }
           
            $.getJSON("data.php?header=<?php echo $_GET["header"] ?>&limit=<?php if ( $_GET["limit"] == '' ) { echo 10; } else { echo $_GET["limit"]; } ?>&includenull=<?php echo $_GET["includenull"] ?>", function(json) {
                options.series[0].data = json;
                chart = new Highcharts.Chart(options);
            });
           
           
           
        });  
        </script>
        <script src="js/highcharts.js"></script>
        <script src="js/modules/exporting.js"></script>
    </head>
    <body>
        <div id="container" style="min-width: 400px; height: 400px; margin: 0 auto"></div>


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
<form action="." method="get" id="header">
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

</body>
</html>
