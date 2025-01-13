"""
Generate html from a template file
"""
import json
import os
from pathlib import Path

current_dir = Path(__file__).parent

dest_dir = current_dir / 'results'
template_detail_path = current_dir / 'templates' / 'base_detail.txt'
template_list_path = current_dir / 'templates' / 'base_list.txt'
template_contents_path = current_dir / 'templates' / 'base_contents_list.txt'


def generate_contents_list(
        thumbnail: str,
        file_name: str,
        page_title:str,
)->str:
    contents_list = template_contents_path.read_text(encoding='utf-8')
    replaced_list = contents_list.replace('{thumbnail}', thumbnail)
    replaced_list = replaced_list.replace('{file_name}', file_name)
    replaced_list = replaced_list.replace('{page_title}', page_title)
    return replaced_list


def generate_list_html_file(
        contents: str,
)->None:
    output_path = dest_dir / 'movie_list.html'

    try:
        template_content = template_list_path.read_text(encoding='utf-8')
        final_content = template_content.replace('{contents}', contents)
        output_path.write_text(final_content, encoding='utf-8')
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_list_path}")
    except Exception as e:
        print(f"Error occurred while generating file: {str(e)}")


def generate_detail_html_file(
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
        template_content = template_detail_path.read_text(encoding='utf-8')

        final_content = template_content.replace('{page_title}', page_title)
        final_content = final_content.replace('{movie_url}', movie_url)
        final_content = final_content.replace('{detail_text}', detail_text)
        if previous_url is None:
            final_content = final_content.replace('{previous_page_url}', '')
        else:
            previous_page_url = f'<a href="{previous_url}" class="btn btn-primary">Previous</a>'
            final_content = final_content.replace('{previous_page_url}', previous_page_url)
        if next_url is None:
            final_content = final_content.replace('{next_page_url}', '')
        else:
            next_page_url = f'<a href="{next_url}" class="btn btn-primary">次へ</a>'
            final_content = final_content.replace('{next_page_url}', next_page_url)

        output_path.write_text(final_content, encoding='utf-8')
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_detail_path}")
    except Exception as e:
        print(f"Error occurred while generating file: {str(e)}")


def generate_html_files():
    """
    Generate html files from templates/base.txt by replacing the portion enclosed in braces
    """
    work_dir = current_dir / 'work'
    if not work_dir.exists():
        print(f"Error: Template directory '{work_dir}' does not exist")
        raise FileNotFoundError

    json_file = work_dir / 'data.json'
    try:
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            print(f'Error: File not found: {json_file}')
    except json.JSONDecodeError:
        print(f'Error: File is not properly formatted: {json_file}')

    info_dict_list = []
    contents = ''
    for movie_id, page_data in data.items():
        detail_text_file = work_dir / movie_id / page_data['detail_text_file']
        detail_text = detail_text_file.read_text(encoding='utf-8')
        thumbnail = f'../work/{movie_id}/{page_data["thumbnail"]}'
        info_dict_list.append(
            {
                'file_name': movie_id,
                'page_title': page_data['page_title'],
                'movie_url': page_data['movie_url'],
                'detail_text': detail_text,
                'previous_url': page_data['previous_url'],
                'next_url': page_data['next_url'],
            }
        )

        add_contents = generate_contents_list(thumbnail, movie_id, page_data['page_title'])
        contents += add_contents

    for info_dict in info_dict_list:
        print(info_dict['file_name'])
        generate_detail_html_file(**info_dict)

    generate_list_html_file(contents)


if __name__ == "__main__":
    generate_html_files()
