import os.path

from django.core.management.base import BaseCommand

from experiment.models import Experiment


class Command(BaseCommand):
    help = 'Creates a new experiment rules class'

    def handle(self, *args, **options):
        # Ask for the experiment name
        experiment_rules_set_name = input("What is the name of your experiment rule set? (ex. Musical Preferences): ")

        # Create the experiment rule class
        success = self.create_experiment_rule_class(experiment_rules_set_name)

        if not success:
            return

        # Add the new experiment to ./experiment/rules/__init__.py
        self.register_experiment_rule(experiment_rules_set_name, './experiment/rules/__init__.py')

        # Create a basic test file for the experiment
        self.create_test_file(experiment_rules_set_name)

        # Ask if the user wants to create a new experiment with the same name (yes/no)
        create_experiment = input("Do you want to create a new experiment with the same name? (yes/no): ")

        if create_experiment.lower() == 'yes' or create_experiment.lower() == 'y':
            self.stdout.write(self.style.WARNING("Creating a new experiment..."))
            Experiment.objects.create(
                name=experiment_rules_set_name, 
                rules=experiment_rules_set_name,
                slug=experiment_rules_set_name.lower().replace(' ', '_')
            )

    def create_experiment_rule_class(self, experiment_rules_set_name):
        # Get the experiment name in different cases
        experiment_rules_set_name_snake_case, experiment_rules_set_name_snake_case_upper, experiment_rules_set_name_pascal_case = self.get_experiment_rules_set_name_cases(experiment_rules_set_name)

        # Create a new file for the experiment class
        filename = f"./experiment/rules/{experiment_rules_set_name_snake_case}.py"

        # Check if the file already exists
        if os.path.isfile(filename):
            self.stdout.write(self.style.ERROR(f"Experiment {experiment_rules_set_name} already exists. Exiting without creating file(s)."))
            return

        # Create the file by copying ./experiment/management/commands/templates/experiment.py
        with open(filename, 'w') as f:
            with open('./experiment/management/commands/templates/experiment.py', 'r') as template:
                f.write(template.read()
                    .replace('NewExperiment', experiment_rules_set_name_pascal_case)
                    .replace('new_experiment', experiment_rules_set_name_snake_case)
                    .replace('NEW_EXPERIMENT', experiment_rules_set_name_snake_case_upper)
                    .replace('New Experiment', experiment_rules_set_name.title())
                )

        self.stdout.write(self.style.SUCCESS(f"Created {filename} for experiment {experiment_rules_set_name}"))

        return True

    def register_experiment_rule(self, experiment_rules_set_name, file_path):

        # Get the experiment name in different cases
        experiment_rules_set_name_snake_case, experiment_rules_set_name_snake_case_upper, experiment_rules_set_name_pascal_case = self.get_experiment_rules_set_name_cases(experiment_rules_set_name)

        # New lines to add
        new_import = f"from .{experiment_rules_set_name_snake_case} import {experiment_rules_set_name_pascal_case}\n"
        new_dict_entry = f"    {experiment_rules_set_name_pascal_case}.ID: {experiment_rules_set_name_pascal_case},\n"

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

        self.stdout.write(self.style.SUCCESS(f"Registered {experiment_rules_set_name} in {file_path}"))

    def create_test_file(self, experiment_rules_set_name):
        # Get the experiment name in different cases
        experiment_rules_set_name_snake_case, experiment_rules_set_name_snake_case_upper, experiment_rules_set_name_pascal_case = self.get_experiment_rules_set_name_cases(experiment_rules_set_name)

        # Create a new file for the experiment class
        filename = f"./experiment/rules/tests/test_{experiment_rules_set_name_snake_case}.py"

        # Check if the file already exists
        if os.path.isfile(filename):
            self.stdout.write(self.style.ERROR(f"File {filename} already exists. Exiting without creating file."))
            return

        # Create the file by copying ./experiment/management/commands/templates/experiment.py
        with open(filename, 'w') as f:
            with open('./experiment/management/commands/templates/test_experiment.py', 'r') as template:
                f.write(template.read()
                    .replace('NewExperiment', experiment_rules_set_name_pascal_case)
                    .replace('new_experiment', experiment_rules_set_name_snake_case)
                    .replace('NEW_EXPERIMENT', experiment_rules_set_name_snake_case_upper)
                    .replace('New Experiment', experiment_rules_set_name.title())
                )

        self.stdout.write(self.style.SUCCESS(f"Created {filename} for experiment {experiment_rules_set_name}"))

    def get_experiment_rules_set_name_cases(self, experiment_rules_set_name):
        # Convert experiment name to snake_case and lowercase every word and replace spaces with underscores
        experiment_rules_set_name_snake_case = experiment_rules_set_name.lower().replace(' ', '_')
        experiment_rules_set_name_snake_case_upper = experiment_rules_set_name_snake_case.upper()

        # Convert experiment name to PascalCase and capitalize every word and remove spaces
        experiment_rules_set_name_pascal_case = experiment_rules_set_name.title().replace(' ', '')

        return experiment_rules_set_name_snake_case, experiment_rules_set_name_snake_case_upper, experiment_rules_set_name_pascal_case
