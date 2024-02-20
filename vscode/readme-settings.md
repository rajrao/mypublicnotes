**Git**
```json
"gitlens.remotes": [{
        "regex": "https:\\/\\/(git-codecommit\\.us-west-2\\.amazonaws\\.com)\\/v1/repos\\/(.+)",
        "type": "Custom",
        "name": "AWS Code Commit",
        "protocol": "https",
        "urls": {
            "repository": "https://us-west-2.console.aws.amazon.com/codesuite/codecommit/repositories/${repo}/browse?region=us-west-2",
            "branches": "https://us-west-2.console.aws.amazon.com/codesuite/codecommit/repositories/${repo}/branches?region=us-west-2",
            "branch": "https://us-west-2.console.aws.amazon.com/codesuite/codecommit/repositories/${repo}/browse/refs/heads/${branch}?region=us-west-2", //
            "commit": "https://us-west-2.console.aws.amazon.com/codesuite/codecommit/repositories/${repo}/commit/${id}?region=us-west-2",
            "file": "https://us-west-2.console.aws.amazon.com/codesuite/codecommit/repositories/${repo}/browse/refs/heads/${branch}/--/${file}?region=us-west-2&lines=${line}",
            "fileInBranch": "https://us-west-2.console.aws.amazon.com/codesuite/codecommit/repositories/${repo}/browse/refs/heads/${branch}/--/${file}?region=us-west-2&lines=${line}",
            "fileInCommit": "https://us-west-2.console.aws.amazon.com/codesuite/codecommit/repositories/${repo}/browse/${id}/--/${file}?region=us-west-2&lines=${line}",
            "fileLine": "{line}",
            "fileRange": "${start}-${end}"
            }
        }
    ],
"git-graph.dialog.fetchRemote.prune": true,
"git-graph.repository.fetchAndPrune": true,
"git.autofetch": true,
"git.pruneOnFetch": true,
"git.confirmSync": false,
```
**Python**
```json
"[python]": {
        "editor.formatOnType": true
    },
"autoDocstring.docstringFormat": "pep257",
"python.linting.pycodestyleEnabled": true,
"python.linting.pycodestyleCategorySeverity.E": "Warning",
"python.linting.pycodestyleArgs": ["--max-line-length=99"],
"python.analysis.diagnosticSeverityOverrides": {
    "reportUnboundVariable": "information",
    "reportImplicitStringConcatenation": "none",
    "reportMissingImports": "information",
    "reportUndefinedVariable": "information",
    "reportMissingModuleSource": "information"
},
"python.analysis.inlayHints.functionReturnTypes": true,
"python.analysis.inlayHints.variableTypes": true,
"editor.rulers": [
    99
],
```
