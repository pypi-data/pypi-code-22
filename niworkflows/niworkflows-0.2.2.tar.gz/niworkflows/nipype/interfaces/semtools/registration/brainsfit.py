# -*- coding: utf-8 -*-
# -*- coding: utf8 -*-
"""Autogenerated file - DO NOT EDIT
If you spot a bug, please report it on the mailing list and/or change the generator."""

import os

from ...base import (CommandLine, CommandLineInputSpec, SEMLikeCommandLine,
                     TraitedSpec, File, Directory, traits, isdefined,
                     InputMultiPath, OutputMultiPath)


class BRAINSFitInputSpec(CommandLineInputSpec):
    fixedVolume = File(desc="Input fixed image (the moving image will be transformed into this image space).", exists=True, argstr="--fixedVolume %s")
    movingVolume = File(desc="Input moving image (this image will be transformed into the fixed image space).", exists=True, argstr="--movingVolume %s")
    samplingPercentage = traits.Float(
        desc="Fraction of voxels of the fixed image that will be used for registration. The number has to be larger than zero and less or equal to one. Higher values increase the computation time but may give more accurate results. You can also limit the sampling focus with ROI masks and ROIAUTO mask generation. The default is 0.002 (use approximately 0.2% of voxels, resulting in 100000 samples in a 512x512x192 volume) to provide a very fast registration in most cases. Typical values range from 0.01 (1%) for low detail images to 0.2 (20%) for high detail images.", argstr="--samplingPercentage %f")
    splineGridSize = InputMultiPath(traits.Int, desc="Number of BSpline grid subdivisions along each axis of the fixed image, centered on the image space. Values must be 3 or higher for the BSpline to be correctly computed.", sep=",", argstr="--splineGridSize %s")
    linearTransform = traits.Either(traits.Bool, File(), hash_files=False, desc="(optional) Output estimated transform - in case the computed transform is not BSpline. NOTE: You must set at least one output object (transform and/or output volume).", argstr="--linearTransform %s")
    bsplineTransform = traits.Either(traits.Bool, File(), hash_files=False, desc="(optional) Output estimated transform - in case the computed transform is BSpline. NOTE: You must set at least one output object (transform and/or output volume).", argstr="--bsplineTransform %s")
    outputVolume = traits.Either(traits.Bool, File(), hash_files=False, desc="(optional) Output image: the moving image warped to the fixed image space. NOTE: You must set at least one output object (transform and/or output volume).", argstr="--outputVolume %s")
    initialTransform = File(desc="Transform to be applied to the moving image to initialize the registration.  This can only be used if Initialize Transform Mode is Off.", exists=True, argstr="--initialTransform %s")
    initializeTransformMode = traits.Enum("Off", "useMomentsAlign", "useCenterOfHeadAlign", "useGeometryAlign", "useCenterOfROIAlign",
                                          desc="Determine how to initialize the transform center.  useMomentsAlign assumes that the center of mass of the images represent similar structures.  useCenterOfHeadAlign attempts to use the top of head and shape of neck to drive a center of mass estimate. useGeometryAlign on assumes that the center of the voxel lattice of the images represent similar structures.  Off assumes that the physical space of the images are close.  This flag is mutually exclusive with the Initialization transform.", argstr="--initializeTransformMode %s")
    useRigid = traits.Bool(desc="Perform a rigid registration as part of the sequential registration steps.  This family of options overrides the use of transformType if any of them are set.", argstr="--useRigid ")
    useScaleVersor3D = traits.Bool(desc="Perform a ScaleVersor3D registration as part of the sequential registration steps.  This family of options overrides the use of transformType if any of them are set.", argstr="--useScaleVersor3D ")
    useScaleSkewVersor3D = traits.Bool(desc="Perform a ScaleSkewVersor3D registration as part of the sequential registration steps.  This family of options overrides the use of transformType if any of them are set.", argstr="--useScaleSkewVersor3D ")
    useAffine = traits.Bool(desc="Perform an Affine registration as part of the sequential registration steps.  This family of options overrides the use of transformType if any of them are set.", argstr="--useAffine ")
    useBSpline = traits.Bool(desc="Perform a BSpline registration as part of the sequential registration steps.  This family of options overrides the use of transformType if any of them are set.", argstr="--useBSpline ")
    useSyN = traits.Bool(desc="Perform a SyN registration as part of the sequential registration steps.  This family of options overrides the use of transformType if any of them are set.", argstr="--useSyN ")
    useComposite = traits.Bool(desc="Perform a Composite registration as part of the sequential registration steps.  This family of options overrides the use of transformType if any of them are set.", argstr="--useComposite ")
    maskProcessingMode = traits.Enum(
        "NOMASK", "ROIAUTO", "ROI", desc="Specifies a mask to only consider a certain image region for the registration.  If ROIAUTO is chosen, then the mask is computed using Otsu thresholding and hole filling. If ROI is chosen then the mask has to be specified as in input.", argstr="--maskProcessingMode %s")
    fixedBinaryVolume = File(desc="Fixed Image binary mask volume, required if Masking Option is ROI. Image areas where the mask volume has zero value are ignored during the registration.", exists=True, argstr="--fixedBinaryVolume %s")
    movingBinaryVolume = File(desc="Moving Image binary mask volume, required if Masking Option is ROI. Image areas where the mask volume has zero value are ignored during the registration.", exists=True, argstr="--movingBinaryVolume %s")
    outputFixedVolumeROI = traits.Either(
        traits.Bool, File(), hash_files=False, desc="ROI that is automatically computed from the fixed image. Only available if Masking Option is ROIAUTO. Image areas where the mask volume has zero value are ignored during the registration.", argstr="--outputFixedVolumeROI %s")
    outputMovingVolumeROI = traits.Either(
        traits.Bool, File(), hash_files=False, desc="ROI that is automatically computed from the moving image. Only available if Masking Option is ROIAUTO. Image areas where the mask volume has zero value are ignored during the registration.", argstr="--outputMovingVolumeROI %s")
    useROIBSpline = traits.Bool(desc="If enabled then the bounding box of the input ROIs defines the BSpline grid support region. Otherwise the BSpline grid support region is the whole fixed image.", argstr="--useROIBSpline ")
    histogramMatch = traits.Bool(
        desc="Apply histogram matching operation for the input images to make them more similar.  This is suitable for images of the same modality that may have different brightness or contrast, but the same overall intensity profile. Do NOT use if registering images from different modalities.", argstr="--histogramMatch ")
    medianFilterSize = InputMultiPath(traits.Int, desc="Apply median filtering to reduce noise in the input volumes. The 3 values specify the radius for the optional MedianImageFilter preprocessing in all 3 directions (in voxels).", sep=",", argstr="--medianFilterSize %s")
    removeIntensityOutliers = traits.Float(
        desc="Remove very high and very low intensity voxels from the input volumes. The parameter specifies the half percentage to decide outliers of image intensities. The default value is zero, which means no outlier removal. If the value of 0.005 is given, the 0.005% of both tails will be thrown away, so 0.01% of intensities in total would be ignored in the statistic calculation.", argstr="--removeIntensityOutliers %f")
    fixedVolume2 = File(desc="Input fixed image that will be used for multimodal registration. (the moving image will be transformed into this image space).", exists=True, argstr="--fixedVolume2 %s")
    movingVolume2 = File(desc="Input moving image that will be used for multimodal registration(this image will be transformed into the fixed image space).", exists=True, argstr="--movingVolume2 %s")
    outputVolumePixelType = traits.Enum("float", "short", "ushort", "int", "uint", "uchar", desc="Data type for representing a voxel of the Output Volume.", argstr="--outputVolumePixelType %s")
    backgroundFillValue = traits.Float(desc="This value will be used for filling those areas of the output image that have no corresponding voxels in the input moving image.", argstr="--backgroundFillValue %f")
    scaleOutputValues = traits.Bool(
        desc="If true, and the voxel values do not fit within the minimum and maximum values of the desired outputVolumePixelType, then linearly scale the min/max output image voxel values to fit within the min/max range of the outputVolumePixelType.", argstr="--scaleOutputValues ")
    interpolationMode = traits.Enum("NearestNeighbor", "Linear", "ResampleInPlace", "BSpline", "WindowedSinc", "Hamming", "Cosine", "Welch", "Lanczos", "Blackman",
                                    desc="Type of interpolation to be used when applying transform to moving volume.  Options are Linear, NearestNeighbor, BSpline, WindowedSinc, Hamming, Cosine, Welch, Lanczos, or ResampleInPlace.  The ResampleInPlace option will create an image with the same discrete voxel values and will adjust the origin and direction of the physical space interpretation.", argstr="--interpolationMode %s")
    numberOfIterations = InputMultiPath(
        traits.Int, desc="The maximum number of iterations to try before stopping the optimization. When using a lower value (500-1000) then the registration is forced to terminate earlier but there is a higher risk of stopping before an optimal solution is reached.", sep=",", argstr="--numberOfIterations %s")
    maximumStepLength = traits.Float(desc="Starting step length of the optimizer. In general, higher values allow for recovering larger initial misalignments but there is an increased chance that the registration will not converge.", argstr="--maximumStepLength %f")
    minimumStepLength = InputMultiPath(
        traits.Float, desc="Each step in the optimization takes steps at least this big.  When none are possible, registration is complete. Smaller values allows the optimizer to make smaller adjustments, but the registration time may increase.", sep=",", argstr="--minimumStepLength %s")
    relaxationFactor = traits.Float(
        desc="Specifies how quickly the optimization step length is decreased during registration. The value must be larger than 0 and smaller than 1. Larger values result in slower step size decrease, which allow for recovering larger initial misalignments but it increases the registration time and the chance that the registration will not converge.", argstr="--relaxationFactor %f")
    translationScale = traits.Float(desc="How much to scale up changes in position (in mm) compared to unit rotational changes (in radians) -- decrease this to allow for more rotation in the search pattern.", argstr="--translationScale %f")
    reproportionScale = traits.Float(desc="ScaleVersor3D 'Scale' compensation factor.  Increase this to allow for more rescaling in a ScaleVersor3D or ScaleSkewVersor3D search pattern.  1.0 works well with a translationScale of 1000.0", argstr="--reproportionScale %f")
    skewScale = traits.Float(desc="ScaleSkewVersor3D Skew compensation factor.  Increase this to allow for more skew in a ScaleSkewVersor3D search pattern.  1.0 works well with a translationScale of 1000.0", argstr="--skewScale %f")
    maxBSplineDisplacement = traits.Float(
        desc="Maximum allowed displacements in image physical coordinates (mm) for BSpline control grid along each axis.  A value of 0.0 indicates that the problem should be unbounded.  NOTE:  This only constrains the BSpline portion, and does not limit the displacement from the associated bulk transform.  This can lead to a substantial reduction in computation time in the BSpline optimizer.,       ", argstr="--maxBSplineDisplacement %f")
    fixedVolumeTimeIndex = traits.Int(desc="The index in the time series for the 3D fixed image to fit. Only allowed if the fixed input volume is 4-dimensional.", argstr="--fixedVolumeTimeIndex %d")
    movingVolumeTimeIndex = traits.Int(desc="The index in the time series for the 3D moving image to fit. Only allowed if the moving input volume is 4-dimensional", argstr="--movingVolumeTimeIndex %d")
    numberOfHistogramBins = traits.Int(desc="The number of histogram levels used for mutual information metric estimation.", argstr="--numberOfHistogramBins %d")
    numberOfMatchPoints = traits.Int(desc="Number of histogram match points used for mutual information metric estimation.", argstr="--numberOfMatchPoints %d")
    costMetric = traits.Enum("MMI", "MSE", "NC", "MIH", desc="The cost metric to be used during fitting. Defaults to MMI. Options are MMI (Mattes Mutual Information), MSE (Mean Square Error), NC (Normalized Correlation), MC (Match Cardinality for binary images)", argstr="--costMetric %s")
    maskInferiorCutOffFromCenter = traits.Float(
        desc="If Initialize Transform Mode is set to useCenterOfHeadAlign or Masking Option is ROIAUTO then this value defines the how much is cut of from the inferior part of the image. The cut-off distance is specified in millimeters, relative to the image center. If the value is 1000 or larger then no cut-off performed.", argstr="--maskInferiorCutOffFromCenter %f")
    ROIAutoDilateSize = traits.Float(
        desc="This flag is only relevant when using ROIAUTO mode for initializing masks.  It defines the final dilation size to capture a bit of background outside the tissue region.  A setting of 10mm has been shown to help regularize a BSpline registration type so that there is some background constraints to match the edges of the head better.", argstr="--ROIAutoDilateSize %f")
    ROIAutoClosingSize = traits.Float(
        desc="This flag is only relevant when using ROIAUTO mode for initializing masks.  It defines the hole closing size in mm.  It is rounded up to the nearest whole pixel size in each direction. The default is to use a closing size of 9mm.  For mouse data this value may need to be reset to 0.9 or smaller.", argstr="--ROIAutoClosingSize %f")
    numberOfSamples = traits.Int(
        desc="The number of voxels sampled for mutual information computation.  Increase this for higher accuracy, at the cost of longer computation time., NOTE that it is suggested to use samplingPercentage instead of this option. However, if set to non-zero, numberOfSamples overwrites the samplingPercentage option.  ", argstr="--numberOfSamples %d")
    strippedOutputTransform = traits.Either(
        traits.Bool, File(), hash_files=False, desc="Rigid component of the estimated affine transform. Can be used to rigidly register the moving image to the fixed image. NOTE:  This value is overridden if either bsplineTransform or linearTransform is set.", argstr="--strippedOutputTransform %s")
    transformType = InputMultiPath(
        traits.Str, desc="Specifies a list of registration types to be used.  The valid types are, Rigid, ScaleVersor3D, ScaleSkewVersor3D, Affine, BSpline and SyN.  Specifying more than one in a comma separated list will initialize the next stage with the previous results. If registrationClass flag is used, it overrides this parameter setting.", sep=",", argstr="--transformType %s")
    outputTransform = traits.Either(traits.Bool, File(), hash_files=False, desc="(optional) Filename to which save the (optional) estimated transform. NOTE: You must select either the outputTransform or the outputVolume option.", argstr="--outputTransform %s")
    initializeRegistrationByCurrentGenericTransform = traits.Bool(
        desc="If this flag is ON, the current generic composite transform, resulted from the linear registration stages, is set to initialize the follow nonlinear registration process. However, by the default behaviour, the moving image is first warped based on the existant transform before it is passed to the BSpline registration filter. It is done to speed up the BSpline registration by reducing the computations of composite transform Jacobian.", argstr="--initializeRegistrationByCurrentGenericTransform ")
    failureExitCode = traits.Int(desc="If the fit fails, exit with this status code.  (It can be used to force a successfult exit status of (0) if the registration fails due to reaching the maximum number of iterations.", argstr="--failureExitCode %d")
    writeTransformOnFailure = traits.Bool(desc="Flag to save the final transform even if the numberOfIterations are reached without convergence. (Intended for use when --failureExitCode 0 )", argstr="--writeTransformOnFailure ")
    numberOfThreads = traits.Int(desc="Explicitly specify the maximum number of threads to use. (default is auto-detected)", argstr="--numberOfThreads %d")
    debugLevel = traits.Int(desc="Display debug messages, and produce debug intermediate results.  0=OFF, 1=Minimal, 10=Maximum debugging.", argstr="--debugLevel %d")
    costFunctionConvergenceFactor = traits.Float(
        desc="From itkLBFGSBOptimizer.h: Set/Get the CostFunctionConvergenceFactor. Algorithm terminates when the reduction in cost function is less than (factor * epsmcj) where epsmch is the machine precision. Typical values for factor: 1e+12 for low accuracy; 1e+7 for moderate accuracy and 1e+1 for extremely high accuracy.  1e+9 seems to work well.,       ", argstr="--costFunctionConvergenceFactor %f")
    projectedGradientTolerance = traits.Float(desc="From itkLBFGSBOptimizer.h: Set/Get the ProjectedGradientTolerance. Algorithm terminates when the project gradient is below the tolerance. Default lbfgsb value is 1e-5, but 1e-4 seems to work well.,       ", argstr="--projectedGradientTolerance %f")
    maximumNumberOfEvaluations = traits.Int(desc="Maximum number of evaluations for line search in lbfgsb optimizer.", argstr="--maximumNumberOfEvaluations %d")
    maximumNumberOfCorrections = traits.Int(desc="Maximum number of corrections in lbfgsb optimizer.", argstr="--maximumNumberOfCorrections %d")
    gui = traits.Bool(desc="Display intermediate image volumes for debugging.  NOTE:  This is not part of the standard build sytem, and probably does nothing on your installation.", argstr="--gui ")
    promptUser = traits.Bool(desc="Prompt the user to hit enter each time an image is sent to the DebugImageViewer", argstr="--promptUser ")
    metricSamplingStrategy = traits.Enum("Random", desc="It defines the method that registration filter uses to sample the input fixed image. Only Random is supported for now.", argstr="--metricSamplingStrategy %s")
    logFileReport = traits.Either(traits.Bool, File(), hash_files=False, desc="A file to write out final information report in CSV file: MetricName,MetricValue,FixedImageName,FixedMaskName,MovingImageName,MovingMaskName", argstr="--logFileReport %s")
    writeOutputTransformInFloat = traits.Bool(desc="By default, the output registration transforms (either the output composite transform or each transform component) are written to the disk in double precision. If this flag is ON, the output transforms will be written in single (float) precision. It is especially important if the output transform is a displacement field transform, or it is a composite transform that includes several displacement fields.", argstr="--writeOutputTransformInFloat ")


class BRAINSFitOutputSpec(TraitedSpec):
    linearTransform = File(desc="(optional) Output estimated transform - in case the computed transform is not BSpline. NOTE: You must set at least one output object (transform and/or output volume).", exists=True)
    bsplineTransform = File(desc="(optional) Output estimated transform - in case the computed transform is BSpline. NOTE: You must set at least one output object (transform and/or output volume).", exists=True)
    outputVolume = File(desc="(optional) Output image: the moving image warped to the fixed image space. NOTE: You must set at least one output object (transform and/or output volume).", exists=True)
    outputFixedVolumeROI = File(desc="ROI that is automatically computed from the fixed image. Only available if Masking Option is ROIAUTO. Image areas where the mask volume has zero value are ignored during the registration.", exists=True)
    outputMovingVolumeROI = File(desc="ROI that is automatically computed from the moving image. Only available if Masking Option is ROIAUTO. Image areas where the mask volume has zero value are ignored during the registration.", exists=True)
    strippedOutputTransform = File(desc="Rigid component of the estimated affine transform. Can be used to rigidly register the moving image to the fixed image. NOTE:  This value is overridden if either bsplineTransform or linearTransform is set.", exists=True)
    outputTransform = File(desc="(optional) Filename to which save the (optional) estimated transform. NOTE: You must select either the outputTransform or the outputVolume option.", exists=True)
    logFileReport = File(desc="A file to write out final information report in CSV file: MetricName,MetricValue,FixedImageName,FixedMaskName,MovingImageName,MovingMaskName", exists=True)


class BRAINSFit(SEMLikeCommandLine):

    """title: General Registration (BRAINS)

category: Registration

description: Register a three-dimensional volume to a reference volume (Mattes Mutual Information by default). Full documentation avalable here: http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/BRAINSFit. Method described in BRAINSFit: Mutual Information Registrations of Whole-Brain 3D Images, Using the Insight Toolkit, Johnson H.J., Harris G., Williams K., The Insight Journal, 2007. http://hdl.handle.net/1926/1291

version: 3.0.0

documentation-url: http://www.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/BRAINSFit

license: https://www.nitrc.org/svn/brains/BuildScripts/trunk/License.txt

contributor: Hans J. Johnson, hans-johnson -at- uiowa.edu, http://www.psychiatry.uiowa.edu

acknowledgements: Hans Johnson(1,3,4); Kent Williams(1); Gregory Harris(1), Vincent Magnotta(1,2,3);  Andriy Fedorov(5) 1=University of Iowa Department of Psychiatry, 2=University of Iowa Department of Radiology, 3=University of Iowa Department of Biomedical Engineering, 4=University of Iowa Department of Electrical and Computer Engineering, 5=Surgical Planning Lab, Harvard

"""

    input_spec = BRAINSFitInputSpec
    output_spec = BRAINSFitOutputSpec
    _cmd = " BRAINSFit "
    _outputs_filenames = {'outputVolume': 'outputVolume.nii', 'bsplineTransform': 'bsplineTransform.h5', 'outputTransform': 'outputTransform.h5', 'outputFixedVolumeROI': 'outputFixedVolumeROI.nii',
                          'strippedOutputTransform': 'strippedOutputTransform.h5', 'outputMovingVolumeROI': 'outputMovingVolumeROI.nii', 'linearTransform': 'linearTransform.h5', 'logFileReport': 'logFileReport'}
    _redirect_x = False
