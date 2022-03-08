import os, argparse, sys
from github import Github, BadCredentialsException, UnknownObjectException, GithubException, RateLimitExceededException
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


    # Get dem args
    args = parser.parse_args()

    # First, TOKEN
    TOKEN = None
    Title = "### Public"
    if args.token is not None:
        TOKEN = args.token
    elif os.environ["GITHUB_TOKEN"] is not None:
        TOKEN = os.environ["GITHUB_TOKEN"]
    else:
        Title = "### Public and Private"
        print("Hey, you need a github token in an env var if you want the private repos too!")

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
        except GithubException:
            exit("Error: Some exception occurred")
        except:
            exit("Unknown error connecting to GitHub API. Dost thou have internets?")
    else:
        search = g
        print("No organisation select, grepping ALL repos")

    # How are we doing on the rate limit?
    rate_limit = g.get_rate_limit()
    rate = rate_limit.search
    if rate.remaining == 0:
        print(f'You have 0/{rate.limit} API calls remaining. Reset time: {rate.reset}')
        return
    else:
        print(f'You have {rate.remaining}/{rate.limit} API calls remaining')
        
        # Get the keywords and construct the query
        keywords = input('Enter space separated key keyword(s)[e.g python flask postgres]: ')        
        query = 'org:'+ args.org +' '+ keywords + ' in:file extension:yml'
        
        print('Query is: ' + query)
        try:
            result = g.search_code(query, order='desc')
        except RateLimitExceededException:
            exit("Error: Looks like the secondary rate limit has been reached. Wait a few minutes, then try again")
        except:
            exit("Unknown error on search")            

        files_table_data = [['Repo Name', 'File Name', 'URL']]

        for file in progressbar(result, "Searching repos: ", 40):
        #for file in result:
            filex = [
                file.repository.full_name,
                file.name,
                file.path
            ]
            files_table_data.append(filex)
            #print(file.repository.full_name, file.html_url)
        
        print(f'Found {result.totalCount} file(s)')
        #print(tabulate(files_table_data, headers='firstrow', tablefmt='fancy_grid'))
        print(tabulate(files_table_data, headers='firstrow', tablefmt='github'))

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
