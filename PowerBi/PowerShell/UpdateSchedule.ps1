function UpdateSchedule{
    param(
        [string]$workspaceName,
        [string]$datasetName,
        [decimal]$everyXHours
    )

    Write-Host "Updating schedule for $datasetName in $workspaceName for every $everyXHours hours"

    Connect-PowerBIServiceAccount | Out-Null 
    $WorkspaceObject = (Get-PowerBIWorkspace -Name $workspaceName)
    $PbiReportObject = (Get-PowerBIReport -Workspace $WorkspaceObject -Name $datasetName)

    $ApiUrl = "groups/" + $WorkspaceObject.Id + "/datasets/" + $PbiReportObject.DatasetId + "/refreshSchedule" 

    
    $time = [TimeSpan]::Zero

    $hourlySchedule = ""
    $s = @()
    while($time.TotalHours -lt 24)
    {
        $s+="""$($time.ToString('hh\:mm'))"""
        $time = $time.Add([TimeSpan]::FromMinutes($everyXHours*60))
    }
    $hourlySchedule = [String]::Join(',',$s)
    Write-Host "Number of schedules $(($s).length)"


    $scheduleToUse = $hourlySchedule

    $ApiRequestBody = @"
    {
        "value": {
            "days": [
                "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
            ],
            "times": [
               %%scheduleToUse%%
            ],
            "enabled": true,
            "localTimeZoneId": "Mountain Standard Time",
            "notifyOption": "MailOnFailure"
        }
    }
"@
    

    $ApiRequestBody = $ApiRequestBody.Replace('%%scheduleToUse%%',$scheduleToUse)

    $response = $null
    try
    {
        Write-Host "Updating Refresh Schedule"
        $response = Invoke-PowerBIRestMethod -Url $ApiUrl -Method Patch -Body ($ApiRequestBody)
        Write-Host "Refresh Schedule Updated. Retrieving Schedule"
        $response = Invoke-PowerBIRestMethod -Url $ApiUrl -Method Get
        Write-Host "Complete"
    }
    catch 
    {
        Write-Host "An error occurred:"
        Write-Host $_
    }
    $response

}

UpdateSchedule "WorkspaceName" "DatasetName" 1
