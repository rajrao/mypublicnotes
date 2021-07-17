#############################################################
# This tool can extract the report pages from a pbix file that contains
# both the datamodel (dataset) and reports.
# It requires 7zip to be installed on your machine.
# When you run the file, point at your dataset pbix.
# a new file with the postfix "_reports" will be created.
# open the new pbix file, all your visuals will show an error. Point it at the dataset
# hosted in PowerBi.com service.
##############################################################

Add-Type -AssemblyName System.IO.Compression.FileSystem

#https://devblogs.microsoft.com/scripting/hey-scripting-guy-can-i-open-a-file-dialog-box-with-windows-powershell/
Function Get-FileName($initialDirectory)
{  
 [System.Reflection.Assembly]::LoadWithPartialName(“System.windows.forms”) |
 Out-Null

 $OpenFileDialog = New-Object System.Windows.Forms.OpenFileDialog
 $OpenFileDialog.initialDirectory = $initialDirectory
 $OpenFileDialog.filter = “PBIX (*.pbix)| *.pbix”
 $OpenFileDialog.ShowDialog() | Out-Null
 $OpenFileDialog.filename
} #end function Get-FileName


#$DebugPreference = "Continue" #use to see error messages
$ErrorActionPreference = "Stop"
try
{
    cls

    $datasetFilePath = Get-FileName
    $datasetFolderPath = [System.IO.Path]::GetDirectoryName($datasetFilePath)
    $datasetFileName = [System.IO.Path]::GetFileNameWithoutExtension($datasetFilePath)
    
    Write-Host "Processing $datasetFileName...."
    
    $tempReportLocation = $env:TEMP + "\ds2rpt_" + (New-Guid)
    Write-Debug "Temp folder $tempReportLocation"

    [System.IO.Compression.ZipFile]::ExtractToDirectory($datasetFilePath, $tempReportLocation)

    Write-Debug "Deleting datamodel"
    try
    {
        Remove-Item ($tempReportLocation + "\DataModel")
    }
    catch
    {
        Write-Error "A DataModel was not found in the PBIX. Please use a PBIX that is a dataset!"
        throw
    }
    Write-Debug "Deleting connections"
    Remove-Item ($tempReportLocation + "\Connections")
    Write-Debug "Deleting SecurityBindings"
    Remove-Item ($tempReportLocation + "\SecurityBindings")


    Write-Debug "Cleaning up `[Content_Types`].xml"
    #https://stackoverflow.com/questions/31478105/powershell-script-to-delete-xml-element
    $contentTypeFileName = $tempReportLocation + "\``[Content_Types``].xml"
    $contentTypesDoc = [xml](Get-Content $contentTypeFileName)
    $deleteNames = "/DataModel","/Connections","/SecurityBindings"
    ($contentTypesDoc.Types.ChildNodes |Where-Object { $DeleteNames -contains $_.PartName }) | ForEach-Object {
        Write-Debug $_.PartName
        # Remove each node from its parent
        [void]$_.ParentNode.RemoveChild($_)
    }
    $dataMashupNode = $contentTypesDoc.CreateNode("element", "Override", $contentTypesDoc.DocumentElement.NamespaceURI)
    $dataMashupNode.SetAttribute("PartName","/DataMashup")
    $dataMashupNode.SetAttribute("ContentType","")
    $contentTypesDoc.Types.AppendChild($dataMashupNode) > $null

    Write-Debug "Writing out `[Content_Types`].xml"
    $contentTypesDoc.Save($tempReportLocation + "\[Content_Types].xml")


    $outputFolder = $tempReportLocation + "reportOnly"
    New-Item $outputFolder -ItemType directory > $null

    $outputPbixFilePath = $outputFolder + "\" + $datasetFileName + "_reports.zip"

    #[System.IO.Compression.ZipFile]::CreateFromDirectory($tempReportLocation, $outputPbixFilePath)
    #Compress-Archive -Path ("$tempReportLocation" +"\*") -DestinationPath $outputPbixFilePath -CompressionLevel Optimal

    $7zipPath = "$env:ProgramFiles\7-Zip\7z.exe"
    try
    {
        & "$7zipPath" "a" "$outputPbixFilePath" ("$tempReportLocation" +"\*") > $null
    }
    catch
    {
        Write-Error "Please ensure 7Zip is installed before running this tool"
        throw
    }
    Write-Debug "Writing to path $datasetFolderPath\$datasetFileName`_reports.pbix"
    Move-Item $outputPbixFilePath -Destination "$datasetFolderPath\$datasetFileName`_reports.pbix" -Force -ErrorAction Stop

    Write-Host "Success!!! Created file at $datasetFolderPath\$datasetFileName`_reports.pbix"
    Write-Host "After opening the new file `"$datasetFileName`_reports.pbix`", use `"PowerBi Datasets`" option in PBI toolbar, to point the pbix at the correct dataset"
}
catch
{
    Write-Error $_.Exception
}
