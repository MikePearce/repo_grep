import os, argparse, sys
from github import Github, BadCredentialsException, UnknownObjectException
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tabulate import tabulate

def main():

    # Grab the args (or not)
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--organisation',
                    default=None,
                    dest='org',
                    help='Provide GitHub org name. Defaults to none.',
                    type=str
                    )

    parser.add_argument('-t', '--token',
                    default=None,
                    dest='token',
                    help='Provide a GitHub token. Defaults to none.',
                    type=str
                    )

    parser.add_argument('-d', '--duration',
                    default=6,
                    dest='duration',
                    help='The number of minutes/weeks/months/years. Defaults to 6.',
                    type=int
                    )

    parser.add_argument('-dt', '--durationtype',
                    default="months",
                    dest='duration_type',
                    help='The type of duration: minutes|days|weeks|months|years. Defaults to months.',
                    type=str
                    )



    # Get dem args
    args = parser.parse_args()

    # First, TOKEN
    TOKEN = None
    if args.token is not None:
        TOKEN = args.token
    elif os.environ["GITHUB_TOKEN"] is not None:
        TOKEN = os.environ["GITHUB_TOKEN"]
    else:
        print("Hey, you need a github token in an env var if you want the private repos too!")

    if TOKEN is None:
        Title = "### Public"
    else:
        Title = "### Public and Private"


    # Use my access_token and create an object
    g = Github(TOKEN)

    # See if we've got an org (and the TOKEN can access it)
    if args.org is not None:
        try:
            # Get the org object
            search = g.get_organization(args.org)
            print("Using org ["+ args.org +"]")
        except BadCredentialsException:
            exit("Error: token is not valid")
        except UnknownObjectException:
            exit("Error: org ["+ args.org +"] not recogised.")
        except:
            exit("Unknown error connecting to GitHub API.")
    else:
        search = g
        print("Using personal repos")

    # Oldest date
    duration_in_past = -abs(args.duration)
    deadline = relativeTime(args.duration_type,duration_in_past,datetime.today())

    # Init empty lists
    old_repos = [['Repo Name', 'Last Commit', 'Committer', 'Status']]
    empty_repos = [['Repo Name', 'Owner', 'Status']]

    # Find the repos
    for repo in progressbar(search.get_repos(), "Reticulating the Splines: ", 40):

        try:
            # Got to be a nicer way of doing this?
            last_commit = repo.get_commits()[0]
            last_commit_date = last_commit.commit.author.date
            last_commit_author = last_commit.commit.author
            # If the last update was over
            if (last_commit_date < deadline):

                commit = [
                        repo.name,
                        last_commit_date,
                        last_commit_author.name,
                        "Archived" if repo.archived else "Active"
                        ]
                old_repos.append(commit)
        except:
            commit = [repo.owner, "Archived" if repo.archived else "Active"]
            empty_repos.append(commit)

    print(Title,"Repos older than", args.duration, args.duration_type, len(old_repos))
    print(tabulate(old_repos, headers='firstrow', tablefmt='fancy_grid'))

    print("\n\nEmpty Repos")
    print(tabulate(empty_repos, headers='firstrow', tablefmt='fancy_grid'))


def relativeTime(time_thing, time_to_add, date_to_add_to):
    """ Add time (inc negative) to a date"""
    return date_to_add_to + relativedelta(**{time_thing:time_to_add})

def progressbar(it, prefix="", size=60, file=sys.stdout):
    """
    Simple doodah to print a progress bar thanks to
    https://stackoverflow.com/users/1207193/iambr
    """
    count = it.totalCount
    if count > 0:
        def show(j):
            x = int(size*j/count)
            file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
            file.flush()
        show(0)
        for i, item in enumerate(it):
            yield item
            show(i+1)
        file.write("\n")
        file.flush()

if __name__ == "__main__":
    main()
