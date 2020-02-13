from os import path, walk

import click
import hurry.filesize


def get_size(dir):
    result = 0

    for dirname, dirs, files in walk(dir):
        try:
            result += sum(path.getsize(
                path.join(dirname, file)
            ) for file in files)
        except FileNotFoundError:
            pass

    return result


@click.command()
@click.option('--include-hidden', is_flag=True, default=False)
@click.option('--match', 'matches', default=['node_modules'], multiple=True)
@click.argument('entry', type=click.Path(exists=True))
def main(entry: click.Path, include_hidden, matches):
    result = {match: 0 for match in matches}

    for dirname, dirs, files in walk(entry):
        for current_dir in dirs:
            if current_dir in matches:
                current_path = path.join(dirname, current_dir)
                size = get_size(current_path)
                result[current_dir] += size
                print(current_path, hurry.filesize.size(size))

        for current_dir in dirs:
            if (
                current_dir.startswith('.') and
                not include_hidden
            ) or current_dir in matches:
                dirs.remove(current_dir)

    total = sum(result.values())

    if total:
        print()

    for match, size in result.items():
        print(match, hurry.filesize.size(size))

    print('Total', hurry.filesize.size(total))


if __name__ == "__main__":
    main()
