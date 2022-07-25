# pil_printer
## Introduction
With the *pil_printer* module it is possible to print a PIL image or several PIL images to a printer.
The most common use case is to print JPG or PNG file(s) at an exact point with an exact scaling.
Most graphics programs don't support exact placement and the user has nearly always to
manually control this placement/scaling for each image.

## Restrictions
*pil_printer* only works under Windows.

## Installation
The *pil_printer* module consists of one file: pil_printer.py which should be copied to the
current working directory or any directory in the sys.path.

It might be necessary to install win32print, win32ui and Pillow.

## Usage / examples
In order to use *pil_printer*, just put
```
from pil_printer import pil_printer, spec
```
at the top of your program.

If want to print the file `a.jpg` to the printer, scaled to 10 cm wide, use
```
image = "a.jpg"
pil_printer(image, width=10)
```
The image will be printed centered on the page.

If you want to offset the image by 5 cm to the right and 10 cm up, use
```
pil_printer("a.jpg", width=10, horizontal_offset=5, vertical_offset=-10)
```
Instead of using cm as the unit, you also use inch:
```
pil_printer("a.jpg", width=4, horizontal_offset=2, vertical_offset=-4, unit="inch")
```
By default, pil_printer uses the default printer, but with the printer argument,
any printer can be selected:
```
pil_printer("a.jpg", width=10, printer="EPSON WF-3725")
```
The image parameter doesn't have to be a filename. It can also be a PIL image, either
created by loading a file or using PIL primitives:
```
from pil_printer import pil_printer, spec
from PIL import ImageDraw
im = Image.new(mode="RGBA", size=(1000, 1000), color=(255, 255, 255))
d = ImageDraw.Draw(im=im)
d.rectangle(xy=(100, 100, 900, 900), outline=(0, 0, 0))
pil_printer(im)
```
So far, we've just printed one image on a page.
Instead of the image parameter, however multiple files/images may be specified:
```
pil_printer("a.jpg", "b.jpg", width=10)
```
*This is usually not what is wanted as all images are printed with the same scaling/positioning.*

In order to print multiple images with different scaling/postioning, the spec function can be used:
```
pil_printer(spec("a.jpg", width=10, horizontal_offset=-5), spec("b.jpg", width=5, horizontal_offset=5))
```
The spec parameters override the pil_printer parameters.

**Note that it is required to specify either width or height, but never both!**

## Reference
```
def pil_printer(*image, width=None, height=None, horizontal_offset=0, vertical_offset=0, unit="cm", printer_name=None):

    Prints a PIL image to a printer
    
    Parameters
    ----------
    image : PIL image
        Image to be printed
        Or it is possible to specify many images.
        However this nearly always requires the images to be given
        as a spec, in order to set offset(s) and possibly height/width
        
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
```

```
def spec(image, width=None, height=None, horizontal_offset=None, vertical_offset=None, unit=None):

    Prepares an image to be printed with custom properties
    
    Parameters
    ----------
    image : PIL image
        Image(s) to be used
        
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
        Must be cm or inch
        
    Returns
    -------
    spec : dict
        to be used as image in call to pil_printer
```


