import subprocess
import sys
import json


def loadConfig():
    with open("project_build_config.json", 'r') as config:
        return json.load(config)


def detectChanges(conf):
    git_command = ['git', '--no-pager', 'diff',
                   '--name-only', 'HEAD', sys.argv[1]]

    gitDiff = subprocess.check_output([*git_command]).decode("utf-8")
    gitDiff = gitDiff.splitlines()
    defaults = conf['defaults']
    projectAndContents = [(proj, elements)
                          for proj in conf['projects']
                          for elements in conf['projects'][proj]]
    """
    Iterate through the git changes and see what projects need
    to be built
    """
    tmpToBuild = []
    for diff in gitDiff:
        for obj in projectAndContents:
            if obj[1].endswith('/'):
                if diff.startswith(obj[1]):
                    tmpToBuild.append(obj[0])
            elif obj[1] == diff:
                tmpToBuild.append(obj[0])
    # If the lengths aren't equal, refer to defaults as needing a build
    if len(tmpToBuild) != len(gitDiff):
        tmpToBuild.extend(defaults)
    tmpToBuild = list(set(tmpToBuild))

    projectsToBuild = []
    if 'all' in tmpToBuild:
        tmpToBuild.remove('all')
        for obj in projectAndContents:
            if obj[0] != 'all':
                tmpToBuild.append(obj[0])
        projectsToBuild.extend(tmpToBuild)
    else:
        projectsToBuild.extend(tmpToBuild)

    return sorted(list(set(projectsToBuild)))


def writeFile(modifiedProjects):
    with open("changes", "w") as f:
        for project in modifiedProjects:
            f.write("{}\n".format(project))


if __name__ == '__main__':
    conf = loadConfig()
    modifiedProjects = detectChanges(conf)
    writeFile(modifiedProjects)
