#requires -version 2
[CmdletBinding()]
<#
.SYNOPSIS
  <Overview of script>

.DESCRIPTION
  <Brief description of script>

.PARAMETER <Parameter_Name>
    <Brief description of parameter input required. Repeat this attribute if required>

.INPUTS
  <Inputs if any, otherwise state None>

.OUTPUTS
  <Outputs if any, otherwise state None - example: Log file stored in C:\Windows\Temp\<name>.log>

.NOTES
  Version:        1.0
  Author:         <Name>
  Creation Date:  <Date>
  Purpose/Change: Initial script development
  
.EXAMPLE
  <Example goes here. Repeat this attribute for more than one example>
#>

PARAM ( 
    [string]$aReqParam = $(throw "-aReqParam is required."),
    [switch]$YesNoSwitch = $false
)
#---------------------------------------------------------[Initialisations]--------------------------------------------------------

#Set Error Action to Silently Continue
#$ErrorActionPreference = "SilentlyContinue"

#Dot Source required Function Libraries
#. "C:\Scripts\Functions\Logging_Functions.ps1"

#----------------------------------------------------------[Declarations]----------------------------------------------------------

#Script Version
$sScriptVersion = "1.0"

#Log File Info
$sLogPath = "$HOME\clouddrive"
$sLogName = "x.log"
$sLogFile = Join-Path -Path $sLogPath -ChildPath $sLogName

function Write-Log-Start {
    param (
        [Parameter(Mandatory=$False, Position=0)]
        [String]$Entry
    )
   Write-Log $Entry $false
}

function Write-Log {
    param (
        [Parameter(Mandatory=$False, Position=0)]
        [String]$Entry,
        [Parameter(Mandatory=$False, Position=1)]
        [switch]$Append = $true
    )
    $message = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff') $Entry";
    Write-Host $message
    if ($Append)
    {
        $message | Out-File -FilePath $sLogFile -Append
    }
    else
    {
        $message | Out-File -FilePath $sLogFile
    }
}

#-----------------------------------------------------------[Functions]------------------------------------------------------------


Function Function1{
  Param([String]$param1 = "no value provided")
  
  Begin{
    Write-Log "$param1"
    Write-Log "<description of what is going on>..."
  }
  
  Process{
    Try{
      #<code goes here>
    }
    
    Catch{
      Write-Log $_.Exception
      Break
    }
  }
  
  End{
    If($?){
      Write-Log "Completed Successfully."
      Write-Log " "
    }
  }
}


#-----------------------------------------------------------[Execution]------------------------------------------------------------
cls;
Write-Log-Start "Start"
Write-Log "Hello $aReqParam $YesNoSwitch"
Function1
