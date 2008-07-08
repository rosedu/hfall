#ifndef _3DS_CHUNKS_
#define _3DS_CHUNKS_

#include "Array.h"

typedef struct ChunkHeader
{
	int start_position;
	unsigned short chunk_id;
	unsigned int chunk_length;
};

/*###########################  Object Chunks  ###################################*/

class TextureChunk
{
	public:
		char *name;
		unsigned short percentage;
		unsigned short bumpPercentage;
		unsigned short tiling;
		float blur;
		float uScale;
		float vScale;
		float uOffset;
		float vOffset;
		float rotationAngle;
		unsigned char firstBlendColor[3];
		unsigned char secondBlendColor[3];
		unsigned char redBlendColor[3];
		unsigned char greenBlendColor[3];
		unsigned char blueBlendColor[3];
		TextureChunk() : name(NULL) {};
};

class MaterialChunk
{
	public:
		char *name;
		unsigned char ambientColor[3];
		unsigned char diffuseColor[3];
		unsigned char specularColor[3];
		unsigned short shininess;
		unsigned short shininessStrength;
		unsigned short secondShininessStrength;
		unsigned short transparency;
		unsigned short transparencyFallof;
		unsigned short reflectionBlur;
		bool isSelfIlluminated;
		bool twoSided;
		bool aditive;
		bool wireframe;
		float wireSize;
		unsigned short shadingType;
		TextureChunk textureMap1;
		TextureChunk textureMap2;
		TextureChunk specularMap;
		TextureChunk opacityMap;
		TextureChunk reflectionMap;
		TextureChunk bumpMap;
		TextureChunk shininessMap;
		TextureChunk textureMask1;
		TextureChunk textureMask2;
		TextureChunk opacityMask;
		TextureChunk bumpMask;
		TextureChunk specularMask;
		TextureChunk reflectionMask;
		TextureChunk shininessMask;
		MaterialChunk() : name(NULL) {};
};

class MaterialGroupChunk
{
	public:
		char *materialName;
		unsigned short nrOfFaces;
		unsigned short *faces;
		MaterialGroupChunk() : materialName(NULL), 
		faces(NULL), nrOfFaces(0) {};
};

class FacesChunk
{	
	public:
		unsigned short nrOfFaces;
		unsigned short *faces;
		unsigned short *flags;
		long *smoothingList;
		Array<MaterialGroupChunk> materialGroups;
		FacesChunk() : faces(NULL), flags(NULL),
		smoothingList(NULL), nrOfFaces(0) {};
};

class TextureInfoChunk
{
	public:
		unsigned short mapType;
		float tiling[2];
		float icon[3];
		float matrix[4][3]; 
        float scaling;
        float planIconW;
        float planIconH;
        float cylIconH;
};

class MeshData
{
	public:
		unsigned short nrOfVertices;
		unsigned short nrOfCoordrinates;
		float *vertices;
		float *coordinates;
		float matrix[4][3];
		char color;
		FacesChunk faces;
		TextureInfoChunk textureInfo;
		char *mapMaterials[6];
		MeshData() : vertices(NULL),
		coordinates(NULL) {};
};

class SpotLightChunk
{
	public:
		float target[3];
		float hotSpot;
		float fallOff;
		float rolloffAngle;
		float aspectRatio;
		bool seeCone;
		bool castsShadows;
		float localShadow[2];
		unsigned short mapSize;
};

class LightChunk
{
	public:
		bool lightOff;
		float position[3];
		float color[3];
		float attenuation;
		float innerRange;
		float outerRange;
		float multiplier;
		char *exclude;
		SpotLightChunk spotLight;
		LightChunk() : exclude(NULL) {};
};

class CameraChunk
{
	public:
		float position[3];
		float target[3];
		float bankAngle;
		float focus;
		bool seeOutline;
		float ranges[2];
};

class MeshChunk
{
	public:
		char *name;
		unsigned short type;
		MeshData data;
		LightChunk light;
		CameraChunk camera;
		MeshChunk() : name(NULL) {};
};

class ObjectChunk
{	
	public:
		int version;
		float masterScale;
		float ambientLight[3];
		Array<MaterialChunk> materials;
		Array<MeshChunk> meshes;
};

/*###########################  Animation Chunks  ###################################*/

class KeyframeHeader
{
	public:
		char *filename;
		unsigned short revision;
		int animationLength;
		KeyframeHeader() : filename(NULL) {};
};

class KeyframeNodeHeader
{
	public:
		char *name;
		unsigned short flags[2];
		unsigned short heirarchy;
		KeyframeNodeHeader() : name(NULL) {};
};

class TrackData
{
	public:
		int frameNumber;
		unsigned short splineFlags;
	    float splineData[5];
};

class KeyframeTrack
{
	public:
		unsigned short flags;
		int unknown[2]; 
		int nrOfKeys;
        TrackData *trackData;
        KeyframeTrack() : trackData(NULL) {};
};

typedef float float3[3]; 

class KeyframeTrackPosition : public KeyframeTrack
{
	public:
        float3 *position;
        KeyframeTrackPosition() : position(NULL) {};
};

class KeyframeTrackRotation : public KeyframeTrack
{
	public:
        float *rotation;
        float3 *axis;
        KeyframeTrackRotation() : rotation(NULL),
        axis(NULL) {};
};

class KeyframeTrackScale : public KeyframeTrack
{
	public:
        float3 *scale;
        KeyframeTrackScale() : scale(NULL) {};
};

class KeyframeTrackColor : public KeyframeTrack
{
	public:
        float3 *color;
        KeyframeTrackColor() : color(NULL) {};
};

class KeyframeTrackLightHotspot : public KeyframeTrack
{
	public:
        float *angle;
        KeyframeTrackLightHotspot() : angle(NULL) {};
};

class KeyframeTrackLightFalloff : public KeyframeTrack
{
	public:
        float *angle;
        KeyframeTrackLightFalloff() : angle(NULL) {};
};

class KeyframeCameraRollPosition : public KeyframeTrack
{
	public:
		float *roll;
		KeyframeCameraRollPosition() : roll(NULL) {};
};

class KeyframeCameraFieldOfView : public KeyframeTrack
{
	public:
		float *fieldOfView;
		KeyframeCameraFieldOfView() : fieldOfView(NULL) {};
};

class BoundingBox
{
	public:
		float min[3];
		float max[3];
};

class KeyframeChunkHeader
{
	public:
		unsigned short nodeID;
		KeyframeNodeHeader nodeHeader;
};         												

class ObjectKeyframeChunk : public KeyframeChunkHeader
{
	public:
		float pivotPosition[3];
		char *instanceName;
		KeyframeTrackPosition trackPosition;
		KeyframeTrackRotation trackRotation;
		KeyframeTrackScale trackScale;
		BoundingBox box;
		ObjectKeyframeChunk() : instanceName(NULL) {};
};

class SpotlightKeyframeChunk : public KeyframeChunkHeader
{
	public:
		KeyframeTrackPosition trackPosition;
		KeyframeTrackColor trackColor;
		KeyframeTrackLightHotspot trackLightHotspot;
		KeyframeTrackLightFalloff trackLightFalloff;
		KeyframeCameraRollPosition cameraRollPosition;
};

class LightTargetKeyframeChunk : public KeyframeChunkHeader
{
	public:
		KeyframeTrackPosition trackPosition;
};

class LightKeyframeChunk : public KeyframeChunkHeader
{
	public:
		KeyframeTrackPosition trackPosition;
		KeyframeTrackColor trackColor;
};

class CameraKeyframeChunk : public KeyframeChunkHeader
{
	public:
		KeyframeTrackPosition trackPosition;
		KeyframeCameraFieldOfView cameraFieldOfView;
		KeyframeCameraRollPosition cameraRollPosition;
};

class TargetKeyframeChunk : public KeyframeChunkHeader
{
	public:
		KeyframeTrackPosition trackPosition;
};

class KeyframeChunk
{	
	public:
		KeyframeHeader header;
		unsigned int startFrame;
		unsigned int endFrame;
		int currentTime;
		Array<ObjectKeyframeChunk> objectKeyframes;
		//Array<AmbientKeyframeChunk> ambientKeyframes;
		Array<CameraKeyframeChunk> cameraKeyframes;
		Array<TargetKeyframeChunk> targetKeyframes;
		Array<LightKeyframeChunk> lightKeyframes;
		Array<LightTargetKeyframeChunk> lightTargetKeyframes;
		Array<SpotlightKeyframeChunk> spotlightKeyframes;
};


#endif
