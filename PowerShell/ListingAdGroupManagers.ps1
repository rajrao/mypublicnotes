#set the searchRoot and filter appropriately

cls
$directorySearcher = New-Object System.DirectoryServices.DirectorySearcher
$directorySearcher.SearchRoot = [ADSI]'LDAP://xxxx.yyyy.com'
$directorySearcher.Filter = '(cn=AdGroupPrefix*)' #
[void]$directorySearcher.PropertiesToLoad.Add('cn')
[void]$directorySearcher.PropertiesToLoad.Add('distinguishedname')
[void]$directorySearcher.PropertiesToLoad.Add('managedBy')
[void]$directorySearcher.PropertiesToLoad.Add('displayName')
[void]$directorySearcher.PropertiesToLoad.Add('info')
$results = $directorySearcher.FindAll()

#$results | Select-Object @{Name="cn";Expression={$_.Properties["cn"]}},@{Name="manager";Expression={$_.Properties["managedBy"]}},@{Name="info";Expression={$_.Properties["info"]}} `
#                    | Format-Table -Wrap -AutoSize
#                    #,@{Name="dn";Expression={$_.Properties["distinguishedname"]}},@{Name="displayname";Expression={$_.Properties["displayName"]}} `

$customObjectArray = New-Object System.Collections.ArrayList
foreach ($row in $results)
{
    try
    {
        if ($row.Properties["managedBy"] -ne $null)
        {
            $manager =  [regex]::Matches(($row.Properties["managedBy"] -as [String]), "CN=(.*?),.*").Groups[1].Value
        }
        else
        {
            $manager = ""
        }
        
        $cnSamObj = [PSCustomObject] @{
                        "cn" = $row.Properties["cn"] -as [String]
                        "managedBy" = $manager
                        "info" = $row.Properties["info"] -as [String]
                    
                        #"displayName" = $row.Properties["displayName"] -as [String]
                        #"distinguishedname" = $row.Properties["distinguishedname"] -as [String]
                    }
        [void]$customObjectArray.Add($cnSamObj)
    }
    catch 
    {
        Write-Output $row.Properties
    }
}

$customObjectArray | Sort-Object -Property cn | Format-Table
