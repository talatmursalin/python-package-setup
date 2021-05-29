import os
import getpass
from pkgcli.utils import methods
from pkgcli.errors.error import SpecificationError

author = getpass.getuser()
curr_dir = os.getcwd()
file_dir = os.path.dirname(__file__)
set_up_template = methods.read_file(os.path.join(file_dir, 'templates', 'setup', 'setup_basic'))


# inputs

def input_package_name():
    name = input('package name: ')
    if len(name) == 0:
        raise SpecificationError('Package name can\'t be empty')
    if ' ' in name or '-' in name:
        print('White spaces and hyphens will be replaced with underscore')
        name = name.replace(' ', '_').replace('-', '_')
    # TODO add more validations
    return name


def input_version():
    default = '0.0.1'
    version = input('version({}): '.format(default))
    return version or default


def input_requirements():
    default = ''
    requirements = input('install requires(enter comma separated value or leave empty): ')
    # TODO put validations
    return requirements or default


def input_author():
    default = author
    pkg_author = input('author({}): '.format(default))
    return pkg_author or default


def input_email():
    default = '{}@mail.com'.format(author)
    email = input('email({}): '.format(default))
    # TODO put validations
    return email or default


def input_description():
    default = 'An awesome python package'
    description = input('description({}): '.format(default))
    return description or default

# input end


def create_bin_dir(root_dir):
    msg = 'Create bin dir?(Y/N default) :'
    choice = methods.input_binary_choice(msg)
    if choice:
        methods.make_dir(os.path.join(root_dir, 'bin'))


def add_changes_file(root_dir):
    methods.touch(os.path.join(root_dir, 'CHANGES.txt'))


def create_manifest_file(root_dir):
    msg = 'Create manifest file?(Y/N default) :'
    choice = methods.input_binary_choice(msg)
    if choice:
        methods.touch(os.path.join(root_dir, 'MANIFEST.in'))


def create_doc_dir(root_dir):
    msg = 'Create doc dir?(Y default/N) :'
    choice = methods.input_binary_choice(msg, default=True)
    if choice:
        methods.make_dir(os.path.join(root_dir, 'docs'))


def add_license_file(root_dir):
    content = methods.read_file(os.path.join(file_dir, 'templates', 'license', 'MIT'))
    methods.write_file(os.path.join(root_dir, 'LICENSE'), content)


def add_readme(root_dir, desc):
    methods.write_file(os.path.join(root_dir, 'README.md'), desc)


def add_gitignore(root_dir):
    msg = 'Add gitignore file?(Y default/N) :'
    choice = methods.input_binary_choice(msg, default=True)
    if choice:
        methods.copy_file(os.path.join(file_dir, 'templates', 'texts', 'gitignore'),
                          os.path.join(root_dir, '.gitignore'))


def update_setup_template(placeholder, value):
    global set_up_template
    set_up_template = set_up_template.replace(placeholder, value)


def create_setup_py(root_dir):
    methods.write_file(os.path.join(root_dir, 'setup.py'), set_up_template)


def create_structure(tmp_dir):
    package_name = input_package_name()
    methods.make_dir(os.path.join(tmp_dir, package_name))
    methods.touch(os.path.join(tmp_dir, package_name, '__init__.py'))
    methods.copy_file(os.path.join(file_dir, 'templates', 'code', 'main.py'), os.path.join(tmp_dir, package_name))
    update_setup_template('[placeholder_package_name]', package_name)

    v = input_version()
    update_setup_template('[placeholder_version]', v)

    pkg_author = input_author()
    update_setup_template('[placeholder_author]', pkg_author)

    email = input_email()
    update_setup_template('[placeholder_email]', email)

    description = input_description()
    update_setup_template('[placeholder_description]', description)
    add_readme(tmp_dir, description)

    # requirements = input_requirements()
    # update_setup_template('[placeholder_requirements]', requirements)

    create_doc_dir(tmp_dir)
    create_bin_dir(tmp_dir)
    add_changes_file(tmp_dir)
    create_manifest_file(tmp_dir)
    add_license_file(tmp_dir)
    add_gitignore(tmp_dir)
    create_setup_py(tmp_dir)
    return package_name


def main():
    tmp_dir = os.path.join(curr_dir, methods.random_dir_name())
    methods.make_dir(tmp_dir)
    try:
        pkg = create_structure(tmp_dir)
        methods.copy_everything(tmp_dir, curr_dir)
        success_txt = methods.read_file(os.path.join(file_dir, 'templates', 'texts', 'success'))
        success_txt = success_txt.replace('[placeholder_dir]', curr_dir).replace('[placeholder_package_name]', pkg)
        print(success_txt)
    except Exception as e:
        print(e)
    finally:
        methods.clear_everything(tmp_dir)


if __name__ == '__main__':
    main()
