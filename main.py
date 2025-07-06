import argparse
from readme_generator import ReadmeGenerator

#todo: create and instantiate my own objects for settings

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("--settings", action="store_true", help="Open settings configuration")
group.add_argument("--template", action="store_true", help="Open template wizard")
group.add_argument("--regenerate", action="store_true", help="Open regeneration wizard")
args = parser.parse_args()

if args.settings:
    print("Not yet implemented.") #settings.cli()
elif args.template:
    print("Not yet implemented.") #template_gen.cli()
elif args.regenerate:
    print("Not yet implemented.") #readme_gen.cli(path_to_template)
else:
    generator = ReadmeGenerator(None)
    generator.cli("test-files/template.md")