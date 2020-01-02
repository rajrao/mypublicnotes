Sourced from: https://help.github.com/articles/syncing-a-fork/

Configure to allow merging between someone else's branch and yours 

**One time configuration**
	
	See configured remotes:
		git remote -v
		
	Add remote:
		git remote add upstream https://github.com/SpilledMilkCOM/MooveePicker.git
	
**Merge source repo into my fork**

	Create a branch for the merge.

	Fetch upstream:
		git fetch upstream
	
	Change to master (or the branch into which you are doing the merge)
		git checkout master
	
	Merge **upstream/master** to **master**
	
		git merge upstream/master
		
	or
	
	Change to master
		git checkout master
	Pull to master
		git pull upstream/master

	
Create the pull request via GitHub to source repo.
