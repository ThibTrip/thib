import base64
import os
from bs4 import BeautifulSoup
from plumbum import cli
from loguru import logger


# # CLI app

# +
class ImageEmbedder(cli.Application):
    """
    Embeds local images in an HTML file (the app will look for
    local image paths and open them and use bytes instead of
    the path).

    The original HTML file will be **overwritten** with embedded
    images.

    For help on how to use the script execute "python embed_images.py --help"
    in a terminal.
    """
    def main(self, html_file):

        # parse HTML file
        logger.info(f'Opening the file "{html_file}"')
        if not os.path.isfile(html_file):
            raise FileNotFoundError(f'No file found at path "{html_file}"')
        soup = BeautifulSoup(open(html_file, encoding='utf-8'), features='html.parser')

        # get all images, resolve paths and embed images by putting bytes into the HTML code
        imgs = soup.findAll('img')

        for img in imgs:
            src = img.get('src', '')
            src_lower = src.lower()
            is_path = src and not ('http' in src_lower or 'www' in src_lower)
            if is_path:
                logger.info(f'Embedding image "{src}"')
                media_type = os.path.splitext(src_lower)[-1].lstrip('.').replace('jpg', 'jpeg').replace('svg', 'svg+xml')

                # keep the default FileNotFoundError if the file does note exist that's OK
                with open(src, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())

                # convert to bytes in the HTML code
                data_string = f"data:image/{media_type};charset=utf-8;base64,"+encoded_string.decode('utf-8')
                img['src'] = data_string

        # save modified HTML code
        logger.info(f'Overwriting the file "{html_file}"')
        with open(html_file, "w", encoding='utf-8') as file:
            file.write(str(soup))
        
if __name__ == "__main__":
    ImageEmbedder.run()
