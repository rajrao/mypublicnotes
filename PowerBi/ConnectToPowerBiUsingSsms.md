

1. Install DaxStudio (https://daxstudio.org/)
2. After you open DaxStudio and connect to your PowerBi instance, you will be able to determine the PowerBi port by looking at the status bar (bottom right).

Now that you have the port, you can connect to PowerBi as though it were an SSAS instance, using localhost:xxxxx which you determined in step 2. You can use either SSMS or Excel do do this.










Useful commands:
1. TASKLIST /FI "imagename eq msmdsrv.exe" /FI "sessionname eq console"
2. netstat /ano | findstr "portnumber from above command"

PowerBi Temp Folder:
%LocalAppData%\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces
