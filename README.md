# LightMeter
A tool for RoboFont for calculating gray levels at any point in a glyph.

![LightMeter Screenshot](https://github.com/LettError/LightMeter/blob/master/LightMeterScreenshot.png)

Drag the tool over parts of a glyph to see the gray levels. The number in the blue box is a percentage.

* Airy disk blurring is caused by diffraction in the eye. It is independent of focus, other factors also contribute, these are not part of this tool.
* This blurring is small, but still typographically significant.
* This code uses its own convolution kernel. It does not generate or process a bitmap. 
* Some tools for calculating the diameter of the Airy disk are in scaleTools.py
* For each measurement the tool has to do a fair number of calculations. Works fine on a Mid 2014 MacBook Pro, but might be slower on older machines. Increase the chunkSize in the source if necessary.

## Example

Suppose we are looking at 8 pt type from 40 cm, the angular size for the em is 24.26' arcminutes. [See on sizecalc.com](http://sizecalc.com/#distance=400millimeters&physical-size=8points&perceived-size-units=arcminutes). Also suppose the em for this font is 1000 units. 

<table>
<tr>
<td>Pupilsize (mm)</td><td>Airy disc diameter (arcminutes)</td><td>(upm * angular size Airy diameter) / angular size em (em units)</td>
</tr>

<tr>
<td> 8.2</td><td>0.658</td><td>27.13</td>
</tr>


<tr>
<td> 1</td><td>4.494</td><td>185.28</td>
</tr>
</table>

Airy disk diameter data from Review of Basic Principles in Review of Basic Principles in Optics, Wavefront and Wavefront Error by Austin Roorda, Ph.D. University of California, Berkeley. http://roorda.vision.berkeley.edu.

## So what does it mean?
These numbers can be an indication about the physical limits of vision. As these calculations seem to show, letterforms at reading size and distance are at a scale where this kind of blurring is significant.

## Controls
* arrow up: increase diameter
* arrow down: decrease diameter
* c: clear trail
* t: toggle trail
* p: toggle grid
* i: invert

## To do
* wire up sliders for eye distance, typesize and pupil size.
* add support for non-circular kernels. 
