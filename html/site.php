<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
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
echo "<div class=\"container\">";
echo "<div class=\"panel panel-primary\">";
  echo "<div class=\"panel-heading\">";
    echo "<h3><b>".$_GET["site"] . "</b></h3>";
  echo "</div>";
echo "</div>";

$mysqli = new mysqli("localhost", "root", "password", "headers");

if (mysqli_connect_errno()) {
    printf("Connect failed: %s\n", mysqli_connect_error());
    exit();
}

$command = "SELECT url, name, value FROM site as s JOIN header as h, ".
"header_value as hv, header_name as hn WHERE site = ? AND s.site_id = ".
"h.site_id AND h.header_name_id = hn.header_name_id AND h.header_value_id ".
"= hv.header_value_id";
if ($stmt = $mysqli->prepare($command)) {
  $stmt->bind_param("s", $_GET["site"]);
  $stmt->execute();
  $result = $stmt->get_result();

  $fields_num = $result->num_rows;
  echo "<table class=\"table table-hover\">";
  echo "<thead>";
  echo "<tr>";
  echo "<td><b>url</b></td>";
  echo "<td><b>name</b></td>";
  echo "<td><b>value</b></td>";
  echo "</tr>";
  echo "</thead>";
  while($row = $result->fetch_assoc())
  {
      echo "<tbody>";
      echo "<tr>";
          echo "<td>";
          echo $row['url'];
          echo "</td>";

          echo "<td>";
          echo "<a href=\"header.php?header=". $row['name'] ."\">". $row['name'] ."</a>";
          echo "</td>";

          echo "<td>";
          echo $row['value'];
          echo "</td>";
      echo "</tr>";
  }
  echo "</tbody>\n";
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
