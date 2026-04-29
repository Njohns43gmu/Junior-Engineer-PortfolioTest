for($i = 1; $i -lt 10; $i++){
    Write-Host "The current number is $i"
}
$data = Import-Csv .\TextOutput\selection.csv
$selectedColumns = $data | Select-Object Age, Email
$filtereddata = $data | Where-Object {$_.Age -gt 25} | ForEach-Object {
    Write-Output $_
}
Write-Output $filtereddata
Out-File -FilePath .\TextOutput\output.txt -InputObject $filtereddata
Write-Host "Data has been processed"