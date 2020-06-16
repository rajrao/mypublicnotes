$filePath = "c:\blah.json";

$fileContents = Get-Content $filePath -ErrorAction Stop -Raw;
$json = ConvertFrom-Json $fileContents;

#null out partition property on entities
$($json.entities).partitions = $null;

#convert back to string
$jsonString = ConvertTo-Json $json -Compress -Depth 100

$jsonString
