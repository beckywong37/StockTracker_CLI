
"""
File name: test_commit.py
Description: Setting up Github repository for project and making a test commit

Github username: beckywong37
Step 1: Add remote repo with token
    git remote add origin <URL>
    git remote set-url origin <URL>
Step 2: Check repo added correctly (will show URL with token)
    git remote -v
Step 3: Check name of branch
    git branch
Step 4: Stage changes
    git add .
    git status (shows which files will be committed)
Step 5: Commit changes
    git commit -m "Your commit message"
Step 6: To share changes with remote repo, need to push
    git push origin master
"""

"""
Setting up git on new laptop
1. Clone repo (CS361-MainProgram) from git to computer 
2. git init - initialize Git repo by creating .git directory in project
    tells git it can start tracking changes
3. git add ./ - add project files in current directory
4. git status - check what changes have been staged
5. git commit -m "Initial commit" - commit changes
"""
