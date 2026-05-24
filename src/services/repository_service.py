import git
import os


class RepositoryService:

    def clone_repo(self, repo_url, path="repos"):

        repo_name = repo_url.split("/")[-1]

        clone_path = os.path.join(
            path,
            repo_name
        )

        if not os.path.exists(path):
            os.makedirs(path)

        git.Repo.clone_from(
            repo_url,
            clone_path
        )

        return clone_path