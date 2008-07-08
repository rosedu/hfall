#ifndef _3DS_PARSER_
#define _3DS_PARSER_

#include "Chunks.h"

class MaxParser
{
	public:
		MaxParser();
		MaxParser(const char *filename);
		~MaxParser();
		bool parse();
		bool parse(bool object, bool animation);
		void setFile(const char *filename);
		inline int getVersion() { return version; }
		inline ObjectChunk *getObjectChunk() { return object; }
		inline KeyframeChunk *getKeyframeChunk() { return keyframe; }
		
	private:
		void readChunkHeader(ChunkHeader &h);
		void readMainChunk(int bytes);
		void readMaterialChunk(int bytes);
		void readTextureChunk(TextureChunk &texture, int bytes);
		void readObjectChunk(int bytes);
		void readMeshChunk(int bytes);
		void readMeshData(MeshData &data, int bytes);
		void readFacesChunk(FacesChunk &faces, int bytes);
		void readLightChunk(LightChunk &light, int bytes);
		void readSpotLigthChunk(SpotLightChunk &spotLight, int bytes);
		void readCameraChunk(CameraChunk &camera, int bytes);
		void readKeyframeChunk(int bytes);
		void readObjectKeyframeChunk(int bytes);
		void readAmbientKeyframeChunk(int bytes);
		void readCameraKeyframeChunk(int bytes);
		void readTargetKeyframeChunk(int bytes);
		void readLightKeyframeChunk(int bytes);
		void readLightTargetKeyframeChunk(int bytes);
		void readSpotlightKeyframeChunk(int bytes);
		
		void readKeyframeNodeHeader(KeyframeNodeHeader &header);
		void readKeyframeTrackPosition(KeyframeTrackPosition &track);
		void readKeyframeTrackRotation(KeyframeTrackRotation &track);
		void readKeyframeTrackScale(KeyframeTrackScale &track);
		void readKeyframeTrackColor(KeyframeTrackColor &track);
		void readKeyframeTrackLightHotspot(KeyframeTrackLightHotspot &track);
		void readKeyframeTrackLightFalloff(KeyframeTrackLightFalloff &track);
		void readKeyframeCameraRollPosition(KeyframeCameraRollPosition &track);
		void readKeyframeCameraFieldOfView(KeyframeCameraFieldOfView &track);
		void readKeyframeTrackHeader(KeyframeTrack &track);
		void readTrackData(TrackData &data);
		void readColor(unsigned char (&color)[3]);
		void readFloatColor(float (&color)[3]);
		void updateBytesToRead(int &bytes, unsigned int length);
		unsigned short readPercent();
		float readFloatPercent();
		char *readName();
		
	private:
		int version;
		char *filename;
		KeyframeChunk *keyframe;
		ObjectChunk *object;
};

#endif
