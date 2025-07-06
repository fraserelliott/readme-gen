import argparse

#todo: create and instantiate my own objects for settings, template_gen and readme_gen

parser = argparse.ArgumentParser()
parser.add_argument("--settings", action="store_true", help="Open settings configuration")
parser.add_argument("--template", action="store_true", help="Open template wizard")
parser.add_argument("--regenerate", action="store_true", help="Open regeneration wizard")
args = parser.parse_args()

if args.settings:
    print("Not yet implemented.") #settings.cli()
elif args.template:
    print("Not yet implemented.") #template_gen.cli()
elif args.regenerate:
    print("Not yet implemented.") #readme_gen.cli(path_to_template)
else:
    print("Not yet implemented.") #readme_gen.cli()