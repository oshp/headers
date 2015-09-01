<?php
echo $_GET["site"] . "<br><br>";

$link = mysql_connect('localhost', 'root', 'password');
if (!$link) {
    die('Não foi possível conectar: ' . mysql_error());
}

if (!mysql_select_db('headers', $link)) {
    echo 'Não foi possível selecionar o banco de dados';
    exit;
}

$sql = 'SELECT url, header_name.name, header_value.value FROM site JOIN header, header_value, header_name WHERE site = \'' . $_GET["site"] . '\' AND site.site_id = header.site_id AND header.header_name_id = header_name.header_name_id AND header.header_value_id = header_value.header_value_id;';
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
    foreach($row as $key => $cell) {
        echo "<td>";
                if ($cell === NULL) {
                  echo "NULL";
                } else {
					if ($key == 1) {
						echo "<a href=\"header.php?header=$cell\">$cell</a>";
					} else {
						echo "$cell";
					}
                }
        echo "</td>";
    }
    echo "</tr>\n";
}

mysql_free_result($result);
mysql_close($link);
?>