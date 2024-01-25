import os.path

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates a new experiment rules class'

    def handle(self, *args, **options):
        # Ask for the experiment name
        experiment_name = input("What is the name of your experiment? (ex. Musical Preferences): ")

        # Create the experiment rule class
        self.create_experiment_rule_class(experiment_name)

        # Add the new experiment to ./experiment/rules/__init__.py
        self.register_experiment_rule(experiment_name, './experiment/rules/__init__.py')

        # Create a basic test file for the experiment
        self.create_test_file(experiment_name)

    def create_experiment_rule_class(self, experiment_name):
        # Get the experiment name in different cases
        experiment_name_snake_case, experiment_name_snake_case_upper, experiment_name_pascal_case = self.get_experiment_name_cases(experiment_name)

        # Create a new file for the experiment class
        filename = f"./experiment/rules/{experiment_name_snake_case}.py"

        # Check if the file already exists
        if os.path.isfile(filename):
            # Warn the user that the file already exists and ask if they want to overwrite it
            self.stdout.write(self.style.WARNING(f"File {filename} already exists"))
            overwrite = input(f"Do you want to overwrite it? (y/n): ")

            # If the user does not want to overwrite the file, exit the command
            if overwrite.lower() != 'y':
                self.stdout.write(self.style.WARNING(f"File {filename} was not created"))
                return
            else:
                self.stdout.write(self.style.WARNING(f"File {filename} will be overwritten"))

        # Create the file by copying ./experiment/management/commands/templates/experiment.py
        with open(filename, 'w') as f:
            with open('./experiment/management/commands/templates/experiment.py', 'r') as template:
                f.write(template.read()
                    .replace('NewExperiment', experiment_name_pascal_case)
                    .replace('new_experiment', experiment_name_snake_case)
                    .replace('NEW_EXPERIMENT', experiment_name_snake_case_upper)
                    .replace('New Experiment', experiment_name.title())
                )

        self.stdout.write(self.style.SUCCESS(f"Created {filename} for experiment {experiment_name}"))

    def register_experiment_rule(self, experiment_name, file_path):

        # Get the experiment name in different cases
        experiment_name_snake_case, experiment_name_snake_case_upper, experiment_name_pascal_case = self.get_experiment_name_cases(experiment_name)

        # New lines to add
        new_import = f"from .{experiment_name_snake_case} import {experiment_name_pascal_case}\n"
        new_dict_entry = f"    {experiment_name_pascal_case}.ID: {experiment_name_pascal_case},\n"

        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Find the line to insert the new import, maintaining alphabetical order
        import_index = next(i for i, line in enumerate(lines) if line.startswith('from .') and line > new_import)
        lines.insert(import_index, new_import)

        # Find the line to insert the new dictionary entry, maintaining alphabetical order within the EXPERIMENT_RULES
        dict_start_index = lines.index("EXPERIMENT_RULES = {\n") + 1  # Start after the opening brace
        dict_end_index = lines.index("}\n", dict_start_index)  # Find the closing brace
        dict_entry_index = next((i for i, line in enumerate(lines[dict_start_index:dict_end_index], dict_start_index) if line > new_dict_entry), dict_end_index)
        lines.insert(dict_entry_index, new_dict_entry)

        # Write the modified lines back to the file
        with open(file_path, 'w') as file:
            file.writelines(lines)

        self.stdout.write(self.style.SUCCESS(f"Registered {experiment_name} in {file_path}"))

    def create_test_file(self, experiment_name):
        # Get the experiment name in different cases
        experiment_name_snake_case, experiment_name_snake_case_upper, experiment_name_pascal_case = self.get_experiment_name_cases(experiment_name)

        # Create a new file for the experiment class
        filename = f"./experiment/rules/tests/test_{experiment_name_snake_case}.py"

        # Check if the file already exists
        if os.path.isfile(filename):
            # Warn the user that the file already exists and ask if they want to overwrite it
            self.stdout.write(self.style.WARNING(f"File {filename} already exists"))
            overwrite = input(f"Do you want to overwrite it? (y/n): ")

            # If the user does not want to overwrite the file, exit the command
            if overwrite.lower() != 'y':
                self.stdout.write(self.style.WARNING(f"File {filename} was not created"))
                return
            else:
                self.stdout.write(self.style.WARNING(f"File {filename} will be overwritten"))

        # Create the file by copying ./experiment/management/commands/templates/experiment.py
        with open(filename, 'w') as f:
            with open('./experiment/management/commands/templates/test_experiment.py', 'r') as template:
                f.write(template.read()
                    .replace('NewExperiment', experiment_name_pascal_case)
                    .replace('new_experiment', experiment_name_snake_case)
                    .replace('NEW_EXPERIMENT', experiment_name_snake_case_upper)
                    .replace('New Experiment', experiment_name.title())
                )

        self.stdout.write(self.style.SUCCESS(f"Created {filename} for experiment {experiment_name}"))

    def get_experiment_name_cases(self, experiment_name):
        # Convert experiment name to snake_case and lowercase every word and replace spaces with underscores
        experiment_name_snake_case = experiment_name.lower().replace(' ', '_')
        experiment_name_snake_case_upper = experiment_name_snake_case.upper()

        # Convert experiment name to PascalCase and capitalize every word and remove spaces
        experiment_name_pascal_case = experiment_name.title().replace(' ', '')

        return experiment_name_snake_case, experiment_name_snake_case_upper, experiment_name_pascal_case
