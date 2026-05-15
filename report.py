import datetime


def save_report(content, output_path='review_output.md'):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(output_path, 'w') as f:
        f.write(f'# Code Review Report\n')
        f.write(f'**Generated:** {timestamp}\n\n')
        f.write(content)

    print(f'Report saved to {output_path}')
    return output_path

    


