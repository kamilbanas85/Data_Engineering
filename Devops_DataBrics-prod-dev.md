Aby zsynchronizować zmienną wskazującą na aktualne środowisko dev, prod itp., w pliku konfiguracyjnym (przykładowo 'config_file.py') należy utworzyć pipeline w pliku YMAL.


Aby plik YMAL mógł wykonać 'commit' zmian do danego środowiska, należy nadać uprawnienia 'Contribute' oraz 'Contribute to pull reqests' dla grupy 'Project Name' Build Serice '[Organization Name] dla danego repozytorium na którym mają być zmiany:


(Project Setting -> Repositories -> Nazwa Repo -> Security)



<img src="./schemat.jpg" width="600">


Przykład pliku YMAL:

```yaml
trigger:
  branches:
    include:
      - dev
      - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  # Checkout the repository explicitly using the built-in script
  - checkout: self
    persistCredentials: true # Important - Persist creds to run further git commands
    clean: true

  # Determine the branch name and update Env_config
  - script: |
      echo "## Determining the branch name..."
      echo "Branch name: $(Build.SourceBranchName)"

      # Set environment value based on branch
      if [ "$(Build.SourceBranchName)" = "main" ]; then
        ENV_VALUE="prod"
      else
        ENV_VALUE="dev"
      fi
      echo "Setting Env_config to $ENV_VALUE"

      # Update the config_file.py in the same directory
      sed -i "s/Env_config = .*/Env_config = \"$ENV_VALUE\"/" ./config_file.py
      echo "Updated config_file.py with Env_config=$ENV_VALUE"
    displayName: Update Config File

  # Commit and push the changes
  - script: |
      echo "## Committing changes..."
      git config --global user.email "$(Build.RequestedForEmail)"
      git config --global user.name "Azure Pipelines"

      git add ./config_file.py
      git commit -m "Set Env_config to $ENV_VALUE for branch $(Build.SourceBranchName)"
      git push origin HEAD:$(Build.SourceBranchName)
    displayName: Commit Changes
```


Przykład pliku 'config_file.py':

```python
# Configuration for the environment

Env_config = "dev"  # Environment can be "dev" or "prod"
```
