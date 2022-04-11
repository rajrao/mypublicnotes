

```
Login-PowerBI | Out-Null

$WorkspaceObject = (Get-PowerBIWorkspace -Name "Workspace Name Here")
$datasets = Get-PowerBIDataset -WorkspaceId $WorkspaceObject.Id

$refreshSchedules =  New-Object System.Collections.ArrayList

foreach ($dataset in $datasets)
{
    if ($dataset.IsRefreshable)
    {
        $ApiUrl = "groups/" + $WorkspaceObject.Id + "/datasets/" + $dataset.Id + "/refreshSchedule" 
        $response = $null
        try
        {
            $response = Invoke-PowerBIRestMethod -Url $ApiUrl -Method Get
            $jsonObj = ConvertFrom-Json $response
            
            $timeAndDateUrl = "https://www.timeanddate.com/worldclock/converter.html?iso=20220117T" + ([string]($jsonObj.times)).Replace(":","") + "00&p1=75&p2=1440&p3=176"
            $cnSamObj = [PSCustomObject] @{
                        "DatasetName" = $dataset.Name
                        "ReportRefreshTime" = $jsonObj.times -as [String]
                        "TimeUrl" =  $timeAndDateUrl
                        "Timezone" = $jsonObj.localTimeZoneId -as [String]
                        "Days" = $jsonObj.days -as [String]
                    }
            [void]$refreshSchedules.Add($cnSamObj)
        }
        catch 
        {
            Write-Host "An error occured Retrieving Schedule for " + $dataset.Name
            Write-Host $_
        }
    }
}

$refreshSchedules | Sort-Object -Property Times,DatasetName | Format-Table -Wrap -AutoSize
$refreshSchedules | Sort-Object -Property Times,DatasetName | Export-Csv -NoTypeInformation -Delimiter "`t" -Path "c:\temp\refreshinfo.csv"
get-content "c:\temp\refreshinfo.csv"
```
