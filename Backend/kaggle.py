import subprocess
import time 

class kaggleAPI:
    def __init__(self, notebook_id, project_path):
        self.notebook_id = notebook_id
        self.project_path = project_path

    def execute_terminal_command(self, command):
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.stdout

    def init_kaggle_dataset(self):
        command = f'kaggle datasets init -p {self.project_path}/dataset'
        return self.execute_terminal_command(command)

    def create_kaggle_dataset(self):
        command = f'kaggle datasets create -p {self.project_path}/dataset -r tar'
        return self.execute_terminal_command(command)

    def pull_kaggle_dataset(self, dataset_id):
        command = f'kaggle datasets metadata -p {self.project_path}/dataset {dataset_id}'
        return self.execute_terminal_command(command)

    def update_kaggle_dataset(self):
        command = f'kaggle datasets version -p {self.project_path}/dataset -m "Updated dataset using Kaggle API" -r tar'
        return self.execute_terminal_command(command)

    def pull_kaggle_notebook(self):
        command = f'kaggle kernels pull {self.notebook_id} -p {self.project_path}/notebook -m'
        return self.execute_terminal_command(command)

    def push_kaggle_notebook(self):
        command = f'kaggle kernels push -p {self.project_path}/notebook'
        return self.execute_terminal_command(command)

    def get_notebook_status(self):
        command = f'kaggle kernels status {self.notebook_id}'
        return self.execute_terminal_command(command)

    def get_notebook_output(self):
        command = f'kaggle kernels output {self.notebook_id} -p {self.project_path}/nb_output'
        return self.execute_terminal_command(command)

    def wait_for_notebook_completion(self):
        while True:
            status = self.get_notebook_status()
            if "complete" in status.lower():
                print("Notebook has completed its run.")
                break
            elif "error" in status.lower():
                print("Notebook run encountered an error.")
                break
            time.sleep(1) 