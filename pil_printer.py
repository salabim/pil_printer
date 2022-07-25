import win32print
import win32ui
from PIL import Image
from PIL import ImageWin
from pathlib import Path
import collections

"""
pil_printer

To be used to print a (or many) images to a printer.
Only Windows is supported.

Based on http://timgolden.me.uk/python/win32_how_do_i/print.html
"""
__version__ = "1.0.0"

def spec(image, width=None, height=None, horizontal_offset=None, vertical_offset=None, unit=None):
    """
    Prepares an image to be printed with custom properties
    
    Parameters
    ----------
    image : PIL image
        Image to be used
        
    width : float 
        Width of the printed image in the given unit
        Defaults to width given in call to pil_printer
        
    height : float 
        Height of  the printed image in the given unit
        Defaults to height given in call to pil_printer        
                    
    horizontal_offset : float
        Defaults to horizontal_offset given in call to pil_printer
        
    vertical_offset : float
        Defaults to vertical_offset given in call to pil_printer
        
    unit : str
        Defaults to unit given in call to pil_printer
        
    Returns
    -------
    spec : dict
        to be used as image in call to pil_printer
    """
    return dict(image=image, width=width, height=height, horizontal_offset=horizontal_offset, vertical_offset=vertical_offset, unit=unit)


def pil_printer(*image, width=None, height=None, horizontal_offset=0, vertical_offset=0, unit="cm", printer_name=None):
    """
    Prints a PIL image to a printer
    
    Parameters
    ----------
    image : PIL image
        Image to be printed
        Or it is possible to specify many images. However this nearly always requires 
        the images to be given as a spec, in order to set offset(s) and possibly height/width
        
    width : float 
        Width of the printed image in the given unit
        No default
        
    height : float 
        Height of  the printed image in the given unit
        No default
                    
    horizontal_offset : float
        Normally the image is printed centered on the page.
        With this parameter, the image can be offset horizontally
        Default: 0
        
    vertical_offset : float
        Normally the image is printed centered on the page.
        With this parameter, the image can be offset vertically
        Default: 0        
        
    unit : str
        Either 'cm' (default) or 'inch'

    printer : str
        Printer name to used
        Default: default printer

    Note
    ----
    One and only one of width/height has to be specified
    Only compatible with Windows platforms.
    """
    ImageInfo = collections.namedtuple("ImageInfo", "image x0 y0 x1 y1")

    LOGPIXELSX = 88
    LOGPIXELSY = 90

    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111

    if printer_name is None:
        printer_name = win32print.GetDefaultPrinter()

    image_infos = []
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)
    printer_size = hDC.GetDeviceCaps(PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)
    pixels_per_inch = hDC.GetDeviceCaps(LOGPIXELSX), hDC.GetDeviceCaps(LOGPIXELSY)

    width_default = width
    height_default = height
    horizontal_offset_default = horizontal_offset
    vertical_offset_default = vertical_offset
    unit_default = unit

    for image in image[:]:
        if isinstance(image, dict):
            width = width_default if image["width"] is None else image["width"]
            height = height_default if image["height"] is None else image["height"]
            horizontal_offset = horizontal_offset_default if image["horizontal_offset"] is None else image["horizontal_offset"]
            vertical_offset = vertical_offset_default if image["vertical_offset"] is None else image["vertical_offset"]
            unit = unit_default if image["unit"] is None else image["unit"]
            image = image["image"]
        else:
            width = width_default
            height = height_default
            horizontal_offset = horizontal_offset_default
            vertical_offset = vertical_offset_default
            unit = unit_default

        size = [None, None]
        if width is not None:
            size[0] = width

        if height is not None:
            size[1] = height

        if all(i_size is None for i_size in size):
            raise ValueError("neither width nor height specified")

        if not any(i_size is None for i_size in size):
            raise ValueError("width and he`ight specified")

        offset = [horizontal_offset, vertical_offset]

        if unit == "cm":
            inches_in_unit = 2.54
        elif unit == "inch":
            inches_in_unit = 1
        else:
            raise ValueError(f"unit should be 'cm' or 'inch', not {repr(unit)}")

        offset_in_pixels = [offset[i] * pixels_per_inch[i] / inches_in_unit for i in (0, 1)]

        if isinstance(image, (str, Path)):
            image = Image.open(image)

        if not isinstance(image, Image.Image):
            raise ValueError("image is not a proper Image.Image")

        for i in (0, 1):
            if size[i] is not None:
                scale = size[i] * pixels_per_inch[i] / image.size[i] / inches_in_unit

        scaled_width, scaled_height = [int(scale * i_size) for i_size in image.size]
        x0 = int(offset_in_pixels[0] + (printer_size[0] - scaled_width) / 2)
        y0 = int(offset_in_pixels[1] + (printer_size[1] - scaled_height) / 2)
        x1 = x0 + scaled_width
        y1 = y0 + scaled_height
        image_infos.append(ImageInfo(image, x0, y0, x1, y1))

    hDC.StartDoc("pil_printer")
    hDC.StartPage()

    for image_info in image_infos:
        dib = ImageWin.Dib(image_info.image)
        dib.draw(hDC.GetHandleOutput(), (image_info.x0, image_info.y0, image_info.x1, image_info.y1))

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()


if __name__ == "__main__":
    file_name = "a.jpg"
    im = file_name
    pil_printer(spec(im, horizontal_offset=2, width=10), spec(im, vertical_offset=10), width=5, horizontal_offset=0, vertical_offset=5, unit="cm")
