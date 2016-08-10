<?php
function normalize_special_characters($str)
{
    # Quotes cleanup
    $str = ereg_replace(chr(ord("`")), "'", $str);    # `
    $str = ereg_replace(chr(ord("´")), "'", $str);    # ´
    $str = ereg_replace(chr(ord("„")), ",", $str);    # „
    $str = ereg_replace(chr(ord("`")), "'", $str);    # `
    $str = ereg_replace(chr(ord("´")), "'", $str);    # ´
    $str = ereg_replace(chr(ord("“")), "\"", $str);   # “
    $str = ereg_replace(chr(ord("”")), "\"", $str);   # ”
    $str = ereg_replace(chr(ord("´")), "'", $str);    # ´
    $str = ereg_replace(chr(147), "\"", $str);        # ´
    $str = ereg_replace(chr(148), "\"", $str);        # ´

    $unwantedArray = array('Š'=>'S', 'š'=>'s', 'Ž'=>'Z', 'ž'=>'z',
      'À'=>'A', 'Á'=>'A', 'Â'=>'A', 'Ã'=>'A',
      'Ä'=>'A', 'Å'=>'A', 'Æ'=>'A', 'Ç'=>'C',
      'È'=>'E', 'É'=>'E', 'Ê'=>'E', 'Ë'=>'E',
      'Ì'=>'I', 'Í'=>'I', 'Î'=>'I', 'Ï'=>'I',
      'Ñ'=>'N', 'Ò'=>'O', 'Ó'=>'O', 'Ô'=>'O',
      'Õ'=>'O', 'Ö'=>'O', 'Ø'=>'O', 'Ù'=>'U',
      'Ú'=>'U', 'Û'=>'U', 'Ü'=>'U', 'Ý'=>'Y',
      'Þ'=>'B', 'ß'=>'Ss', 'à'=>'a', 'á'=>'a',
      'â'=>'a', 'ã'=>'a', 'ä'=>'a', 'å'=>'a',
      'æ'=>'a', 'ç'=>'c', 'è'=>'e', 'é'=>'e',
      'ê'=>'e', 'ë'=>'e', 'ì'=>'i', 'í'=>'i',
      'î'=>'i', 'ï'=>'i', 'ð'=>'o', 'ñ'=>'n',
      'ò'=>'o', 'ó'=>'o', 'ô'=>'o', 'õ'=>'o',
      'ö'=>'o', 'ø'=>'o', 'ù'=>'u', 'ú'=>'u',
      'û'=>'u', 'ý'=>'y', 'ý'=>'y', 'þ'=>'b',
      'ÿ'=>'y' );
    $str = strtr($str, $unwantedArray);

    # Bullets, dashes, and trademarks
    $str = ereg_replace(chr(149), "&#8226;", $str);    # bullet •
    $str = ereg_replace(chr(150), "&ndash;", $str);    # en dash
    $str = ereg_replace(chr(151), "&mdash;", $str);    # em dash
    $str = ereg_replace(chr(153), "&#8482;", $str);    # trademark
    $str = ereg_replace(chr(169), "&copy;", $str);     # copyright mark
    $str = ereg_replace(chr(174), "&reg;", $str);      # registration mark

    return $str;
}

$con = mysql_connect("localhost","root","password");

if (!$con) {
  die('Could not connect: '. mysql_error());
}

mysql_select_db("headers", $con);

$result = mysql_query("SELECT header_value.value AS '". $_GET["header"]
  ."', COUNT(*) AS quantity FROM site JOIN header, header_value, ".
  "header_name WHERE site.site_id = header.site_id AND ".
  "header.header_name_id = header_name.header_name_id AND ".
  "header.header_value_id = header_value.header_value_id AND ".
  "header_name.name = '". $_GET["header"]
  ."' GROUP BY header_value.value ORDER BY quantity DESC LIMIT ".
  $_GET["limit"] .";");

$rows = array();
while($r = mysql_fetch_array($result)) {
    $row[0] = "\"". normalize_special_characters($r[0]) ."\"";
    $row[1] = $r[1];
    array_push($rows,$row);
}

if ($_GET["includenull"] == '1') {
	$result = mysql_query("SELECT url AS '". $_GET["header"]
    ."', COUNT(*) AS quantity FROM site WHERE site.code >= 0 AND ".
    "site.site_id NOT IN (SELECT site.site_id FROM site JOIN header".
    ", header_value, header_name WHERE site.site_id = header.site_id ".
    "AND header.header_name_id = header_name.header_name_id AND ".
    "header.header_value_id = header_value.header_value_id AND ".
    "header_name.name = '". $_GET["header"] ."');");

	$r = mysql_fetch_row($result);
	$row[0] = "\"NULL\"";
	$row[1] = $r[1];
	array_push($rows,$row);
}
print json_encode($rows, JSON_NUMERIC_CHECK);

mysql_free_result($result);
mysql_close($con);
?>
