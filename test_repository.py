from src.services.repository_service import RepositoryService

service = RepositoryService()

path = service.clone_repo(
    "https://github.com/psf/requests"
)

print("Repository cloned at:")
print(path)