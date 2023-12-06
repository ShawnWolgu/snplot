# SNPLOT
A python code to draw figures in scientific papers. Based on self plotting habits.

## Features
- Automatically load configuration
- Automatically applicate variant styles
- Can call interactive UI to do detailed adjustment

# Update Log
## Ver0.4
- Added a small status monitor. It can reflect reading or writing the config file and exporting the current image.
- Add colormap switch and change the cmap sequence by colorwheel
- Modified the paddings and tick length in default style to make it more like a common Nature style

## Ver0.3
- Fixed an issue with legends in linemarkdata (e.g., point, line, combination).
- Added support for defining single-group data in linemarkdata.
- Fixed a problem with the xtick parameter, which was causing an error in the expand_arg function. This parameter has been removed.
- Resolved an error that occurred when converting the axis to logarithmic due to issues with the xlim parameter. The issue arose when crossing the value of zero, as logarithmic coordinates must correspond to positive values.
- Replaced numerical controls with input boxes or used both for better control.
- Added an export button for easy direct exporting.
- Fixed a bug that occurred when reading the config file, where it did not match existing adjustable features.
- Implemented a control for enabling/disabling legends.
- Fixed issues with the colorbar.

## Ver0.2
- Add eulerdata type
- Add plot type: Pole figure and inverse pole figure tracks

## Ver0.1
- support simple scatter and line plots
- support a simple interactive UI based on custom_tkinter
- support line mark data
- support mark data with errorbar
- support mark data with color (filled or unfilled)
- Add config save and load buttons in UI
