# -*- coding: utf-8 -*-
# -*- coding: utf8 -*-
"""Autogenerated file - DO NOT EDIT
If you spot a bug, please report it on the mailing list and/or change the generator."""

from nipype.interfaces.base import CommandLine, CommandLineInputSpec, SEMLikeCommandLine, TraitedSpec, File, Directory, traits, isdefined, InputMultiPath, OutputMultiPath
import os


class GradientAnisotropicDiffusionInputSpec(CommandLineInputSpec):
    conductance = traits.Float(desc="Conductance controls the sensitivity of the conductance term. As a general rule, the lower the value, the more strongly the filter preserves edges. A high value will cause diffusion (smoothing) across edges. Note that the number of iterations controls how much smoothing is done within regions bounded by edges.", argstr="--conductance %f")
    iterations = traits.Int(desc="The more iterations, the more smoothing. Each iteration takes the same amount of time. If it takes 10 seconds for one iteration, then it will take 100 seconds for 10 iterations. Note that the conductance controls how much each iteration smooths across edges.", argstr="--iterations %d")
    timeStep = traits.Float(desc="The time step depends on the dimensionality of the image. In Slicer the images are 3D and the default (.0625) time step will provide a stable solution.", argstr="--timeStep %f")
    inputVolume = File(position=-2, desc="Input volume to be filtered", exists=True, argstr="%s")
    outputVolume = traits.Either(traits.Bool, File(), position=-1, hash_files=False, desc="Output filtered", argstr="%s")


class GradientAnisotropicDiffusionOutputSpec(TraitedSpec):
    outputVolume = File(position=-1, desc="Output filtered", exists=True)


class GradientAnisotropicDiffusion(SEMLikeCommandLine):
    """title: Gradient Anisotropic Diffusion

category: Filtering.Denoising

description: Runs gradient anisotropic diffusion on a volume.

Anisotropic diffusion methods reduce noise (or unwanted detail) in images while preserving specific image features, like edges.  For many applications, there is an assumption that light-dark transitions (edges) are interesting.  Standard isotropic diffusion methods move and blur light-dark boundaries.  Anisotropic diffusion methods are formulated to specifically preserve edges. The conductance term for this implementation is a function of the gradient magnitude of the image at each point, reducing the strength of diffusion at edges. The numerical implementation of this equation is similar to that described in the Perona-Malik paper, but uses a more robust technique for gradient magnitude estimation and has been generalized to N-dimensions.

version: 0.1.0.$Revision: 19608 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/GradientAnisotropicDiffusion

contributor: Bill Lorensen (GE)

acknowledgements: This command module was derived from Insight/Examples (copyright) Insight Software Consortium

"""

    input_spec = GradientAnisotropicDiffusionInputSpec
    output_spec = GradientAnisotropicDiffusionOutputSpec
    _cmd = "GradientAnisotropicDiffusion "
    _outputs_filenames = {'outputVolume': 'outputVolume.nii'}


class CurvatureAnisotropicDiffusionInputSpec(CommandLineInputSpec):
    conductance = traits.Float(desc="Conductance controls the sensitivity of the conductance term. As a general rule, the lower the value, the more strongly the filter preserves edges. A high value will cause diffusion (smoothing) across edges. Note that the number of iterations controls how much smoothing is done within regions bounded by edges.", argstr="--conductance %f")
    iterations = traits.Int(desc="The more iterations, the more smoothing. Each iteration takes the same amount of time. If it takes 10 seconds for one iteration, then it will take 100 seconds for 10 iterations. Note that the conductance controls how much each iteration smooths across edges.", argstr="--iterations %d")
    timeStep = traits.Float(desc="The time step depends on the dimensionality of the image. In Slicer the images are 3D and the default (.0625) time step will provide a stable solution.", argstr="--timeStep %f")
    inputVolume = File(position=-2, desc="Input volume to be filtered", exists=True, argstr="%s")
    outputVolume = traits.Either(traits.Bool, File(), position=-1, hash_files=False, desc="Output filtered", argstr="%s")


class CurvatureAnisotropicDiffusionOutputSpec(TraitedSpec):
    outputVolume = File(position=-1, desc="Output filtered", exists=True)


class CurvatureAnisotropicDiffusion(SEMLikeCommandLine):
    """title: Curvature Anisotropic Diffusion

category: Filtering.Denoising

description: Performs anisotropic diffusion on an image using a modified curvature diffusion equation (MCDE).

MCDE does not exhibit the edge enhancing properties of classic anisotropic diffusion, which can under certain conditions undergo a 'negative' diffusion, which enhances the contrast of edges.  Equations of the form of MCDE always undergo positive diffusion, with the conductance term only varying the strength of that diffusion.

 Qualitatively, MCDE compares well with other non-linear diffusion techniques.  It is less sensitive to contrast than classic Perona-Malik style diffusion, and preserves finer detailed structures in images.  There is a potential speed trade-off for using this function in place of Gradient Anisotropic Diffusion.  Each iteration of the solution takes roughly twice as long.  Fewer iterations, however, may be required to reach an acceptable solution.

version: 0.1.0.$Revision: 19608 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/CurvatureAnisotropicDiffusion

contributor: Bill Lorensen (GE)

acknowledgements: This command module was derived from Insight/Examples (copyright) Insight Software Consortium

"""

    input_spec = CurvatureAnisotropicDiffusionInputSpec
    output_spec = CurvatureAnisotropicDiffusionOutputSpec
    _cmd = "CurvatureAnisotropicDiffusion "
    _outputs_filenames = {'outputVolume': 'outputVolume.nii'}


class GaussianBlurImageFilterInputSpec(CommandLineInputSpec):
    sigma = traits.Float(desc="Sigma value in physical units (e.g., mm) of the Gaussian kernel", argstr="--sigma %f")
    inputVolume = File(position=-2, desc="Input volume", exists=True, argstr="%s")
    outputVolume = traits.Either(traits.Bool, File(), position=-1, hash_files=False, desc="Blurred Volume", argstr="%s")


class GaussianBlurImageFilterOutputSpec(TraitedSpec):
    outputVolume = File(position=-1, desc="Blurred Volume", exists=True)


class GaussianBlurImageFilter(SEMLikeCommandLine):
    """title: Gaussian Blur Image Filter

category: Filtering.Denoising

description: Apply a gaussian blurr to an image

version: 0.1.0.$Revision: 1.1 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/GaussianBlurImageFilter

contributor: Julien Jomier (Kitware), Stephen Aylward (Kitware)

acknowledgements: This work is part of the National Alliance for Medical Image Computing (NAMIC), funded by the National Institutes of Health through the NIH Roadmap for Medical Research, Grant U54 EB005149.

"""

    input_spec = GaussianBlurImageFilterInputSpec
    output_spec = GaussianBlurImageFilterOutputSpec
    _cmd = "GaussianBlurImageFilter "
    _outputs_filenames = {'outputVolume': 'outputVolume.nii'}


class MedianImageFilterInputSpec(CommandLineInputSpec):
    neighborhood = InputMultiPath(traits.Int, desc="The size of the neighborhood in each dimension", sep=",", argstr="--neighborhood %s")
    inputVolume = File(position=-2, desc="Input volume to be filtered", exists=True, argstr="%s")
    outputVolume = traits.Either(traits.Bool, File(), position=-1, hash_files=False, desc="Output filtered", argstr="%s")


class MedianImageFilterOutputSpec(TraitedSpec):
    outputVolume = File(position=-1, desc="Output filtered", exists=True)


class MedianImageFilter(SEMLikeCommandLine):
    """title: Median Image Filter

category: Filtering.Denoising

description: The MedianImageFilter is commonly used as a robust approach for noise reduction. This filter is particularly efficient against "salt-and-pepper" noise. In other words, it is robust to the presence of gray-level outliers. MedianImageFilter computes the value of each output pixel as the statistical median of the neighborhood of values around the corresponding input pixel.

version: 0.1.0.$Revision: 19608 $(alpha)

documentation-url: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/MedianImageFilter

contributor: Bill Lorensen (GE)

acknowledgements: This command module was derived from Insight/Examples/Filtering/MedianImageFilter (copyright) Insight Software Consortium

"""

    input_spec = MedianImageFilterInputSpec
    output_spec = MedianImageFilterOutputSpec
    _cmd = "MedianImageFilter "
    _outputs_filenames = {'outputVolume': 'outputVolume.nii'}
