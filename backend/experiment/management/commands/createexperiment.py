import os.path

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates a new experiment rules class'

    def handle(self, *args, **options):
        # Ask for the experiment name
        experiment_name = input("What is the name of your experiment? (ex. Musical Preferences): ")

        # Convert experiment name to snake_case and lowercase every word and replace spaces with underscores
        experiment_name_snake_case = experiment_name.lower().replace(' ', '_')
        experiment_name_snake_case_upper = experiment_name_snake_case.upper()

        # Convert experiment name to PascalCase and capitalize every word and remove spaces
        experiment_name_pascal_case = experiment_name.title().replace(' ', '')

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

        # Example of modifying an existing file by adding a line of text
        # existing_file = 'existing_file.py'  # Specify the correct path to the file you want to modify
        # with open(existing_file, 'a') as f:
        #     f.write(f"# Added experiment: {experiment_name}\n")

        # self.stdout.write(self.style.SUCCESS(f"Updated {existing_file}"))
