$reportName = "xxxxx"
$reportWorkspaceName = "yyyyy"

$datasetWorkspaceName = "aaaaa"
$datasetName = "bbbbb"

function RebindReport{
    param(
        [string]$workspaceId,
        [string]$reportId,
        [string]$datasetIdToRebindTo
    )

    if ($workspaceId -eq $null -or $reportId -eq $null -or $datasetIdToRebindTo -eq $null)
    {
        throw "WorkspaceId, ReportId, and DatasetIdToRebindTo must be specified"
    }
          

    $ApiUrl = "https://api.powerbi.com/v1.0/myorg/groups/${workspaceId}/reports/${reportId}/Rebind" 
    $ApiRequestBody = "{'datasetId': '${datasetIdToRebindTo}'}"
    $ApiRequestBody

    $response = $null
    try
    {
        Write-Host "Rebinding Report"
        $response = Invoke-PowerBIRestMethod -Url $ApiUrl -Method Post -Body ($ApiRequestBody)
        Write-Host "Rebind completed"
        
        Write-Host "Complete"
    }
    catch 
    {
        Write-Host "An error occurred:"
        Write-Host $_
    }
    $response

}
$ErrorActionPreference = "Stop"

#Login-PowerBI | Out-Null

#report info
$WorkspaceObject = (Get-PowerBIWorkspace -Name $reportWorkspaceName)
$PbiReportObject = (Get-PowerBIReport -Workspace $WorkspaceObject -Name $reportName)
$reportWorkspaceId = $WorkspaceObject.Id
$reportId = $PbiReportObject.Id
$oldDatasetForReport = $PbiReportObject.DatasetId

#dataset to rebind to info
$datasetWorkspaceObject = (Get-PowerBIWorkspace -Name $datasetWorkspaceName)
$PbiDatasetObject = (Get-PowerBIDataset -Workspace $datasetWorkspaceObject -Name $datasetName)
$datasetWorkspaceId = $datasetWorkspaceObject.Id
$datasetId = $PbiDatasetObject.Id

Write-Host "Rebinding ReportId: ${reportId}"
Write-Host "in workspace ${reportWorkspaceId}"
Write-Host "from ${oldDatasetForReport}"
Write-Host "to ${datasetId} in ${datasetWorkspaceId}"


RebindReport -workspaceId $reportWorkspaceId -reportId $reportId -datasetIdToRebindTo $datasetId

$PbiReportObject = (Get-PowerBIReport -Workspace $WorkspaceObject -Name $reportName)
$PbiReportObject
