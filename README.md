# LightMeter
A tool for RoboFont for calculating gray levels at any point in a glyph.

![LightMeter Screenshot](https://github.com/LettError/LightMeter/blob/master/LightMeterScreenshot.png)

Drag the tool over parts of a glyph to see the gray levels. The number in the blue box is a percentage.

* Airy disk blurring is caused by diffraction, independent of focus.
* This blurring is small, but still typographically significant.
* This code uses its own convolution kernel. It does not generate or process a bitmap. 
* Some tools for calculating the diameter of the Airy disk are in scaleTools.py

## Example
> 8 pt type, at 40 cm, the angular size for the em is 24.26' arcminutes

<table>
<tr>
<td>Pupilsize (mm)</td><td>Airy disc diameter (arcminutes)</td><td>em units</td>
</tr>

<tr>
<td> 8.2</td><td>0.658</td><td>27.13</td>
</tr>


<tr>
<td> 1</td><td>4.494</td><td>185.28</td>
</tr>
</table>

Airy disk diameter data from http://voi.opt.uh.edu/1_Roorda_OpticPrinciples.pdf

## To do
* wire up sliders for eye distance, typesize and pupil size.
* add support for non-circular kernels. 
