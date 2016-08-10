<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>

<?php
$mysqli = new mysqli("localhost", "root", "password", "headers");

if (mysqli_connect_errno()) {
    printf("Connect failed: %s\n", mysqli_connect_error());
    exit();
}

if ($_GET["value"] == 'NULL') {
	$command = "SELECT site, url FROM site as s WHERE s.code >= 0 AND ".
    "s.site_id NOT IN (SELECT s.site_id FROM site as s JOIN header as h, ".
    "header_value as hv, header_name as hn WHERE s.site_id = h.site_id ".
    "AND h.header_name_id = hn.header_name_id AND h.header_value_id = ".
    "hv.header_value_id AND hn.name = '') ORDER BY s.site_id;";

  $value = 'Not set';
} else {
  $command = "SELECT site, url FROM site as s JOIN header as h, header_value ".
    "as hv, header_name as hn WHERE (s.site_id = h.site_id AND ".
    "h.header_name_id = hn.header_name_id AND h.header_value_id = ".
    "hv.header_value_id AND hn.name = ? AND hv.value = ?) ".
    "ORDER BY s.site_id;";

  $value = $_GET["value"];
  $header = $_GET["header"];
}

echo "<br><br><br>";
echo "<nav class=\"navbar navbar-inverse navbar-fixed-top\">";
  echo "<div class=\"navbar-header\">";
    echo "<a class=\"navbar-brand\" href=\"#\">SecureHeaders Project</a>";
    echo "<ul class=\"nav navbar-nav\">";
      echo "<li class=\"active\"><a href=\"#\">Home</a></li>";
    echo "</ul>";
  echo "</div>";
echo "</nav>";

echo "<div class=\"container col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-1 main\">";
  echo "<div class=\"panel panel-primary\">";
    echo "<div class=\"panel-heading\">";
      echo "<h3><b>". $_GET["header"] . ": ". $value ."</b></h3>";
    echo "</div>";
  echo "</div>";

if ($stmt = $mysqli->prepare($command)) {
  if ($_GET["header"] != "NULL") {
    $stmt->bind_param("ss", $header,$value);
  }
  $stmt->execute();
  $result = $stmt->get_result();
  $fields_num = $result->num_rows;

  //echo "<table class=\"table table-hover\">";
  echo "<table class=\"table table-responsive\">";
    echo "<thead class=\"thead-inverse\">";
      echo "<tr>";
        echo "<th>site</th>";
        echo "<th>url</th>";
      echo "</tr>";
    echo "</thead>";
    echo "<tbody>";
  while($row = $result->fetch_assoc())
  {
      echo "<tr>";
        echo "<th>";
          echo "<a href=\"site.php?site=". $row['site'] ."\">". $row['site'] ."</a>";
        echo "</th>";
        echo "<td>";
          echo $row['url'];
          echo "</td>";
      echo "</tr>";
  }
  echo "</tbody>";
  echo "</table>";
  echo "</div>";
  $stmt->free_result();
  $stmt->close();
}

echo "<nav class=\"navbar navbar-default navbar-fixed-bottom\">";
echo "<div class=\"container\">";
echo "<p class=\"navbar-text\">An initiative of:
<a href=\"mailto:alexandre.fmenezes@owasp.org.br\">Alexandre Menezes</a> &
<a href=\"mailto:ricardo.iramar@owasp.org.br\">Ricardo Iramar</a></p>";
echo "</div>";
echo "</nav>";

$mysqli->close();
?>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
