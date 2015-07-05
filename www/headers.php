<?php
$link = mysql_connect('localhost', 'root', 'password');
if (!$link) {
    die('Não foi possível conectar: ' . mysql_error());
}

if (!mysql_select_db('headers', $link)) {
    echo 'Não foi possível selecionar o banco de dados';
    exit;
}

if ($_GET["value"] == 'NULL') {
	$sql    = 'SELECT site, url FROM site WHERE site.code >= 0 AND site.site_id NOT IN (SELECT site.site_id FROM site JOIN header, header_value, header_name WHERE site.site_id = header.site_id AND header.header_name_id = header_name.header_name_id AND header.header_value_id = header_value.header_value_id AND header_name.name = \'' . mysql_real_escape_string($_GET["header"]) . '\') ORDER BY site.site_id;';
} else {
	$sql    = 'SELECT site, url, header_value.value AS \'' . mysql_real_escape_string($_GET["header"]) . '\' FROM site JOIN header, header_value, header_name WHERE site.site_id = header.site_id AND header.header_name_id = header_name.header_name_id AND header.header_value_id = header_value.header_value_id AND header_name.name = \'' . mysql_real_escape_string($_GET["header"]) . '\' AND header_value.value = \'' . mysql_real_escape_string($_GET["value"]) . '\' ORDER BY site.site_id;';
}

$result = mysql_query($sql, $link);

if (!$result) {
    echo "Erro do banco de dados, não foi possível consultar o banco de dados\n";
    echo 'Erro MySQL: ' . mysql_error();
    exit;
}

$fields_num = mysql_num_fields($result);

echo "<table border='1'><tr>";
// printing table headers
for($i=0; $i<$fields_num; $i++)
{
    $field = mysql_fetch_field($result);
    echo "<td>{$field->name}</td>";
}
echo "</tr>\n";
// printing table rows
while($row = mysql_fetch_row($result))
{
    echo "<tr>";
    // $row is array... foreach( .. ) puts every element
    // of $row to $cell variable
    foreach($row as $cell) {
        echo "<td>";
                if ($cell === NULL) {
                  echo "NULL";
                } else {
                  echo "$cell";
                }
        echo "</td>";
    }
    echo "</tr>\n";
}

mysql_free_result($result);
mysql_close($link);
?>

