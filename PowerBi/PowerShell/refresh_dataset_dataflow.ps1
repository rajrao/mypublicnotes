function GetRefreshHistory{
    param(
        [string]$workspaceName,
        [string]$datasetName
    )

    
    $WorkspaceObject = (Get-PowerBIWorkspace -Name $workspaceName)
    $PbiReportObject = (Get-PowerBIReport -Workspace $WorkspaceObject -Name $datasetName)

    $ApiUrl = "groups/" + $WorkspaceObject.Id + "/datasets/" + $PbiReportObject.DatasetId + "/refreshes" 
    $response = $null
    try
    {
        Write-Host "Retrieving refresh history $ApiUrl"
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

function RefreshDataset{
    param(
        [string]$workspaceName,
        [string]$datasetName
    )

    
    $WorkspaceObject = (Get-PowerBIWorkspace -Name $workspaceName)
    $PbiReportObject = (Get-PowerBIReport -Workspace $WorkspaceObject -Name $datasetName)

    $ApiUrl = "groups/" + $WorkspaceObject.Id + "/datasets/" + $PbiReportObject.DatasetId + "/refreshes" 
    $response = $null
    try
    {
        Write-Host "Retrieving refresh history $ApiUrl"
        $response = Invoke-PowerBIRestMethod -Url $ApiUrl -Method Post # -Body "{'notifyOption':'NoNotification'}"
        Write-Host $response
        Write-Host "Complete"
    }
    catch 
    {
        Write-Host "An error occurred:"
        Write-Host $_
    }
    $response

}

function RefreshDataflow{
    param(
        [string]$workspaceName,
        [string]$dataflowName
    )

    
    $WorkspaceObject = (Get-PowerBIWorkspace -Name $workspaceName)
    $PbiReportObject = (Get-PowerBIDataflow -Workspace $WorkspaceObject -Name $dataflowName)

    $ApiUrl = "groups/" + $WorkspaceObject.Id + "/dataflows/" + $PbiReportObject.Id + "/refreshes" 
    $response = $null
    try
    {
        Write-Host "Retrieving refresh history $ApiUrl"
        $response = Invoke-PowerBIRestMethod -Url $ApiUrl -Method Post -Body "{'notifyOption':'NoNotification'}"
        Write-Host $response
        Write-Host "Complete"
    }
    catch 
    {
        Write-Host "An error occurred:"
        Write-Host $_
    }
    $response
}

function ConnectToPbi
{
    $applicationId = "insert clientid here";
    $securePassword = "insert client secret here" | ConvertTo-SecureString -AsPlainText -Force
    $credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $applicationId, $securePassword
    Connect-PowerBIServiceAccount -ServicePrincipal -Credential $credential -TenantId "18791e17-6159-4f52-a8d4-de814ca8284a"
}


# use login-powerbi to use your credentials
# use ConnectToPbi to use an SPN
#Login-PowerBI | Out-Null
ConnectToPbi


GetRefreshHistory "Workspace Name Here" "Dataset Name Here"
RefreshDataset "Workspace Name Here" "Dataset Name Here"
RefreshDataflow "Workspace Name Here" "Dataflow Name Here"
