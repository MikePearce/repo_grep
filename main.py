import os
from github import Github
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

def main():

    try:
        TOKEN = None
        # Get token (NO SECRETS HERE!)
        TOKEN = os.environ["GITHUB_TOKEN"]
        Title = "### Public and Private"
    except KeyError:
        Title = "### Public"
        print("Hey, you need a github token in an env var if you want the private repos too!")

    # Use my access_token and create an object
    g = Github(TOKEN)

    # Get the org object
    org = g.get_organization("mytutorcode")

    # Oldest date
    months_in_past = -6
    deadline = relativeTime("months",months_in_past,datetime.today())

    # Init empty dict
    old_repos = {}
    OK_repos = {}

    # Find the repos
    for repo in org.get_repos():
        try:
            # Got to be a nicer way of doing this?
            last_commit = repo.get_commits()[0]
            last_commit_date = last_commit.commit.author.date
            last_commit_author = last_commit.commit.author

            # If the last update was over
            if (last_commit_date < deadline):

                commit = {repo.name: {'last_commit':last_commit_date, 'owner': last_commit_author.name}}
                old_repos.update(commit)
                #repo.get_readme
        except:
            print(repo.name, "is empty")

    print(Title,"Repos older than", months_in_past, "months:", len(old_repos))
    for repoName, dict in old_repos.items():
        print (str(dict['last_commit']), "-", dict['owner'], "-", repoName)


def relativeTime(time_thing, time_to_add, date_to_add_to):
    """ Add time (inc negative) to a date"""
    return date_to_add_to + relativedelta(**{time_thing:time_to_add})

if __name__ == "__main__":
    main()
