g-init:
		touch .gitignore
		git init
		git add .
		git commit -m "initial commit"

g-hooks:
		cp -r ./scripts/.githooks .git/hooks/

g-add: sort format api-sort api-format clean-commands
		git add .

g-commit: format pylint-dev
		git commit -m "$(filter-out $@,$(MAKECMDGOALS))"

g-log:
		git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
