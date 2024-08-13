from github import Github
import csv

# GitHub personal access token
github_token = 'access_token_here'
g = Github(github_token)

# List of repositories to collect solutions from
repositories = ['froghramar/uva', 'sajinia/UVa-Online-Judge', 'ztrixack/uva-online-judge', 'guzlewski/onlinejudge', 'louisfghbvc/Uva', 'San0330/UVA-Solutions', 'soumik9876/UVA-Solutions', 'Diusrex/UVA-Solutions', 'ackoroa/UVa-Solutions', 'ksaveljev/UVa-online-judge', 'truongduy134/uva-online-judge-solutions', 'rezwan4029/UVA-CODES', 'milon/UVa', 'isanchez-aguilar/UVa-Solutions'] 

# CSV file name
csv_file_name = 'datasets/uva_solutions.csv'

def extract_problem_id(path):
    # The problem ID is a number between 100 and 1999
    parts = path.split('/')
    filename = parts[-1]  # Get the last part of the path, which is the filename
    # Extract numeric part from the filename
    numeric_part = ''.join(filter(str.isdigit, filename))
    if numeric_part and 100 <= int(numeric_part) <= 1999:
        return numeric_part
    return None

def generate_problem_link(problem_id):
    ranges = [
        (100, 199), (200, 299), (300, 399), (400, 499),
        (500, 599), (600, 699), (700, 799), (800, 899),
        (900, 999), (1000, 1099), (1100, 1199), (1200, 1299),
        (1300, 1399), (1400, 1499), (1500, 1599), (1600, 1699),
        (1700, 1799)
    ]
    for idx, (start, end) in enumerate(ranges, start=1):
        if start <= problem_id <= end:
            return f'https://onlinejudge.org/external/{idx}/{problem_id}.pdf'
    return None

def traverse_folders(repo, folder, solutions):
    for content in folder:
        if content.type == 'dir':
            traverse_folders(repo, repo.get_contents(content.path), solutions)
        elif content.type == 'file' and content.name.endswith('.cpp'):
            solution_content = content.decoded_content.decode('utf-8')
            problem_id = extract_problem_id(content.path)
            if problem_id is not None:
                problem_link = generate_problem_link(int(problem_id))
                solutions.append({'repo': repo.full_name, 'problem_link': problem_link, 'content': solution_content})

def collect_uva_solutions(repo_name):
    repo = g.get_repo(repo_name)
    solutions = []
    traverse_folders(repo, repo.get_contents(''), solutions)
    return solutions

# Create a CSV file to store the collected data
with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Repository', 'Problem Link', 'Solution'])

    # Loop through each repository
    for repo_name in repositories:
        try:
            repo_solutions = collect_uva_solutions(repo_name)

            # Write repository, problem link, and solution to the CSV file
            for solution in repo_solutions:
                csv_writer.writerow([solution['repo'], solution['problem_link'], solution['content']])

            print(f'Solutions collected from {repo_name}')
        except Exception as e:
            print(f'Error collecting solutions from {repo_name}: {e}')
        
        # GitHub API rate limit handling
        remaining_requests = g.get_rate_limit().core.remaining
        if remaining_requests <= 1:
            reset_time = g.get_rate_limit().core.reset
            sleep_duration = max(0, reset_time - time.time())
            print(f'Rate limit reached. Sleeping for {sleep_duration} seconds.')
            time.sleep(sleep_duration)

print(f'CSV file "{csv_file_name}" created successfully.')