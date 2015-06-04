<h1>HTTP response headers</h1>
HTTP headers are well known and also despised. Seeking the balance between usability and security developers implement functionality through the headers that can make your more versatile or secure application.<br>
But in practice how the headers are being implemented? What sites follow the best implementation practices? Big companies, small, all or none?<br>
<p>
<h3>headers.py</h3>
Python script to get all response headers from Alexa top sites file and store in a MySQL database.<br>
Syntax: $ python headers.py (Alexa csv top sites file) (Number of concurrent threads)<br>
Eg.: $ python headers.py top-1k.csv 200<br>
</p>
<p>
<h3>headers.sql</h3>
MySQL database scheme exported with the command below:<br>
$ mysqldump -u root -p --no-data headers header header_name header_value site > headers.sql<br>
To import you can use this command:<br>
$ mysql -u username -p headers < headers.sql<br>
</p>
<p>
<h3>top-1k.csv</h3>
Just an Alexa top sites file example with 1000 records.<br>
</p>
<p>
<h3>www/</h3>
PHP pages with Highcharts graphics.<br>
Eg.:<br>
<img src="strict-transport-security.png"><br>
</p>
