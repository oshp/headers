<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>SecureHeaders Project</title>
	<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
</head>

<body style="font-family: 'Roboto', sans-serif;">
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
		      echo "<li class=\"active\"><a href=\"/\">Home</a></li>";
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

						echo "<div class=\"col-xs-12 col-sm-12 col-md-10 col-sm-offset-2 col-sm-offset-1 col-md-offset-1 placeholder\" id=\"container\" data-highcharts-chart=\"0\"></div>";
					echo "</div>";

					echo "<nav class=\"navbar navbar-default\">";
					echo "<div class=\"container-fluid col-xs-12 col-sm-9 col-md-8 col-sm-offset-3\">";

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
						echo "<div class=\"form-group input-group\">";
						echo "<input type=\"text\" value=\"\" placeholder=\"Insert an HTTP Header\" id=\"header\" name=\"header\" form=\"header\" class=\"form-control\" value=\"content-type\" aria-describedby=\"headername\">";
							echo "<span type=\"button\" class=\"btn btn-default dropdown-toggle input-group-addon\"  data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">";
								echo "<span class=\"caret\"></span>";
							echo "</span>";
							echo "<ul class=\"dropdown-menu\" id=\"headername\">";

							require_once("db.php");
							$conn = new DB;
							$mysqli = $conn->getConnection();

							$command = "SELECT sql_cache name FROM header_name ORDER BY name;";
							if ($stmt = $mysqli->prepare($command)) {
							  $stmt->execute();
							  $result = $stmt->get_result();
							  while($row = $result->fetch_assoc()) {
							    echo "<li data-value=\"". $row['name'] . "\"><a href=\"#\">"  . $row['name'] . "</a></li>";
							  }
							  $stmt->free_result();
							  $stmt->close();
							}

						echo "</ul>";
						echo "</div>";

						echo "<div class=\"form-group input-group\">";
							echo "<input type=\"text\" size=\"4\" value=\"3\" id=\"limit\" name=\"limit\" form=\"header\" class=\"form-control\" aria-describedby=\"limitvalue\">";
							echo "<span type=\"button\" class=\"btn btn-default dropdown-toggle input-group-addon\"  data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">";
								echo "<span class=\"caret\"></span>";
							echo "</span>";
							echo "<ul class=\"dropdown-menu\" id=\"limitvalue\">";
								echo "<li data-value=\"5\"><a href=\"#\">5</a></li>";
								echo "<li data-value=\"10\"><a href=\"#\">10</a></li>";
								echo "<li data-value=\"20\"><a href=\"#\">20</a></li>";
								echo "<li data-value=\"50\"><a href=\"#\">50</a></li>";
								echo "<li data-value=\"100\"><a href=\"#\">100</a></li>";
							echo "</ul>";
						echo "</div>";

						echo "<div class=\"form-group\">";
								echo "<select class=\"dropdown form-control\" id=\"includenull\" name=\"includenull\">";
									echo "<option value=\"0\">Not null</option>";
									echo "<option value=\"1\">Include null</option>";
								echo "</select>";
						echo "</div>";

						echo " <button type=\"submit\" class=\"btn btn-primary form-control\">Submit</button>";
						echo "</form>";
						echo "</div>";

						echo "</div>";
						echo "</nav>";

				echo "</div>";
		echo "</div>";
	echo "</div>";

	include_once 'footerui.php';

?>
</body>
</html>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="https://code.highcharts.com/highcharts.js"></script>
<script async src="https://code.highcharts.com/modules/exporting.js"></script>
<script type="text/javascript">
	$.getJSON('data.php?header=<?php echo $_GET["header"] ?>&limit=<?php if ( $_GET["limit"] == '' ) { echo 10; } else { echo $_GET["limit"]; } ?>&includenull=<?php echo $_GET["includenull"] ?>', function (data) {
    $('#container').highcharts({
			chart: {
				type: 'pie',
				plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false },
			title: {
        text: 'Header <?php echo $_GET["header"] ?>' },
        tooltip: {
			  formatter: function() {
				return this.point.name + '<br><b>' + this.point.y + ' (' + this.percentage.toFixed(2) + '%)</b>'; } },
      plotOptions: {
        pie: {
					allowPointSelect: true,
          cursor: 'pointer',
					dataLabels: {
					enabled: false },
				  showInLegend: true,
					point: {
						events: {
							click: function () {
								location.href = 'headers.php?header=<?php echo $_GET["header"] ?>&value=' + encodeURIComponent(this.name.substring(1, this.name.length-1)); }
							} } } },
				credits: {
					enabled: false },
        series: [{
					name: 'Header',
          type: 'pie',
					colorByPoint: true,
          data: data }]
			});
	});

	$("#headername").on("click", "a", function(e){
		e.preventDefault();
		var $this = $(this).parent();
		$("[name=header]").val($this.data("value"));
	})

	$("#limitvalue").on("click", "a", function(e){
		e.preventDefault();
		var $this = $(this).parent();
		$("#limit").val($this.data("value"));
	})

	$.urlParam = function(name){
		var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
		return results[1] || 0;
	}

	if ($.urlParam('header') != 'Insert an HTTP Header') {
		$('[name=header]').val($.urlParam('header'));
	}
	if ($.urlParam('includenull') == 1) {
		$('#includenull').val(1);
	}
	if ($.urlParam('limit') != 'Top headers value') {
		$('#limit').val($.urlParam('limit'));
	}

	</script>
