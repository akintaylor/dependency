import sys
import typing

DEPENDENCY_GRAPH = {}

DEPENDENCY_KEYWORD = 'DEPEND'
INSTALL_KEYWORD = 'INSTALL'
REMOVE_KEYWORD = 'REMOVE'
LIST_KEYWORD = 'LIST'
END_KEYWORD = 'END'

INSTALLED_PACKAGES = set()


def parse_file(file_path):
    """
    Parse dependency installation file
    :param file_path: Path to file
    :return: 0/1
    """

    with open(file_path, 'r') as f:
        commands = f.readlines()

    for command in commands:
        command = command.strip()
        print(command)
        command_list = command.split()

        command_name = command_list.pop(0)

        if command_name == LIST_KEYWORD:
            print_installed_packages()
            continue

        if command_name == END_KEYWORD:
            continue

        package, dependencies = command_list[0], command_list[1:]

        if command_name == DEPENDENCY_KEYWORD:
            build_dependency_graph(package, dependencies)

        elif command_name == INSTALL_KEYWORD:

            if package in INSTALLED_PACKAGES:

                message = f'    {package} already installed'
                print(message)

            else:

                deps = get_dependencies(package)

                if not deps:
                    message = f'    {package} successfully installed'
                    INSTALLED_PACKAGES.add(package)
                    print(message)
                else:
                    pass


def print_installed_packages():
    for package in INSTALLED_PACKAGES:
        print(package)


def install_dependencies_recursively(package):
    dependencies = get_dependencies(package)

    if not dependencies:
        if package in INSTALLED_PACKAGES:
            message = f'    {package} already installed'

        return

    else:
        pass


def get_dependencies(package_name) -> typing.Union[list, None]:
    """

    :param package_name:
    :return:
    """
    try:
        dependencies = DEPENDENCY_GRAPH[package_name]['dep']
    except KeyError:
        return None

    return dependencies


def build_dependency_graph(package_name, dependencies):
    """

    :return:
    """

    dependencies.reverse()

    for dep in dependencies:
        if dep in DEPENDENCY_GRAPH:
            DEPENDENCY_GRAPH[dep]['refs'] += 1
        else:
            DEPENDENCY_GRAPH[dep] = {
                'dep': [],
                'refs': 1
            }

    if package_name in DEPENDENCY_GRAPH:
        DEPENDENCY_GRAPH[package_name] = {
            'dep': dependencies,
            'refs': DEPENDENCY_GRAPH[package_name]['refs']
        }
    else:
        DEPENDENCY_GRAPH[package_name] = {
            'dep': dependencies,
            'refs': 0
        }


def run():
    """

    :return:
    """

    parse_file()


if __name__ == '__main__':
    try:
        file_path = sys.argv[1]
    except IndexError:
        raise FileNotFoundError('No File Path')

    parse_file(file_path=file_path)
