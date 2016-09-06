<?php

  require_once("db.php");
  $conn = new DB;
  $mysqli = $conn->getConnection();

  $rows = array();
  $command = "SELECT hv.value as value, COUNT(*) as quantity FROM site as s ".
    "JOIN header as h, header_value as hv, header_name as hn WHERE ".
    "s.site_id = h.site_id AND h.header_name_id = hn.header_name_id AND ".
    "h.header_value_id = hv.header_value_id AND hn.name = ? GROUP BY ".
    "hv.value ORDER BY quantity DESC LIMIT ?";

  if ($stmt = $mysqli->prepare($command)) {
    $stmt->bind_param("ss", $_GET["header"],$_GET["limit"]);
    $stmt->execute();
    $result = $stmt->get_result();
    while($row = $result->fetch_assoc()) {
      $data_row = [ "\"". $row['value'] ."\"", $row['quantity']];
      array_push($rows, $data_row);
    }
  }

  if ($_GET["includenull"] == '1') {
    $command = "SELECT url, COUNT(*) as quantity FROM site as s WHERE ".
      "s.code >= 0 AND s.site_id NOT IN (SELECT s.site_id FROM site as s ".
      "JOIN header as h, header_value as hv, header_name as hn WHERE s.site_id ".
      "= h.site_id AND h.header_name_id = hn.header_name_id AND h.header_value_id = ".
      "hv.header_value_id AND hn.name = ?);";

    if ($stmt = $mysqli->prepare($command)) {
      $stmt->bind_param("s", $_GET["header"]);
      $stmt->execute();
      $result = $stmt->get_result();
      while($row = $result->fetch_assoc()) {
        $data_row = ["\"NULL\"", $row['quantity']];
        array_push($rows, $data_row);
      }
    }
  }
  $stmt->free_result();
  $stmt->close();

  print json_encode($rows, JSON_NUMERIC_CHECK);

?>
