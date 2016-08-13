<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>

<body>
<?php
  $mysqli = new mysqli("localhost", "root", "password", "headers");
  if (mysqli_connect_errno()) {
      printf("Connect failed: %s\n", mysqli_connect_error());
      exit();
  }

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
      echo "<li><a href=\"/secureheaders\">Home</a></li>";
      echo "<li><a href=\"https://www.owasp.org/index.php/OWASP_Secure_Headers_Project\">About</a></li>";
    echo "</ul>";
  echo "</div>";
echo "</div>";
echo "</nav>";

echo "<div class=\"container-fluid\">";
echo "<div class=\"row\">";
echo "<div class=\"container col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-1 main\">";
  echo "<div class=\"panel panel-primary\">";
    echo "<div class=\"panel-heading\">";
      echo "<h3>";
        echo "<b>". $_GET["site"] ."</b>";
        echo " <span class=\"glyphicon glyphicon-collapse-down\" data-toggle=\"collapse\" data-target=\"#displayurl\" aria-hidden=\"true\"></span>";
        echo "<div id=\"displayurl\" class=\"collapse\">";
          echo "<h5><span class=\"glyphicon glyphicon-chevron-right\" aria-hidden=\"true\"></span> ";
            $geturl = "SELECT sql_cache distinct url FROM site as s JOIN header as h, ".
            "header_value as hv, header_name as hn WHERE site = ? AND s.site_id = ".
            "h.site_id AND h.header_name_id = hn.header_name_id AND h.header_value_id ".
            "= hv.header_value_id";
            if ($stmt = $mysqli->prepare($geturl)) {
              $stmt->bind_param("s", $_GET["site"]);
              $stmt->execute();
              $result = $stmt->bind_result($uri);
              $stmt->fetch();
              echo $uri ."</h5>";
              $stmt->free_result();
            }
        echo "</div>";
      echo "</h3>";
    echo "</div>";
  echo "</div>";

$command = "SELECT sql_cache name, value FROM site as s JOIN header as h, ".
"header_value as hv, header_name as hn WHERE site = ? AND s.site_id = ".
"h.site_id AND h.header_name_id = hn.header_name_id AND h.header_value_id ".
"= hv.header_value_id ORDER BY hn.name";
if ($stmt = $mysqli->prepare($command)) {
  $stmt->bind_param("s", $_GET["site"]);
  $stmt->execute();
  $result = $stmt->get_result();

  $fields_num = $result->num_rows;
  echo "<div class=\"table-responsive\">";
  echo "<table class=\"table table-striped\">";
    echo "<thead>";
      echo "<tr>";
        echo "<th>name</th>";
        echo "<th>value</th>";
      echo "</tr>";
    echo "</thead>";
  echo "<tbody>";
  while($row = $result->fetch_assoc())
  {
      echo "<tr>";
          echo "<td>";
            echo "<h4 id=\"headername\">". $row['name'] ."</h4>";
          echo "</td>";

          echo "<td>";
            echo "<a href=\"header.php?header=". $row['name'] ."&value=". $row['value'] ."\"><h4>". $row['value'] ."</h4></a>";
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

echo "<nav class=\"navbar navbar-default navbar-static-bottom\">";
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
</body>
</html>
