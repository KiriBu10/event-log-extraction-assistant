'''
    Description: script to generate one parallel coordinate
    chart per DB considering all available versions.
'''
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
import numpy as np

db_options = ['RunningExample-V', 'paperj-V', 'UWV-V', 'BPI2016-V']
metric_options = ['precision', 'recall', 'f1']
relaxed_options = ['', 'relaxed_']



def plot_parallel_coordinates(db_name, metric, relaxed):
    data = []
    parent_folder = '../testDBs'

    for folder in os.listdir(parent_folder):
        if folder.startswith(db_name):
            folder_path = os.path.join(parent_folder, folder, 'results')
            if os.path.exists(folder_path):
                for file in os.listdir(folder_path):
                    if file.endswith('_METRICS.txt'):
                        parts = file.split('_')
                        prompt_name = parts[1]  # Extract prompt name
                        file_path = os.path.join(folder_path, file)
                        try:
                            with open(file_path, 'r') as f:
                                file_content = f.read().strip()
                                if file_content:
                                    file_content = file_content.replace("'", '"')
                                    metrics = json.loads(file_content)
                                    metric_value = metrics[relaxed + metric]
                                    data.append({
                                        'Folder': folder,
                                        'Prompt': prompt_name,
                                        metric: metric_value
                                    })
                                else:
                                    print(f"Warning: {file_path} is empty.")
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON in file {file_path}: {e}")
                        except Exception as e:
                            print(f"Unexpected error processing file {file_path}: {e}")

    df = pd.DataFrame(data)

    print(df)

    # Pivot the DataFrame to have folders as rows and prompt names as columns
    pivot_df = df.pivot(index='Folder', columns='Prompt', values=metric).reset_index()

    # Fill NaN values with -1
    pivot_df = pivot_df.fillna(-0.2)

    # Define line styles for accessibility
    line_styles = [':', '--', '-', '-.', ':', (0, (3, 5, 1, 5)), (0, (5, 10))]

    # Plot parallel coordinates
    plt.figure(figsize=(12, 6))
    for i, (idx, row) in enumerate(pivot_df.iterrows()):
        plt.plot(row.drop('Folder').values, label=row['Folder'], linewidth=3, linestyle=line_styles[i % len(line_styles)], color='black')

    # Adjust feature names (x-axis labels)
    plt.xticks(range(len(pivot_df.columns) - 1), pivot_df.columns[1:], rotation=6, ha='right', fontname='Times New Roman', fontsize=12)

    # Adjust other font properties
    plt.title('Parallel Coordinates Plot of ' + relaxed + metric + ' by Prompt', fontname='Times New Roman', fontsize=16)
    plt.xlabel('Prompts', fontname='Times New Roman', fontsize=14)
    plt.ylabel(relaxed + metric, fontname='Times New Roman', fontsize=14)

    # Set y-axis increments from -0.2 to 1.0 and replace -0.2 by
    # infinite to represent the Error generating the SQL
    ax = plt.gca()
    ax.set_yticks(np.arange(-0.2, 1.2, 0.2))
    y_labels = ax.get_yticks().tolist()
    y_labels = ['−∞' if label == -0.2 else f'{label:.1f}' for label in y_labels]
    ax.set_yticklabels(y_labels)

    # Adjust legend font properties and position
    plt.legend(loc='upper left', fontsize=12, frameon=True, fancybox=True, facecolor='white', framealpha=1, prop={'family': 'Times New Roman'})
    plt.grid(True)

    # Save the plot as a PDF file
    plt.savefig('plot-' + db_name + '-' + relaxed + metric + '.pdf', format='pdf')

    #plt.show()



for db in db_options:
    for metric in metric_options:
        for relaxed in relaxed_options:
            plot_parallel_coordinates(db, metric, relaxed)
