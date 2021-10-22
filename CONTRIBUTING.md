# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue before making a change. 

Please note we have a [code of conduct](CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.

## Pull Request Process

1. Ensure the CI pipeline and all checks are passing.
2. Update documentation with details of changes.
3. Add an entry to the [change log](CHANGELOG.md).
4. You may merge the Pull Request in once it has approvals of two other developers. If you do not have permission to do
    that, you may request the second reviewer to merge it for you.
   

## Publishing a New Version

Once the package is ready to be released, there are a few things that need to be done:

1. Start with a local clone of the repo on the default branch with a clean working tree.
2. Run the version bump script with the appropriate part name (`major`, `minor`, or `patch`).
    Example: `docker-compose run --rm bump minor`
    
    This wil create a new branch, updates all affected files with the new version, and commit the changes to the branch.

3. Push the new branch to create a new pull request.
4. Get the pull request approved.
5. Merge the pull request to the default branch.

Merging the pull request will trigger a GitHub Action that will create a new release. The creation of this new
release will trigger a GitHub Action that will to build a wheel & a source distributions of the package and push them to
[PyPI][pypi].

!!! warning
    The action that uploads the files to PyPI will not run until a repository maintainer acknowledges that the job is
    ready to run. This is to keep the PyPI publishing token secure. Otherwise, any job would have access to the token. 

In addition to uploading the files to PyPI, the documentation website will be updated to include the new version. If the
new version is a full release, it will be made the new `latest` version.
