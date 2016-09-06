<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
</head>

<body style="font-family: 'Roboto', sans-serif;">
<?php

  include_once 'headerui.php';

  echo "<div class=\"container-fluid\">";
  echo "<div class=\"row\">";
  echo "<div class=\"container col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-1 main\">";
    echo "<div class=\"panel panel-primary\">";
      echo "<div class=\"panel-heading\">";
        echo "<h3>";
          echo "<b>". $_GET["header"] ."</b>";
          echo " <span class=\"glyphicon glyphicon-collapse-down\" data-toggle=\"collapse\" data-target=\"#displayurl\" aria-hidden=\"true\"></span>";
          echo "<div id=\"displayurl\" class=\"collapse\">";
            echo "<h5><span class=\"glyphicon glyphicon-chevron-right\" aria-hidden=\"true\"></span> ";
            echo $_GET["value"] ."</h5>";
          echo "</div>";
        echo "</h3>";
      echo "</div>";
    echo "</div>";

  require_once("db.php");
  $conn = new DB;
  $mysqli = $conn->getConnection();

  $command = "SELECT sql_cache h.site_id, s.site, url, hv.value FROM site AS s JOIN header ".
    "AS h, header_value AS hv, header_name AS hn WHERE hn.name = ? AND ".
    "hv.value = ? AND s.site_id = h.site_id AND h.header_name_id = ".
    "hn.header_name_id AND ".
    "h.header_value_id = hv.header_value_id ORDER BY s.site_id;";

  echo "<div class=\"table-responsive\">";
  echo "<table class=\"table table-striped\">";
    echo "<thead>";
      echo "<tr>";
        echo "<th>Rank</th>";
        echo "<th>Site</th>";
      echo "</tr>";
    echo "</thead>";
      echo "<tbody>";

  if ($stmt = $mysqli->prepare($command)) {
    $stmt->bind_param("ss", $_GET["header"],$_GET["value"]);
    $stmt->execute();
    $result = $stmt->get_result();

    while($row = $result->fetch_assoc()) {
      echo "<tr>";
        echo "<td>";
          echo "<h4>". $row['site_id'] ."</h4>";
        echo "</td>";

        echo "<td>";
          echo "<h4><a class=\"data-toggle=\"tooltip\" title=". $row['url'] ."\" href=\"site.php?site=". $row['site'] . "\">" . $row['site'] ."</a></h4>";
        echo "</td>";
      echo "</tr>";
    }
    echo "</tbody>";
    echo "</table>";
    echo "</div>";

    echo "</div>";
    echo "</div>";
    echo "</div>";
    $stmt->free_result();
    $stmt->close();
}

include_once 'footerui.php';
?>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</body>
</html>
