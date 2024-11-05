from os.path import isfile, join

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a new block rules class'

    def handle(self, *args, **options):
        # Ask for the block name
        ruleset_name = input("What is the name of your block ruleset? (ex. Musical Preferences): ")

        # Create the block rule class
        success = self.create_block_rule_class(ruleset_name)

        if not success:
            return

        # Add the new block to ./experiment/rules/__init__.py
        self.register_experiment_rule(ruleset_name, './experiment/rules/__init__.py')

        # Create a basic test file for the block
        self.create_test_file(ruleset_name)

    def create_block_rule_class(self, ruleset_name):
        # Get the block name in different cases
        ruleset_name_snake_case, ruleset_name_snake_case_upper, ruleset_name_pascal_case = self.get_ruleset_name_cases(ruleset_name)

        # Create a new file for the block rules class
        filename = join(".", "experiment", "rules", f"{ruleset_name_snake_case}.py")

        # Check if the file already exists
        if isfile(filename):
            self.stdout.write(self.style.ERROR(f"Experiment block ruleset \"{ruleset_name}\" already exists. Exiting without creating file(s)."))
            return

        # Create the file by copying ./experiment/management/commands/templates/experiment.py
        with open(filename, 'w') as f:
            with open('./experiment/management/commands/templates/experiment.py', 'r') as template:
                f.write(template.read()
                    .replace('NewBlockRuleset', ruleset_name_pascal_case)
                    .replace('new_block_ruleset', ruleset_name_snake_case)
                    .replace('NEW_BLOCK_RULESET', ruleset_name_snake_case_upper)
                    .replace('New Block Ruleset', ruleset_name.title())
                )

        self.stdout.write(self.style.SUCCESS(f"Created {filename} for block ruleset \"{ruleset_name}\""))

        return True

    def register_experiment_rule(self, ruleset_name, file_path):

        # Get the experiment name in different cases
        ruleset_name_snake_case, ruleset_name_snake_case_upper, ruleset_name_pascal_case = self.get_ruleset_name_cases(ruleset_name)

        # New lines to add
        new_import = f"from .{ruleset_name_snake_case} import {ruleset_name_pascal_case}\n"
        new_dict_entry = f"    {ruleset_name_pascal_case}.ID: {ruleset_name_pascal_case},\n"

        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Find the line to insert the new import, maintaining alphabetical order
        import_index = next(i for i, line in enumerate(lines) if line.startswith('from .') and line > new_import)
        lines.insert(import_index, new_import)

        # Find the line to insert the new dictionary entry, maintaining alphabetical order within the BLOCK_RULES
        dict_start_index = lines.index("BLOCK_RULES = {\n") + 1  # Start after the opening brace
        dict_end_index = lines.index("}\n", dict_start_index)  # Find the closing brace
        dict_entry_index = next((i for i, line in enumerate(lines[dict_start_index:dict_end_index], dict_start_index) if line > new_dict_entry), dict_end_index)
        lines.insert(dict_entry_index, new_dict_entry)

        # Write the modified lines back to the file
        with open(file_path, 'w') as file:
            file.writelines(lines)

        self.stdout.write(self.style.SUCCESS(f"Registered ruleset \"{ruleset_name}\" in {file_path}"))

    def create_test_file(self, ruleset_name):
        # Get the block name in different cases
        ruleset_name_snake_case, ruleset_name_snake_case_upper, ruleset_name_pascal_case = self.get_ruleset_name_cases(ruleset_name)

        # Create a new file for the block class
        filename = join('.', 'experiment', 'rules', 'tests', 'test_' + ruleset_name_snake_case + '.py')

        # Check if the file already exists
        if isfile(filename):
            self.stdout.write(self.style.ERROR(f"File {filename} already exists. Exiting without creating file."))
            return

        # Create the file by copying ./experiment/management/commands/templates/experiment.py
        with open(filename, 'w') as f:
            with open('./experiment/management/commands/templates/test_experiment.py', 'r') as template:
                f.write(template.read()
                    .replace('NewBlockRuleset', ruleset_name_pascal_case)
                    .replace('new_block_ruleset', ruleset_name_snake_case)
                    .replace('NEW_BLOCK_RULESET', ruleset_name_snake_case_upper)
                    .replace('New Block Ruleset', ruleset_name.title())
                )

        self.stdout.write(self.style.SUCCESS(f"Created {filename} for experiment block {ruleset_name}"))

    def get_ruleset_name_cases(self, ruleset_name):
        # Convert block name to snake_case and lowercase every word and replace spaces with underscores
        ruleset_name_snake_case = ruleset_name.lower().replace(' ', '_')
        ruleset_name_snake_case_upper = ruleset_name_snake_case.upper()

        # Convert block name to PascalCase and capitalize every word and remove spaces
        ruleset_name_pascal_case = ruleset_name.title().replace(' ', '')

        return ruleset_name_snake_case, ruleset_name_snake_case_upper, ruleset_name_pascal_case
