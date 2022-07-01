from redminelib import Redmine
from dotenv import load_dotenv
import os
load_dotenv()

class RedmineClient:
    url = os.getenv('REDMINE_URL')
    key = os.getenv('REDMINE_TOKEN')
    redmine = Redmine(url, key = key)

    def issues(self, project):
        project = self.redmine.project.get(project)
        return project.issues
