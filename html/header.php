<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>

<?php
echo "<nav class=\"navbar navbar-inverse navbar-fixed-top\">";
echo "<div class=\"navbar-header\">";
echo "<a class=\"navbar-brand\" href=\"#\">SecureHeaders Project</a>";
echo "<ul class=\"nav navbar-nav\">";
echo "<li class=\"active\"><a href=\"#\">Home</a></li>";
echo "</ul>";
echo "</div>";
echo "</nav>";

echo "<br><br><br>";
echo "<div class=\"container col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-1 main\">";
  echo "<div class=\"panel panel-primary\">";
    echo "<div class=\"panel-heading\">";
      echo "<h3><b>". $_GET["header"] ."</b></h3>";
    echo "</div>";
  echo "</div>";

$mysqli = new mysqli("localhost", "root", "password", "headers");

if (mysqli_connect_errno()) {
    printf("Connect failed: %s\n", mysqli_connect_error());
    exit();
}

$command = "SELECT site, url, hv.value FROM site AS s JOIN header AS h".
  ", header_value AS hv, header_name AS hn WHERE hn.name = ? AND ".
  "s.site_id = h.site_id AND h.header_name_id = hn.header_name_id AND ".
  "h.header_value_id = hv.header_value_id ORDER BY s.site_id;";

echo "<div class=\"table-responsive\">";
echo "<table class=\"table table-hover\">";
  echo "<thead>";
    echo "<tr>";
      echo "<th>site</th>";
      echo "<th>url</th>";
      echo "<th>value</th>";
    echo "</tr>";
  echo "</thead>";

if ($stmt = $mysqli->prepare($command)) {
  $stmt->bind_param("s", $_GET["header"]);
  $stmt->execute();
  $result = $stmt->get_result();

  echo "<tbody>";
  while($row = $result->fetch_assoc())
  {
    echo "<tr>";
      echo "<th>";
        echo "<a href=\"site.php?site=". $row['site'] . "\">" . $row['site'] ."</a>";
      echo "</th>";
      echo "<td>";
        echo $row['url'];
      echo "</td>";
      echo "<td>";
        echo $row['value'];
      echo "</td>";
    echo "</tr>";
  }
  echo "</tbody>";
  echo "</table>";
  echo "</div>";
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
