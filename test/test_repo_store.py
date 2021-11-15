import ranking_modules.repo_store


# TODO
def test_get_dependencies():
    repo = ranking_modules.repo_store.RepoStore('test', 'test')
    assert repo.get_dependencies() == {}
