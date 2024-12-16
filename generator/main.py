"""
Generate html from a template file
"""

from pathlib import Path

current_dir = Path(__file__).parent

dest_dir = current_dir / 'results'
template_path = current_dir / 'templates' / 'base_bootstrap.txt'

def generate_html_file(
        file_name: str,
        page_title: str,
        movie_url: str,
        detail_text: str,
        previous_url: str,
        next_url: str,
) -> None:
    """
    Generate a html file from templates/work.txt by replacing the portion enclosed in braces
    """
    output_path = dest_dir / f'{file_name}.html'

    try:
        template_content = template_path.read_text(encoding='utf-8')

        final_content = template_content.replace('{page_title}', page_title)
        final_content = final_content.replace('{movie_url}', movie_url)
        final_content = final_content.replace('{detail_text}', detail_text)
        if previous_url == '':
            final_content = final_content.replace('{previous_page_url}', '')
        else:
            # previous_page_url = f'<a href="{previous_url}" class="button is-primary">Previous</a>'
            previous_page_url = f'<a href="{previous_url}" class="btn btn-primary">Previous</a>'
            final_content = final_content.replace('{previous_page_url}', previous_page_url)
        if next_url == '':
            final_content = final_content.replace('{next_page_url}', '')
        else:
            # next_page_url = f'<a href="{next_url}" class="button is-primary">Next</a>'
            next_page_url = f'<a href="{next_url}" class="btn btn-primary">次へ</a>'
            final_content = final_content.replace('{next_page_url}', next_page_url)

        output_path.write_text(final_content, encoding='utf-8')
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_path}")
    except Exception as e:
        print(f"Error occurred while generating file: {str(e)}")


def generate_html_files():
    """
    Generate html files from templates/base.txt by replacing the portion enclosed in braces
    """
    base_dir = current_dir / 'work'
    if not base_dir.exists():
        print(f"Error: Template directory '{base_dir}' does not exist")
        raise FileNotFoundError

    work_dirs = sorted([file for file in base_dir.glob('*') if not file.is_file()], key=lambda x: x.name)

    info_dict_list = []
    for work_dir in work_dirs:
        page_title_file = work_dir / 'page_title.txt'
        movie_url_file = work_dir / 'movie_url.txt'
        detail_text_file = work_dir / 'detail_text.txt'
        previous_url_file = work_dir / 'previous_url.txt'
        next_url_file = work_dir / 'next_url.txt'
        info_dict_list.append(
            {
                'file_name': work_dir.name,
                'page_title': page_title_file.read_text(encoding='utf-8').strip(),
                'movie_url': movie_url_file.read_text(encoding='utf-8').strip(),
                'detail_text': detail_text_file.read_text(encoding='utf-8'),
                'previous_url': previous_url_file.read_text(encoding='utf-8').strip(),
                'next_url': next_url_file.read_text(encoding='utf-8').strip(),
            }
        )

    for info_dict in info_dict_list:
        print(info_dict['file_name'])
        generate_html_file(**info_dict)


if __name__ == "__main__":
    generate_html_files()
