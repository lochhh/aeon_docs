(target-module-subject-tracking)=
# Subject Tracking
The subject tracking module processes [camera](target-node-spinnakervideosource) frame events to facilitate comprehensive tracking and analysis of animal positions and movements in the [habitat](target-habitat) or within specific regions or areas in the habitat that are of behavioural significance (e.g. [nest](target-module-nest), [foraging patch](target-module-foraging-patch)). 
It includes nodes such as `PositionTracking` for detecting and tracking blobs (of objects, e.g. animals);
`PoseTracking`, which leverages [SLEAP's](https://sleap.ai/) multi-animal tracking capabilities, to simultaneously track and identify different animals; and
`RegionTracking` for determining if a tracked object is within a specific region.
These enable real-time tracking, event triggering, and data logging, making it easier to monitor and analyse animal behaviour in various experimental setups.

## Nodes
### PositionTracking 
The `PositionTracking (Aeon.Vision)` node accepts frame events generated by a [camera](target-node-spinnakervideosource) and detects dark objects against a light background using a standard blob tracking pipeline. 

Briefly, the incoming image is thresholded to a binary image, then masked using a binary mask image generated by the user. 
This mask should include any area in which the animal could be at a given time, and must have the same width and height as the camera event images<!-- does "camera event images" refer to the "VideoDataFrame"s? --> for which it is intended. 
This ensures any movement or activity outside of the region of interest (therefore have pixel values of zero in the user-generated mask) are eliminated and not tracked.
Below is an example of an input image of the habitat from a top-view camera and its corresponding mask.

::::things-in-a-row
:::{figure} ../../../images/module-cv-tracking-cameratop.png
:height: 200px
:alt: camera top

Habitat image from "CameraTop".
:::
:::{figure} ../../../images/module-cv-tracking-arena-mask.png
:height: 200px
:alt: habitat mask

Habitat mask.
:::
::::

Contours are found and located using the `FindContours` and `BinaryRegionAnalysis` functions from `OpenCV.NET` (available in `Bonsai.Vision` package) and a custom `TakeLargestRegions (Aeon.Vision)` to take the *n* largest regions as defined by the property [`TrackingCount`](#properties). 

#### Inputs
Sequence of `Harp.Timestamped<Aeon.Video.VideoDataFrame>`s from a specific camera published by a [`SpinnakerVideoSource (Aeon.Video)`](target-node-spinnakervideosource) node.

#### Outputs
Sequence of `Harp.Timestamped<Bonsai.Vision.ConnectedComponentCollection>` describing the features of a detected subject. Also published to a `Subject`.

#### Properties
##### Tracking parameters
| Property name | Description                                               |
|---------------|-----------------------------------------------------------|
| **Mask**           | The full or relative path to the mask image, in `.png` format    |
| **Threshold** | The threshold pixel value to apply in order to detect a dark blob on the light background |
| **TrackingCount** | The expected number of animals to track simultaneously |

##### Subjects
Events from this node are published to shared `Subject`s. 
Here you set the names used for these `Subject`s to identify events for this node.
Each of these `Subject`s becomes accessible in the Bonsai editor's toolbox anywhere in the workflow using the name set here.

###### Device event subjects
| Subject name      | Type        | Description                   |
|-------------------|-------------|-------------------------------|
| **TrackingEvents** | `Harp.Timestamped<Bonsai.Vision.ConnectedComponentCollection>` | The `Subject` to which tracking data will be published. This stream is also output directly by the node | 

###### Device input subjects
| Subject name      | Type          | Description                                                                                     |
|-------------------|---------------|-------------------------------------------------------------------------------------------------|
| **FrameEvents**   | `Harp.Timestamped<Aeon.Acquisition.VideoDataFrame>` | The `Subject` to subscribe to that carries frame events from a chosen camera | 

#### Usage
Create a `GroupWorkflow` and give it an appropriate name, e.g. "TrackingTop". 
Inside, place a `PositionTracking (Aeon.Vision)` node, externalise all properties, and connect it to the `WorkflowOutput`.
<!-- Is there a use case for the basic workflow without a camera supplying the videodataframes? If none, perhaps we can remove this example and just provide the full example with camera connected. -->
:::workflow
![Aeon.Vision.PositionTracking](../../../workflows/positionTrackingBase.bonsai)
:::

Next, add a `SubscribeSubject` node, connect it to the `PositionTracking` node as an input, and externalise the `Name` property. 
This name will be set to the `Subject` that carries the `FrameEvents` from the [camera](target-node-spinnakervideosource) on which tracking is to be performed (e.g. "CameraTop"). 

:::workflow
![Aeon.Vision.PositionTracking](../../../workflows/positionTracking.bonsai)
:::

### PoseTracking
Pose tracking utilises [SLEAP](https://sleap.ai/), which is fully integrated with Bonsai through the [Bonsai.Sleap](https://bonsai-rx.org/sleap/index.html) package, to simultaneously track and identify different animals within the habitat.

In Aeon experimental workflows, two linked `IncludeWorkflow`s are provided to give this functionality. 
The `PoseTracking (Extensions)` node contains the complete data flow and processing workflow for identity and tracking of subjects from video frames captured by the cameras, whereas the `PoseTracking (Aeon.Vision.Sleap)` node is used within this workflow to perform the model inference step of processing. 
<!-- To be completed
#### Inputs
#### Outputs
A sequence of `<type>` with the following attributes. 
| Attribute name     | Type                           | Description                      |
|--------------------|--------------------------------|----------------------------------|
| **Attr1**          | `Type`                         | Description of Attr1             |
| **Attr2**          | `Type`                         | Description of Attr2             |
-->
#### Properties
##### General
| Property name | Description                                               |
|---------------|-----------------------------------------------------------|
| **IdentityMinConfidence** |  Set the minimum confidence score applied to computation of an object (animal) instance's centroid |
| **FrameStep**           | Frame by frame inference and pose estimation is computationally expensive. It may be helpful to downsample the incoming stream to run inference in real time. Here you can set the number of frames to skip between incoming frames  |
| **IdentityMinConfidence** | Set the minimum confidence required to label an instance's identity |
| **ModelPath** | Set the partial path to the saved `frozen_graph.pb` |
| **PartMinConfidence** | Set the minimum confidence required to assign a label to an instance's keypoint |

##### Subjects
Both generated and input events of this node are collected and passed to published `Subject`s. 
Here you set the names used for these `Subject`s to identify events for this node.
Each of these `Subject`s becomes accessible in the Bonsai editor's toolbox anywhere in the workflow using the name set here.

###### Device event subjects
| Subject name      | Type        | Description                   |
|-------------------|-------------|-------------------------------|
| **TrackingEvents** | `Harp.Timestamped<Bonsai.Vision.ConnectedComponentCollection>` | The `Subject` to which tracking data will be published. This stream is also output directly by the node | 

###### Device input subjects
| Subject name      | Type          | Description                                                                                     |
|-------------------|---------------|-------------------------------------------------------------------------------------------------|
| **FrameEvents**   | `Harp.Timestamped<Aeon.Acquisition.VideoDataFrame>` | The `Subject` to subscribe to that carries frame events from a chosen camera | 

#### Usage
The trained model must first be exported to [Protocol buffer (.pb) format](https://protobuf.dev/) using the [`sleap-export`](https://sleap.ai/guides/cli.html#sleap-export) command line interface. 
Next, create a `GroupWorkflow` and give it an appropriate name, e.g. "PoseTracking". 
Inside, place a `PoseTracking (Aeon.Vision.Sleap)` node, externalise all properties, and connect it to the `WorkflowOutput`.

:::workflow
![poseTracking](../../../workflows/poseTracking.bonsai)
:::

### RegionTracking 
<!-- I assume this node can be used with either PositionTracking or PoseTracking. If incorrect, we should remove the PoseTracking bit. -->
The `RegionTracking (Aeon.Vision)` node computes and returns a `boolean` describing whether the tracked position (from a [`PositionTracking (Aeon.Vision)`](#positiontracking) or [`PoseTracking (Aeon.Vision.Sleap)`](#posetracking) node) of an animal falls within a defined [region](target-node-regiontracking-properties) of the camera image.
<!-- To be completed
#### Inputs
Tracking events in the format `Harp.Timestamped<Bonsai.Vision.ConnectedComponentCollection>` generated by a [`PositionTracking (Aeon.Vision)`](#positiontracking) node?

#### Outputs
boolean? 
-->
(target-node-regiontracking-properties)=
#### Properties
##### General
| Property name | Description                                               |
|---------------|-----------------------------------------------------------|
| **Region**         | An array of four `OpenCV.NET.Points`. These define the corners (anticlockwise from top left) of the region of interest     |

##### Subjects
Both generated and input events of this node are published to shared `Subject`s. 
Here you set the names used for these `Subject`s to identify events for this node.
Each of these `Subject`s becomes accessible in the Bonsai editor's toolbox anywhere in the workflow using the name set here.

###### Device event subjects
| Subject name      | Type        | Description                   |
|-------------------|-------------|-------------------------------|
| **RegionEvents** | `Harp.Timestamped<bool>` | The `Subject` to which region events will be published. This stream is also output directly by the node | 

###### Device input subjects
| Subject name      | Type          | Description                                                                                     |
|-------------------|---------------|-------------------------------------------------------------------------------------------------|
| **FrameEvents**   | `Harp.Timestamped<Aeon.Acquisition.VideoDataFrame>` | The `Subject` to subscribe to that carries frame events from a chosen camera | 

#### Usage
Place a `RegionTracking (Aeon.Vision)` node, externalise the `Region` property, and rename it to indicate the region this node is responsible for monitoring (e.g. "NestRegion").
Next, add a `SubscribeSubject` node to subscribe to the common "TrackingEvents" `Subject` (e.g. "TrackingTop") and connect it to the `RegionTracking (Aeon.Vision)` node.

:::workflow
![RegionTracking](../../../workflows/regionTracking.bonsai)
:::

### DistanceFromPoint 
<!-- I assume this node can be used with either PositionTracking or PoseTracking. If incorrect, we should remove the PoseTracking bit. -->
The `DistanceFromPoint (Aeon.Vision)` node computes the distance (in pixels) between the tracked position (from a [`PositionTracking (Aeon.Vision)`](#positiontracking) or [`PoseTracking (Aeon.Vision.Sleap)`](#posetracking) node) of an animal and a defined [point](target-node-distancefrompoint-properties) in the camera image. 
<!-- To be completed
#### Inputs
Tracking events in the format `Harp.Timestamped<Bonsai.Vision.ConnectedComponentCollection>` generated by a [`PositionTracking (Aeon.Vision)`](#positiontracking) node?

#### Outputs
A `Harp.Timestamped<double>` distance in pixels?

:::{note}
This node does not output to a published `Subject`.
:::
-->
(target-node-distancefrompoint-properties)=
#### Properties
##### General
<!-- Shouldn't the property be a point "Value"? Check whether the property is indeed "Region". -->
| Property name | Description                                               |
|---------------|-----------------------------------------------------------|
| **Region**         | An array of four `OpenCV.NET.Points`. These define the corners (anticlockwise from top left) of the region of interest     |

#### Usage
Place a `DistanceFromPoint (Aeon.Vision)` node, externalise the `Value` property, and rename it to indicate the point of interest for this node (e.g. "ArenaCenter").
Next, add a `SubscribeSubject` node to subscribe to the common "TrackingEvents" `Subject` (e.g. "TrackingTop") and connect it to the `DistanceFromPoint (Aeon.Vision)` node.

:::workflow
![DistanceFromPoint](../../../workflows/distFromPoint.bonsai)
:::

The output of the `DistanceFromPoint (Aeon.Vision)` node can then be used with other nodes 
like the [`InRange (Aeon.Acquisition)`](#inrange) node to trigger events or commands based on the proximity of an animal to a specific point in the camera image.

(target-node-inrange)=
### InRange
<!-- I assume this node can be used with either PositionTracking or PoseTracking. If incorrect, we should remove the PoseTracking bit. -->
The `InRange (Aeon.Acquisition)` node is used to determine whether the tracked position (from a [`PositionTracking (Aeon.Vision)`](#positiontracking) or [`PoseTracking (Aeon.Vision.Sleap)`](#posetracking) node) of an animal is within a specified [range](target-node-inrange-properties) in a single dimension.
<!-- To be completed
#### Inputs
#### Outputs
A `boolean` describing whether each value of a sequence falls within a specific range
--> 
(target-node-inrange-properties)=
#### Properties
##### General
| Property name | Description                                               |
|---------------|-----------------------------------------------------------|
| **Lower**          | The lower end of the range to check the input value against |
| **Upper**          | The upper end of the range to check the input value against |

##### Subjects
Events from this node are published to shared `Subject`s. 
Here you set the names used for these `Subject`s to identify events for this node.
Each of these `Subject`s becomes accessible in the Bonsai editor's toolbox anywhere in the workflow using the name set here.

###### Device event subjects
`HarpMessage` events emitted to a `Subject`

| Subject name      | Type        | Description                   |
|-------------------|-------------|-------------------------------|
| **RangeEvents**   | `Harp.Timestamped<bool>` | The `Subject` to which the result will be published |

#### Usage
The example here is based on a circular habitat with a corridor around the outside.
To determine if a given source is within the inner radius of the habitat, first create a `GroupWorkflow` and give it an appropriate name, e.g. "InArena".  
Inside, place an `InRange (Aeon.Acquisition)` node, externalise all relevant properties (i.e. the upper bound that is the inner radius of the habitat), and connect it to the `WorkflowInput` (e.g. "Source1") and `WorkflowOutput`.

:::workflow
![InArena](../../../workflows/inRange.bonsai)
:::

The input can, for instance, be a [`DistanceFromPoint (Aeon.Vision)`](#distancefrompoint) node, which computes the distance of a tracked animal from the centre of the habitat, allowing one to determine if the animal is in the open habitat.
Multiple of these `GroupWorkflows` each containing a separate `InRange (Aeon.Acquisition)` node can be used together to determine if a tracked animal position falls within different regions of interest.
For instance, to further determine if the animal is in the corridor, add another `GroupWorkflow`, e.g. "InCorridor", with an `InRange (Aeon.Acquisition)` node with the lower bound set to the inner radius of the habitat and the upper bound set to the outer radius of the habitat.

:::workflow
![ArenaOrCorridor](../../../workflows/corridorOrArena.bonsai)
:::
<!-- To be completed
## GUI
Description of any user interface components and visualisers.
-->

## Logging
<!-- The original "Logging" for the PoseTracking node was copied over from PositionTracking. So here I'm assuming the examples for PositionTracking are applicable to PoseTracking. Check if correct. -->
"TrackingEvents" from a `PositionTracking (Aeon.Vision)` or a `PoseTracking (Aeon.Vision.Sleap)` node can be logged along with the camera from which the "FrameEvents" originated using a [`LogHarpState (Aeon.Acquisition)`](target-node-logharpstate) node. 
First, add a `SubscribeSubject` to subscribe to the "TrackingEvents" `Subject` (e.g. "TrackingTop").
The events can then be formatted as `HarpMessages` and configured to write to register **200** (an unassigned register on all Harp devices) using the custom `FormatBinaryRegions (Aeon.Vision)` node.
Here is an example for logging a `PositionTracking` node.

:::workflow
![logPositionTracking](../../../workflows/logPositionTracking.bonsai)
:::

Multiple `PositionTracking` or `PoseTracking` nodes can be used to track objects in different camera streams simultaneously. 
To do this, select a different "FrameEvents" `Subject` for each node and save the results to the corresponding camera folders.
<!-- To be coompleted 
## State persistence
Information on state recovery or persistence requirements, if applicable.

## Alerts
Explanation of any alert configurations and links to guides or further configuration steps.
-->
:::{seealso}
The [SLEAP](https://sleap.ai/) and [Bonsai.Sleap](https://bonsai-rx.org/sleap/index.html) documentation for more information on training models to be used with the `PoseTracking (Aeon.Vision.Sleap)` node.
:::