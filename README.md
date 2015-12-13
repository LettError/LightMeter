# LightMeter
A tool for RoboFont for calculating gray levels at any point in a glyph.

![LightMeter Screenshot](https://github.com/LettError/LightMeter/blob/master/LightMeterScreenshot.png)

Drag the tool over parts of a glyph to see the gray levels. The number in the blue box is a percentage.

* Airy disk blurring is caused by diffraction, independent of focus.
* This blurring is small, but still typographically significant
* Some tools for calculating the diameter of the Airy disk are in scaleTools.py

## Example
> 8 pt type, at 40 cm, the angular size for the em is 24.26' arcminutes
> Pupilsize, Airy disc diameter, em units
> 8.2 mm: 0.658' arcminutes, 27.13 em units
> 1 mm: 4.494' arcminutes, 185.28 em units

This code uses its own convolution kernel. It does not generate or process a bitmap. 

## To do
* wire up sliders for eye distance, typesize and pupil size.
* add support for non-circular kernels. 
