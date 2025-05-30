To embed report in PBI app from a different workspace:
1. Use File >> Embed report >> Embed in website or portal
  1. Enable action bar to show the file, share, option.
  2. Use additional params from below to control how the embeded report looks.
  3. See more info here: https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-embed-secure
2. Embedding in sharepoint: https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-embed-report-spo
3. 

**Embed Query Parameters**
1. reportSection: This parameter allows you to navigate to a specific report page by providing the page name.

`Example: ?reportSection=ReportSectionName`

2. filter: You can apply filters directly within the URL to display only certain data when the report loads.

`Example: ?filter=TableName/FieldName eq 'value'`
see [Filter a report using query string parameters in the URL](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-url-filters) for more

3. bookmark: Navigate to a specific bookmark in the report by specifying the bookmark name.

`Example: ?bookmark=BookmarkName`

4. pageName: Similar to reportSection, it allows you to open a report to a specific page.

`Example: ?pageName=ReportPageName`

5. pageView: This parameter controls the view mode of the page, such as "FitToWidth" or "ActualSize."

`Example: ?pageView=FitToWidth`

6. navContentPaneEnabled: This parameter shows or hides the navigation pane.

`Example: ?navContentPaneEnabled=false`

7. filterPaneEnabled: Shows or hides the filter pane.

`Example: ?filterPaneEnabled=false`

8. fullscreen: Opens the report in full-screen mode.

`Example: ?fullscreen=true`

9. autoplay: Sets the report to automatically play through pages.

`Example: ?autoplay=true`

10. chromeless: Opens the report without the Power BI navigation chrome.

`Example: ?chromeless=1`

11. ctid: The tenant ID, which can be used when you want to embed a report for users from a specific tenant.

`Example: ?ctid=tenantGUID`

12. groupId: Specifies the workspace where the report is located.

`Example: ?groupId=workspaceGUID`

13. config: Allows passing in a configuration string that can control visual configuration settings.

`Example: ?config=configurationString`
