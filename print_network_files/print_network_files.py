"""
This script browses a specified network location and performs several analyses:
1. Lists files older than two weeks and groups them by their root folder.
2. Generates statistics about the top 5 largest root folders and the sum of all other folders,
   including the count of files older than two weeks.
3. Plots a pie chart of the sizes of the top 5 root folders and the sum of other folders.
The results are saved in a text file and a Markdown (MD) file. The pie chart is inserted into the MD file,
which is then converted to HTML and opened in the default web browser.

Usage:
    python script_name.py --config /path/to/config.ini
    or
    python script_name.py --network_path /path/to/network/location --delete
"""

import os
import datetime
import argparse
import configparser
import markdown
import webbrowser
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import re  # Import the regular expression module


def parse_arguments():
    """
    Parse command line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=('Analyze network location for '
                     'old files and folder statistics.'))
    parser.add_argument('--config', type=str,
                        help='Path to the configuration file.')
    parser.add_argument('--network_path', type=str,
                        help='Path to the network location.')
    parser.add_argument('--delete', action='store_true',
                        help='Delete files listed after processing')
    return parser.parse_args()


def read_config(config_path):
    """
    Read network path from configuration file.

    Parameters
    ----------
    config_path : str
        Path to the configuration file.

    Returns
    -------
    str
        Network path from the configuration file.
    """
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['DEFAULT'].get('network_path')


def plot_folder_sizes(folder_sizes, output_path):
    labels = list(folder_sizes.keys())
    sizes = list(folder_sizes.values())

    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Folder Sizes of Files Older Than 2 Weeks")
    # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.axis('equal')

    pie_chart_filename = os.path.join(output_path, 'folder_sizes.png')
    plt.savefig(pie_chart_filename)
    return pie_chart_filename


def list_files_older_than_two_weeks(network_path, output_path):
    """
    Lists files in the given network path that are older than two weeks.

    Parameters
    ----------
    network_path : str
        Path to the network location.
    output_path : str
        Path to save the output files.

    Returns
    -------
    tuple
        Names of the output files (text file and MD file)
        and folder sizes dictionary.
    """
    two_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=2)
    all_files_to_delete = []
    folder_sizes = Counter()
    folder_file_counts = defaultdict(int)

    file_list = []
    for root, dirs, files in os.walk(network_path):
        root_folder = os.path.relpath(root, network_path).split(os.sep)[0]
        for file in files:
            file_path = os.path.join(root, file)
            file_stat = os.stat(file_path)
            creation_time = datetime.datetime.fromtimestamp(file_stat.st_ctime)
            if creation_time < two_weeks_ago:
                file_list.append(file_path)
                all_files_to_delete.append(file_path)
                folder_sizes[root_folder] += os.path.getsize(file_path)
                folder_file_counts[root_folder] += 1

    # Process folder sizes for top 5 and others
    top_5_folders = dict(folder_sizes.most_common(5))
    other_folders_size = sum(folder_sizes.values()) - \
        sum(top_5_folders.values())
    top_5_folders['Other Folders'] = other_folders_size

    # Count files for top 5 and others
    other_folders_file_count = (sum(folder_file_counts.values()) -
                                sum(folder_file_counts[folder]
                                    for folder in top_5_folders
                                    if folder != 'Other Folders'))
    top_5_folder_file_counts = {folder: folder_file_counts[folder]
                                for folder in top_5_folders
                                if folder != 'Other Folders'}
    top_5_folder_file_counts['Other Folders'] = other_folders_file_count

    # Write file list to output
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_list_filename = os.path.join(
        output_path, f"file_list_{timestamp}.txt")
    with open(file_list_filename, "w") as file:
        for file_path in file_list:
            file.write(f"{file_path}\n")
        file.write("\n")

    # Write MD file for top 5 largest folders
    md_filename = os.path.join(output_path, f"folder_stats_{timestamp}.md")
    with open(md_filename, "w") as md_file:
        md_file.write("# Folder Statistics (Files Older Than 2 Weeks)\n\n")
        md_file.write(
            "Note: 'Total size' refers to the size of files that are older than two weeks.\n\n")
        md_file.write("| Folder Name | Total Size | File Count |\n")
        md_file.write("|-------------|------------|------------|\n")
        for folder, size in top_5_folders.items():
            readable_size = convert_size(size)
            file_count = top_5_folder_file_counts[folder]
            md_file.write(f"| {folder} | {readable_size} | {file_count} |\n")
        md_file.write("\n\n")  # Add extra line breaks for separation
        md_file.write("## Folder Size Distribution\n\n")

    return file_list_filename, md_filename, top_5_folders, all_files_to_delete


def convert_md_to_html(md_filename, output_path):
    """
    Convert an MD file to an HTML file and open it in the default web browser.

    Parameters
    ----------
    md_filename : str
        Path to the Markdown file.
    output_path : str
        Path to save the HTML file.
    """
    with open(md_filename, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()
    html_content = markdown.markdown(
        md_content, extensions=['tables'])  # Convert Markdown to HTML

    # Add Bootstrap classes to the first table tag
    html_content = re.sub(
        r'<table>', '<table class="table table-striped table-hover">', html_content, 1)

    html_filename = os.path.splitext(md_filename)[0] + '.html'
    with open(html_filename, 'w', encoding='utf-8') as html_file:
        html_file.write('<!DOCTYPE html>\n')
        html_file.write('<html lang="en">\n<head>\n')
        html_file.write('<meta charset="UTF-8">\n')
        html_file.write(
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        html_file.write(
            '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">\n')
        html_file.write('</head>\n<body>\n')
        html_file.write('<div class="container">\n')
        html_file.write(html_content)
        html_file.write('\n</div>\n')
        html_file.write('</body>\n</html>')

    webbrowser.open_new_tab('file://' + os.path.realpath(html_filename))


def main(network_path, delete_after_creation):
    output_path = os.path.dirname(os.path.abspath(__file__))
    res = list_files_older_than_two_weeks(network_path, output_path)
    file_list_filename, md_filename, top_5_folders, all_files_to_delete = res

    pie_chart_filename = plot_folder_sizes(top_5_folders, output_path)
    with open(md_filename, 'a') as md_file:
        md_file.write(
            f"\n![Pie Chart of Folder Sizes](file://{pie_chart_filename})\n")

    convert_md_to_html(md_filename, output_path)

    if delete_after_creation:
        # Open the file list in the default text editor
        os.startfile(file_list_filename)
        response = input(
            f"Do you want to delete the listed files? "
            f"They have been listed in {file_list_filename}, "
            f"which has been opened in your default text editor. (y/n): ")
        if response.lower() == 'y':
            for file in all_files_to_delete:
                try:
                    os.remove(file)
                    print(f"Deleted {file}")
                except Exception as e:
                    print(f"Error deleting {file}: {e}")
            print("Listed files deleted.")
        else:
            print("Files not deleted.")


def convert_size(size_bytes):
    """
    Convert a size in bytes to a more readable format (KB, MB, GB).

    Parameters
    ----------
    size_bytes : int
        Size in bytes.

    Returns
    -------
    str
        Readable size format.
    """
    if size_bytes < 150:
        return f"{size_bytes} bytes"
    size_kb = size_bytes / 1024
    if size_kb < 150:
        return f"{size_kb:.2f} KB"
    size_mb = size_kb / 1024
    if size_mb < 150:
        return f"{size_mb:.2f} MB"
    size_gb = size_mb / 1024
    return f"{size_gb:.2f} GB"


if __name__ == "__main__":
    args = parse_arguments()
    network_path = args.network_path

    if args.config:
        config_network_path = read_config(args.config)
        if not network_path:
            network_path = config_network_path

    if network_path:
        main(network_path, args.delete)
    else:
        print("No network path provided. "
              "Please specify a network path.")
