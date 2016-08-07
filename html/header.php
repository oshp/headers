<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>

<?php
echo "<div class=\"container\">";
echo "<h3><b>". $_GET["header"] ."</b></h3><br><br>";

$mysqli = new mysqli("localhost", "root", "password", "headers");

if (mysqli_connect_errno()) {
    printf("Connect failed: %s\n", mysqli_connect_error());
    exit();
}

$command = "SELECT site, url, hv.value FROM site AS s JOIN header AS h".
  ", header_value AS hv, header_name AS hn WHERE hn.name = ? AND ".
  "s.site_id = h.site_id AND h.header_name_id = hn.header_name_id AND ".
  "h.header_value_id = hv.header_value_id;";

echo "<table class=\"table table-hover\">";
echo "<thead>";
echo "<tr>";
echo "<td><b>site</b></td>";
echo "<td><b>url</b></td>";
echo "<td><b>value</b></td>";
echo "</tr>";
echo "</thead>";

if ($stmt = $mysqli->prepare($command)) {
  $stmt->bind_param("s", $_GET["header"]);
  $stmt->execute();
  $result = $stmt->get_result();

  while($row = $result->fetch_assoc())
  {
      echo "<tbody>";
      echo "<tr>";
          echo "<td>";
          echo "<a href=\"site.php?site=". $row['site'] . "\">" . $row['site'] ."</a>";
          echo "</td>";

          echo "<td>";
          echo $row['url'];
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
$mysqli->close();
?>
