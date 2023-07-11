import yaml
from git import Repo

def main():
    repo = Repo(".")
    changed_files = repo.git.diff("origin/main...HEAD", name_only=True).split('\n')

    for file in changed_files:
        if file.endswith('.yaml'):
            check_epoch_increment(file)

def check_epoch_increment(file):
    repo = Repo(".")

    old_content = repo.git.show(f"origin/main:{file}")
    new_content = repo.git.show(f"HEAD:{file}")

    old_yaml = yaml.safe_load(old_content)
    new_yaml = yaml.safe_load(new_content)

    old_package = old_yaml.get('package', {})
    new_package = new_yaml.get('package', {})

    old_epoch = old_package.get('epoch')
    new_epoch = new_package.get('epoch')

    old_version = old_package.get('version')
    new_version = new_package.get('version')

    if old_version != new_version:
        return

    if old_epoch is not None and new_epoch is not None and new_epoch != old_epoch + 1:
        print(f"The package.epoch in {file} should probably be incremented by one.")
        exit(1)

if __name__ == "__main__":
    main()

