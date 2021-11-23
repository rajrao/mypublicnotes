cls
$loadUserDetails = $false #set to $true if you want additional info like samAccountName and UPN.
$onlyCountMembers = $true

$adGroup_CN_Name = "xxxxxx"

$directorySearcher = New-Object System.DirectoryServices.DirectorySearcher
$directorySearcher.SearchRoot = [ADSI]'LDAP://xxxxx.yyyy.com'

$directorySearcher.Filter = '(cn='+ $adGroup_CN_Name  + ')' #
[void]$directorySearcher.PropertiesToLoad.Add('cn')
[void]$directorySearcher.PropertiesToLoad.Add('distinguishedname')
[void]$directorySearcher.PropertiesToLoad.Add('member')
$results = $directorySearcher.FindOne()

$results

$members = New-Object System.Collections.ArrayList
if ($pageProperty = $results.Properties.PropertyNames.Where({$psitem -match '^member;range'}) -as [String]) {
    $directoryEntry = $results.Properties.adspath -as [String]
    $increment = $results.Properties.$pageProperty.count -as [Int]
    $results.Properties.$pageProperty.Foreach({ [void]$members.Add($psitem) })
    
    $start = $increment
    do {
        $end = $start + $increment - 1
        $memberProperty = 'member;range={0}-{1}' -f $start,$end
        $memberPager = New-Object -TypeName System.DirectoryServices.DirectorySearcher -ArgumentList $directoryEntry,'(objectClass=*)',$memberProperty,'Base'
        $pageResults = $memberPager.FindOne()
        $pageProperty = $pageResults.Properties.PropertyNames.Where({$psitem -match '^member;range'}) -as [String]
        $pageResults.Properties.$pageProperty.Foreach({ [void]$members.Add($psitem) })
        $start = $end + 1
    } until ( $pageProperty -match '^member.*\*$' )
}
else {
    $results.Properties.member.Foreach({ [void]$members.Add($psitem) })
}

Write-Host "Simple list written to output_$adGroup_CN_Name`_List.csv"
$members | Set-Content "output_$adGroup_CN_Name`_SimpleList.csv"
$members.Count

if ($loadUserDetails -eq $true)
{
    $customObjectArray = New-Object System.Collections.ArrayList
    #foreach ($cn in $members)
    #{
    #   $found = $cn -match '(?:CN=)(.*?)(?:,)'
    #   if ($found)
    #   {
    #        $filter = "(cn=$($matches[1]))"
    #        $user = Get-ADUser -LDAPFilter $filter  -Server "usdendc04.corp.hds.com" -Properties "sAMAccountName"
    #        if ($user)
    #        {
    #            $sAMAccountName = $user.sAMAccountName
    #            $cnSamObj = [PSCustomObject] @{
    #                "cn" = $matches[1].ToString()
    #                "sAMAccountName" = $sAMAccountName
    #            }
    #
    #            $customObjectArray.Add($cnSamObj)
    #        }
    #    }
    #}
    $directorySearcher = New-Object System.DirectoryServices.DirectorySearcher
    $directorySearcher.SearchRoot = [ADSI]'LDAP://xxxxx.yyyy.com'
    [void]$directorySearcher.PropertiesToLoad.Add('cn')
    [void]$directorySearcher.PropertiesToLoad.Add('sAMAccountName')
    [void]$directorySearcher.PropertiesToLoad.Add('userprincipalname')

    $stopWatch = [System.Diagnostics.Stopwatch]::StartNew()

    foreach ($cn in $members)
    {
        $found = $cn -match '(?:CN=)(.*?)(?:,)'
        if ($found)
        {
            $directorySearcher.Filter = "(cn=$($matches[1]))"
            $results = $directorySearcher.FindOne()
            $cnSamObj = [PSCustomObject] @{
                    "cn" = $matches[1].ToString()
                    "sAMAccountName" = $results.Properties["samaccountname"] -as [String]
                    "userprincipalname" = $results.Properties["userprincipalname"] -as [String]
                }

            $customObjectArray.Add($cnSamObj)
       }
    }



    $customObjectArray.Count

    $csv = $customObjectArray | ForEach-Object{$_}| ConvertTo-Csv -NoTypeInformation
    
    Write-Host "Detailed list written to output_$adGroup_CN_Name`_List.csv"
    $customObjectArray | ForEach-Object{$_}| export-CSV "output_$adGroup_CN_Name`_DetailedList.csv" -notype

    $customObjectArray.Count

    Write-Host "Elapsed milliseconds $($stopWatch.ElapsedMilliseconds)"
}
