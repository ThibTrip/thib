import base64
import os
from bs4 import BeautifulSoup, NavigableString
from plumbum import cli
from loguru import logger


# # Helpers

# +
def get_data_string(src):
    src_lower = src.lower()
    is_path = src and not ('http' in src_lower or 'www' in src_lower)
    if is_path:
        logger.info(f'Getting data string for "{src}"')
        media_type = os.path.splitext(src_lower)[-1].lstrip('.').replace('jpg', 'jpeg').replace('svg', 'svg+xml')

        # keep the default FileNotFoundError if the file does note exist that's OK
        with open(src, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        # convert to bytes in the HTML code
        data_string = f"data:image/{media_type};charset=utf-8;base64,"+encoded_string.decode('utf-8')
        return data_string
    else:
        return None

def is_image_tag(tag):
    if tag.name == 'img':
        return True
    elif tag.name == 'link':
        type_ = getattr(tag, 'type', '')
        return isinstance(type_, str) and type_.startswith('image')
    else:
        return False


# -

# # CLI app

# +
class ImageEmbedder(cli.Application):
    """
    Embeds local images in an HTML file (the app will look for
    local image paths and open them and use bytes instead of
    the path).

    The original HTML file will be **overwritten** with embedded
    images.

    ToDo: since this script is doing more than just embedding images
    now might as well create a command that also export slides from
    a notebook.

    Parameters
    ----------
    html_file : str
        Path to an HTML file

    Examples
    --------
    $ python embed_images.py test.html
    """
    def main(self, html_file, favicon_path=None, page_title=None):

        # parse HTML file
        logger.info(f'Opening the file "{html_file}"')
        if not os.path.isfile(html_file):
            raise FileNotFoundError(f'No file found at path "{html_file}"')
        soup = BeautifulSoup(open(html_file, encoding='utf-8'), features='html.parser')

        # get all images
        imgs = soup.findAll(is_image_tag)

        # embed images by putting bytes into the HTML code
        for img in imgs:
            # check src and href attr
            for attr in ('src', 'href'):
                attr_val = img.get(attr, '')
                data_string = get_data_string(attr_val)
                if data_string:
                    img[attr] = data_string

        # add favicon
        if favicon_path:
            favicon_data_string = get_data_string(favicon_path)
            new_tag = soup.new_tag('link', rel='icon', type='image/png', href=favicon_data_string, sizes='32*32')
            soup.head.insert(0, new_tag)

        # add title
        if page_title:
            new_title = soup.new_tag('title')
            new_title.insert(0, NavigableString(page_title))
            soup.title.replace_with(new_title)

        # save modified HTML code
        logger.info(f'Overwriting the file "{html_file}"')
        with open(html_file, "w", encoding='utf-8') as file:
            file.write(str(soup))
        
if __name__ == "__main__":
    ImageEmbedder.run()
