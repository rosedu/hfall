#include "MaxParser.h"
#include "3DS.h"
#include "Debug.h"
#include <string.h>
#include <stdlib.h>

FILE *f;


MaxParser::MaxParser(const char *file)
{
	keyframe = NULL;
	object = new ObjectChunk();
	setFile(file);
}
MaxParser::MaxParser()
{
	keyframe = NULL;
	object = new ObjectChunk(); 
}
MaxParser::~MaxParser() {}
void MaxParser::setFile(const char *file)
{
	filename = (char *)malloc(strlen(file)*sizeof(char));
	strcpy(filename,file);
}
void MaxParser::readChunkHeader(ChunkHeader &h)
{
	h.start_position = ftell(f);
	fread(&h.chunk_id,2,1,f);
	fread(&h.chunk_length,4,1,f);
}
bool MaxParser::parse(bool obj, bool anim)
{
	if(anim) keyframe = new KeyframeChunk();
	if(!obj) object = NULL;
	return parse();
}
bool MaxParser::parse()
{
	if(!filename)
	{
		debugPrintf("No file\n");
		return false;
	}
	if(!strstr(filename,".3ds"))
	{
		debugPrintf("Invalid source file extension\nExtension must be .3ds\n");
		return false;
	}
	f = fopen(filename,"rb");
	if(!f)
	{
		debugPrintf("No file %s\n",filename);
		return false;
	}
	ChunkHeader h;
	readChunkHeader(h);
	if(h.chunk_id != MAIN_CHUNK)
	{
		debugPrintf("Invalid 3ds file\n");
		fclose(f);
		return false;
	}
	debugPrintf("Main Chunk\n");
	readMainChunk(h.chunk_length - 6);
	int end_position = ftell(f);
	fseek(f,0,SEEK_END);
	int eof = ftell(f);
	fclose(f);
	if(eof != end_position) return false;
	return true;
}

void MaxParser::readMainChunk(int bytes)
{
	ChunkHeader h;
	while (bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case M3D_VERSION:
			{
				fread(&version,sizeof(int),1,f);
				debugPrintf(" Version: %d\n",version);
				break;
			}
			case EDITOR_CHUNK:
			{
				if(object == NULL) break;
				debugPrintf(" EditorChunk\n");
				readObjectChunk(h.chunk_length - 6);
				break;
			}
			case KEYFRAME_CHUNK:
			{
				if(keyframe == NULL) break;
				debugPrintf(" Key Frame\n");
				readKeyframeChunk(h.chunk_length - 6);
				break;
			}
			default: debugPrintf(" Skip unknown %X subchunk\n",h.chunk_id);
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
}

void MaxParser::readObjectChunk(int bytes)
{
	ChunkHeader h;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case MESH_VERSION:
			{
				fread(&object->version,sizeof(int),1,f);
				debugPrintf("  Mesh Version: %d\n",object->version);
				break;
			}
			case MATERIAL_BLOCK:
			{
				debugPrintf("  Material\n");
				readMaterialChunk(h.chunk_length - 6);
				break;
			}
			case MASTER_SCALE:
			{
				fread(&object->masterScale,sizeof(float),1,f);
				debugPrintf("  Master scale: %.2f\n",object->masterScale);
				break;
			}
			case AMBIENT_LIGHT:
			{
				debugPrintf("  Ambient light: ");
				readFloatColor(object->ambientLight);
				break;
			}
			case MESH:
			{
				debugPrintf("  Mesh\n");
				readMeshChunk(h.chunk_length - 6);
				break;
			}
			default: debugPrintf("  Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
}

void MaxParser::readMaterialChunk(int bytes)
{
	MaterialChunk m;
	ChunkHeader h;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case MATERIAL_NAME:
			{
				m.name = readName();
				debugPrintf("   Name: %s\n",m.name);	
				break;
			}
			case AMBIENT_COLOR:
			{
				debugPrintf("   Ambient color: ");
				readColor(m.ambientColor);
				break;
			}
			case DIFFUSE_COLOR:
			{
				debugPrintf("   Diffuse color: ");
				readColor(m.diffuseColor);
				break;
			}
			case SPECULAR_COLOR:
			{
				debugPrintf("   Specular color: ");
				readColor(m.specularColor);
				break;
			}
			case SHININESS_PERCENT:
			{
				debugPrintf("   Shininess percent: ");
				m.shininess = readPercent();
				break;
			}
			case SHIN2PCT_PERCENT:
			{
				debugPrintf("   Shininess strength: ");
				m.shininessStrength = readPercent();
				break;
			}
			case SHIN3PCT_PERCENT:
			{
				debugPrintf("   Shininess second strength: ");
				m.secondShininessStrength = readPercent();
				break;
			}
			case TRANSPARENCY_PERCENT:
			{
				debugPrintf("   Transparency percent: ");
				m.transparency = readPercent();
				break;
			}
			case TRANSP_FALLOF_PERCENT	:
			{
				debugPrintf("   Transparency Fallof percent: ");
				m.transparencyFallof = readPercent();
				break;
			}
			case REFLECTION_BLUR_PERCENT:
			{
				debugPrintf("   Refelection Blur percent: ");
				m.reflectionBlur = readPercent();
				break;
			}
			case SELF_ILLUM:
			{
				debugPrintf("   Self illuminated\n");
				m.isSelfIlluminated = true;
				break;
			}
			case TWO_SIDE:
			{
				debugPrintf("   Two-sided lighting\n");
				m.twoSided = true;
				break;
			}
			case ADDITIVE:
			{
				debugPrintf("   Aditive blend\n");
				m.aditive = true;
				break;
			}
			case WIREFRAME:
			{
				debugPrintf("   Wireframe\n");
				m.wireframe = true;
				break;
			}
			case WIRESIZE:
			{
				fread(&m.wireSize,sizeof(float),1,f);
				debugPrintf("   Wire size: %.2f\n",m.wireSize);
				break;
			}
			case SHADING:
			{
				fread(&m.shadingType,2,1,f);
				debugPrintf("   Shading: %d\n",m.shadingType);
				break;
			}
			case TEXTURE_MAP_1:
			{
				debugPrintf("   Texture Map 1\n");
				debugPrintf("    Percentage: ");
				readTextureChunk(m.textureMap1,h.chunk_length - 6);
				break;
			}
			case TEXTURE_MAP_2:
			{
				debugPrintf("   Texture Map 2\n");
				debugPrintf("    Percentage: ");
				readTextureChunk(m.textureMap2,h.chunk_length - 6);
				break;
			}
			case BUMP_MAP:
			{
				debugPrintf("   Bump Map\n");
				debugPrintf("    Percentage: ");
				readTextureChunk(m.bumpMap,h.chunk_length - 6);
				break;
			}
			case SPECULAR_MAP:
			{
				debugPrintf("   Specular Map\n");
				debugPrintf("    Percentage: ");
				readTextureChunk(m.specularMap,h.chunk_length - 6);
				break;
			}
			case REFLECTION_MAP:
			{
				debugPrintf("   Reflection Map\n");
				debugPrintf("    Percentage: ");
				readTextureChunk(m.reflectionMap,h.chunk_length - 6);
				break;
			}
			case OPACITY_MAP:
			{
				debugPrintf("   Opacity Map\n");
				debugPrintf("    Percentage: ");
				readTextureChunk(m.opacityMap,h.chunk_length - 6);
				break;
			}
			case SHININESS_MAP:
			{
				debugPrintf("   Shininess Map\n");
				debugPrintf("    Percentage: ");
				readTextureChunk(m.shininessMap,h.chunk_length - 6);
				break;
			}
			case TEXTURE_1_MASK:
			{
				debugPrintf("   Texture 1 mask");
				readTextureChunk(m.textureMask1,h.chunk_length - 6);
				break;
			}
			case TEXTURE_2_MASK:
			{
				debugPrintf("   Texture 2 mask");
				readTextureChunk(m.textureMask2,h.chunk_length - 6);
				break;
			}
			case OPACITY_MASK:
			{
				debugPrintf("   Opacity Mask");
				readTextureChunk(m.opacityMask,h.chunk_length - 6);
				break;
			}
			case BUMP_MASK:
			{
				debugPrintf("   Bump Mask");
				readTextureChunk(m.bumpMask,h.chunk_length - 6);
				break;
			}
			case SHININESS_MASK:
			{
				debugPrintf("   Shininess Mask");
				readTextureChunk(m.shininessMask,h.chunk_length - 6);
				break;
			}
			case SPECULAR_MASK:
			{
				debugPrintf("   Specular Mask");
				readTextureChunk(m.specularMask,h.chunk_length - 6);
				break;
			}
			case REFLECTION_MASK:
			{
				debugPrintf("   Reflection Mask");
				readTextureChunk(m.reflectionMask,h.chunk_length - 6);
				break;
			}
			default: debugPrintf("   Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
	object->materials.add(m);
}
void MaxParser::readTextureChunk(TextureChunk &texture, int bytes)
{
	ChunkHeader h;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case INT_PERCENTAGE:
			{
				fread(&texture.percentage,2,1,f);
				debugPrintf("%d\n",texture.percentage);
				break;
			}
			case MAPPING_FILENAME:
			{
				texture.name = readName();
				debugPrintf("    Filename: %s\n",texture.name);
				break;
			}
			case MAP_TEXBLUR:
			{
				fread(&texture.blur,sizeof(float),1,f);
				debugPrintf("    Texture blur: %.2f\n",texture.blur);
				break;
			}
			case MAP_TILING:
			{
				fread(&texture.tiling,sizeof(unsigned short),1,f);
				debugPrintf("    Texture tiling: %d\n",texture.tiling);
				break;
			}
			case MAP_ANGLE:
			{
				fread(&texture.rotationAngle,sizeof(float),1,f);
				debugPrintf("    Rotation angle: %.2f\n",texture.rotationAngle);
				break;
			}
			case MAP_U_SCALE:
			{
				fread(&texture.uScale,sizeof(float),1,f);
				debugPrintf("    U Scale: %.2f\n",texture.uScale);
				break;
			}
			case MAP_V_SCALE:
			{
				float scale;
				fread(&texture.vScale,sizeof(float),1,f);
				debugPrintf("    V Scale: %.2f\n",texture.vScale);
				break;
			}
			case MAP_U_OFFSET:
			{
				fread(&texture.uOffset,sizeof(float),1,f);
				debugPrintf("    U Offset: %.2f\n",texture.uOffset);
				break;
			}
			case MAP_V_OFFSET:
			{
				fread(&texture.vOffset,sizeof(float),1,f);
				debugPrintf("    V Offset: %.2f\n",texture.vOffset);
				break;
			}
			case MAP_COL1:
			{
				debugPrintf("    Color 1: ");
				readColor(texture.firstBlendColor);
				break;
			}
			case MAP_COL2:
			{
				debugPrintf("    Color 2: ");
				readColor(texture.secondBlendColor);
				break;
			}
			case MAP_R_COL:
			{
				debugPrintf("    R_Color: ");
				readColor(texture.redBlendColor);
				break;
			}
			case MAP_G_COL:
			{
				debugPrintf("    G_Color: ");
				readColor(texture.greenBlendColor);
				break;
			}
			case MAP_B_COL:
			{
				debugPrintf("    B_Color: ");
				readColor(texture.blueBlendColor);
				break;
			}
			case MAT_BUMP_PERCENT:
			{
				fread(&texture.bumpPercentage,sizeof(unsigned short),1,f);
				debugPrintf("    Bump percent: %d\n",texture.bumpPercentage);
				break;
			}
			default: debugPrintf("    Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
}

void MaxParser::readMeshChunk(int bytes)
{
	MeshChunk m;
	m.name = readName();
	debugPrintf("   Name: %s\n",m.name);
	bytes-= (strlen(m.name)+1)*sizeof(char);
	ChunkHeader h;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case MESH_DATA:
			{
				m.type = 1;
				debugPrintf("   Mesh data\n");
				readMeshData(m.data, h.chunk_length - 6);
				break;
			}
			case LIGHT:
			{
				m.type = 2;
				debugPrintf("   Light\n");
				readLightChunk(m.light, h.chunk_length - 6);
				break;
			}
			case CAMERA:
			{
				m.type = 3;
				debugPrintf("   Camera\n");
				readCameraChunk(m.camera, h.chunk_length - 6);
				break;
			}
			default: debugPrintf("   Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
	object->meshes.add(m);
}

void MaxParser::readMeshData(MeshData &mesh, int bytes)
{
	ChunkHeader h;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case VERTICES_LIST:
			{
				fread(&mesh.nrOfVertices,2,1,f);
				mesh.vertices = (float *) malloc(3*mesh.nrOfVertices*sizeof(float));
				int j = 0;
				for(int i = 0; i<mesh.nrOfVertices; i++)
				{
					fread(&mesh.vertices[j],sizeof(float),3,f);
					j+= 3;
				}
				debugPrintf("    Number of vertices: %d\n",mesh.nrOfVertices);
				break;
			}
			case MAPPING_COORDINATES_LIST:
			{
				fread(&mesh.nrOfCoordrinates,2,1,f);
				mesh.coordinates = (float *) malloc(2*mesh.nrOfCoordrinates*sizeof(float));
				int j = 0;
				for(int i = 0; i<mesh.nrOfCoordrinates; i++)
				{
					fread(&mesh.coordinates[j],sizeof(float),2,f);
					j+= 2;
				}
				debugPrintf("    Number of map coordonates: %d\n",mesh.nrOfCoordrinates);
				break;
			}
			case FACES_DESCRIPTION:
			{
				readFacesChunk(mesh.faces, h.chunk_length - 6);
				break;
			}
			case LOCAL_COORDINATES_SYSTEM:
			{
				fread(&mesh.matrix,sizeof(float),12,f);
				debugPrintf("    Mesh Matrix\n");
				debugPrintf("     %.2f %.2f %.2f\n",mesh.matrix[0][0],mesh.matrix[0][1],mesh.matrix[0][2]);
				debugPrintf("     %.2f %.2f %.2f\n",mesh.matrix[1][0],mesh.matrix[1][1],mesh.matrix[1][2]);
				debugPrintf("     %.2f %.2f %.2f\n",mesh.matrix[2][0],mesh.matrix[2][1],mesh.matrix[2][2]);
				debugPrintf("     %.2f %.2f %.2f\n",mesh.matrix[3][0],mesh.matrix[3][1],mesh.matrix[3][2]);
				break;
			}
			case MESH_COLOR:
			{
				fread(&mesh.color,sizeof(unsigned char),1,f);
				debugPrintf("    Mesh color: %d\n",mesh.color);
				break;
			}
			case MESH_TEXTURE_INFO:
			{
				fread(&mesh.textureInfo.mapType,sizeof(unsigned short),1,f);
				fread(&mesh.textureInfo.tiling,sizeof(float),2,f);
				fread(&mesh.textureInfo.icon,sizeof(float),3,f);
				fread(&mesh.textureInfo.matrix,sizeof(float),12,f);
				fread(&mesh.textureInfo.planIconW,sizeof(float),1,f);
				fread(&mesh.textureInfo.planIconH,sizeof(float),1,f);
				fread(&mesh.textureInfo.cylIconH,sizeof(float),1,f);
				debugPrintf("    Mesh Texture info\n");
				break;
			}
			case BOX_MAP:
			{
				debugPrintf("    Box Map\n");
				for(int i=0; i<6; i++)
				{
					mesh.mapMaterials[i] = readName();
					debugPrintf("     %s\n",mesh.mapMaterials[i]);
				}
				break;
			}
			default: debugPrintf("    Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
}

void MaxParser::readFacesChunk(FacesChunk &faces, int bytes)
{
	fread(&faces.nrOfFaces,sizeof(unsigned short),1,f);
	faces.flags = (unsigned short *) malloc(faces.nrOfFaces*sizeof(unsigned short));
	faces.faces = (unsigned short *) malloc(3*faces.nrOfFaces*sizeof(unsigned short));
	int j = 0;
	for(int i = 0; i<faces.nrOfFaces; i++)
	{
		fread(&faces.faces[j],sizeof(unsigned short),3,f);
		fread(&faces.flags[i],sizeof(unsigned short),1,f);
		j+= 3;
	}
	debugPrintf("    Number of faces: %d\n",faces.nrOfFaces);
	bytes-= faces.nrOfFaces*8 + 2;
	ChunkHeader h;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case MESH_MATERIAL_GROUP:
			{
				MaterialGroupChunk group;
				group.materialName = readName();
				fread(&group.nrOfFaces,sizeof(unsigned short),1,f);
				group.faces = (unsigned short *) malloc(group.nrOfFaces*sizeof(unsigned short));
				for(int i = 0; i<group.nrOfFaces; i++)
					fread(&group.faces[i],sizeof(unsigned short),1,f);
				debugPrintf("    Mesh Group\n");
				debugPrintf("     Material name: %s\n",group.materialName);
				debugPrintf("     Number of faces: %d\n",group.nrOfFaces);
				faces.materialGroups.add(group);
				break;
			}
			case SMOOTHING_GROUP_LIST:
			{
				faces.smoothingList = (long *) malloc(faces.nrOfFaces*sizeof(long));
				for(int i=0;i<faces.nrOfFaces;i++)
					fread(&faces.smoothingList[i],4,1,f);
				debugPrintf("    Face Smoothing Group\n");
				break;
			}
			default: debugPrintf("    Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
}

void MaxParser::readLightChunk(LightChunk &light, int bytes)
{
	fread(&light.position,sizeof(float),3,f);
	debugPrintf("    Position: %.2f %.2f %.2f\n",light.position[0],light.position[1],light.position[2]);
	debugPrintf("    Color: ");
	readFloatColor(light.color);
	bytes -= 6*sizeof(float) + 6;
	ChunkHeader h;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case SPOTLIGHT:
			{
				debugPrintf("    Spot Light\n");
				readSpotLigthChunk(light.spotLight, h.chunk_length - 6);
				break;
			}
			case LIGHT_OFF:
			{
				debugPrintf("    Light off\n");
				light.lightOff = true;
				break;
			}
			case LIGHT_ATTENUATION:
			{
				fread(&light.attenuation,sizeof(float),1,f);
				debugPrintf("    Attenuation: %.2f\n",light.attenuation);
				break;
			}
			case INNER_RANGE:
			{
				fread(&light.innerRange,sizeof(float),1,f);
				debugPrintf("    Inner range: %.2f\n",light.innerRange);
				break;
			}
			case OUTER_RANGE:
			{
				fread(&light.outerRange,sizeof(float),1,f);
				debugPrintf("    Outer range: %.2f\n",light.outerRange);
				break;
			}
			case MULTIPLIER:
			{
				fread(&light.multiplier,sizeof(float),1,f);
				debugPrintf("    Multiplier: %.2f\n",light.multiplier);
				break;
			}
			case EXCLUDE:
			{
				light.exclude = readName();
				debugPrintf("  Mesh\n");
				debugPrintf("   Name: %s\n",light.exclude);
				break;
			}
			default: debugPrintf("    Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
}

void MaxParser::readSpotLigthChunk(SpotLightChunk &spot, int bytes)
{
	fread(&spot.target,sizeof(float),3,f);
	fread(&spot.hotSpot,sizeof(float),1,f);
	fread(&spot.fallOff,sizeof(float),1,f);
	debugPrintf("     Target: %.2f %.2f %.2f\n",spot.target[0],spot.target[1],spot.target[2]);
	debugPrintf("     Hot Spot: %.2f\n",spot.hotSpot);
	debugPrintf("     Fall Off: %.2f\n",spot.fallOff);
	bytes -= 5*sizeof(float);
	ChunkHeader h;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case ROLLOFF:
			{
				fread(&spot.rolloffAngle,sizeof(float),1,f);
				debugPrintf("     Rollof angle: %.2f\n",spot.rolloffAngle);
				break;
			}
			case ASPECTRATIO:
			{
				fread(&spot.aspectRatio,sizeof(float),1,f);
				debugPrintf("     Aspect Ratio: %.2f\n",spot.aspectRatio);
				break;
			}
			case SEE_CONE:
			{
				spot.seeCone = true;
				debugPrintf("     See cone\n");
				break;
			}
			case SHADOWED:
			{
				spot.castsShadows = true;
				debugPrintf("     Shadowed\n");
				break;
			}
			case LOCAL_SHADOW2:
			{
				fread(&spot.localShadow,sizeof(float),2,f);
				fread(&spot.mapSize,sizeof(unsigned short),1,f);
				debugPrintf("     Local shadow\n");
				debugPrintf("      Map size: %d\n",spot.mapSize);
				debugPrintf("      Parameters: %.2f %.2f\n",spot.localShadow[0],spot.localShadow[1]);
				break;
			}
			default: debugPrintf("     Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
}

void MaxParser::readCameraChunk(CameraChunk &camera, int bytes)
{
	fread(&camera.position,sizeof(float),3,f);
	fread(&camera.target,sizeof(float),3,f);
	fread(&camera.bankAngle,sizeof(float),1,f);
	fread(&camera.focus,sizeof(float),1,f);
	debugPrintf("    Position: %.2f %.2f %.2f\n",camera.position[0],camera.position[1],camera.position[2]);
	debugPrintf("    Target: %.2f %.2f %.2f\n",camera.target[0],camera.target[1],camera.target[2]);
	debugPrintf("    Bank angle: %.2f\n",camera.bankAngle);
	debugPrintf("    Focus: %.2f\n",camera.focus);
	bytes -= 8*sizeof(float);
	ChunkHeader h;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case CAM_SEE_CONE:
			{
				camera.seeOutline = true;
				debugPrintf("    See Outline\n");
				break;
			}
			case CAM_RANGE:
			{
				fread(&camera.ranges,sizeof(float),2,f);
				debugPrintf("    Ranges: %.2f %.2f\n",camera.ranges[0],camera.ranges[1]);
				break;
			}
			default: debugPrintf("    Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
}

void MaxParser::readKeyframeChunk(int bytes)
{
	ChunkHeader h;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case KEYFRAME_HEADER:
			{
				fread(&keyframe->header.revision,sizeof(unsigned short),1,f);
				keyframe->header.filename = readName();
				fread(&keyframe->header.animationLength,sizeof(int),1,f);
				debugPrintf("  Header\n");
				debugPrintf("   Revision: %d\n",keyframe->header.revision);
				debugPrintf("   Filename: %s\n",filename);
				debugPrintf("   Animation length %d\n",keyframe->header.animationLength);
				break;
			}
			case KEYFRAME_SEGMENT:
			{
				fread(&keyframe->startFrame,sizeof(unsigned int),1,f);
				fread(&keyframe->endFrame,sizeof(unsigned int),1,f);
				debugPrintf("  Frames\n   start: %d\n   end: %d\n",keyframe->startFrame,keyframe->endFrame);
				break;
			}
			case CURRENT_TIME:
			{
				fread(&keyframe->currentTime,sizeof(int),1,f);
				debugPrintf("  Current time: %d\n",keyframe->currentTime);
				break;
			}
			/*case AMBIENT_NODE_TAG:
			{
				debugPrintf("  Ambient keyframe data\n");
				readAmbientKeyframeChunk(h.chunk_length - 6);
				break;
			}*/
			case OBJECT_NODE_TAG:
			{
				debugPrintf("  Object keyframe data\n");
				readObjectKeyframeChunk(h.chunk_length - 6);
				break;
			}
			case CAMERA_NODE_TAG:
			{
				debugPrintf("  Camera keyframe data\n");
				readCameraKeyframeChunk(h.chunk_length - 6);
				break;
			}
			case TARGET_NODE_TAG:
			{
				debugPrintf("  Target keyframe data\n");
				readTargetKeyframeChunk(h.chunk_length - 6);
				break;
			}
			case LIGHT_NODE_TAG:
			{
				debugPrintf("  Light keyframe data\n");
				readLightKeyframeChunk(h.chunk_length - 6);
				break;
			}
			case LIGHT_TARGET_NODE_TAG:
			{
				debugPrintf("  Light-target keyframe data\n");
				readLightTargetKeyframeChunk(h.chunk_length - 6);
				break;
			}
			case SPOTLIGHT_NODE_TAG:
			{
				debugPrintf("  Spotlight keyframe data\n");
				readSpotlightKeyframeChunk(h.chunk_length - 6);
				break;
			}
			default: debugPrintf("  Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
}

void MaxParser::readObjectKeyframeChunk(int bytes)
{
	ChunkHeader h;
	ObjectKeyframeChunk obj;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case NODE_ID:
			{
				fread(&obj.nodeID,sizeof(unsigned short),1,f);
				debugPrintf("   Node ID: %d\n",obj.nodeID);
				break;
			}
			case NODE_HEADER:
			{
				readKeyframeNodeHeader(obj.nodeHeader);
				break;
			}
			case OBJECT_PIVOT_POINT:
			{
				fread(&obj.pivotPosition,sizeof(float),3,f);
				debugPrintf("   Pivot: %.2f %.2f %.2f\n",obj.pivotPosition[0],obj.pivotPosition[1],obj.pivotPosition[2]);
				break;
			}
			case INSTANCE_NAME:
			{
				obj.instanceName = readName();
				debugPrintf("   Instance name: %s\n",obj.instanceName);
				break;
			}
			case POSITION_TRACK:
			{
				readKeyframeTrackPosition(obj.trackPosition);
				break;
			}
			case ROTATION_TRACK:
			{
				readKeyframeTrackRotation(obj.trackRotation);
				break;
			}
			case SCALE_TRACK:
			{
				readKeyframeTrackScale(obj.trackScale);
				break;
			}
			case BOUNDING_BOX:
			{
				fread(&obj.box.min,sizeof(float),3,f);
				fread(&obj.box.max,sizeof(float),3,f);
				debugPrintf("   Bounding box\n");
				debugPrintf("    min: %.2f %.2f %.2f\n",obj.box.min[0],obj.box.min[1],obj.box.min[2]);
				debugPrintf("    max: %.2f %.2f %.2f\n",obj.box.max[0],obj.box.max[1],obj.box.max[2]);
				break;
			}
			default: debugPrintf("   Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
	keyframe->objectKeyframes.add(obj);
}

void MaxParser::readSpotlightKeyframeChunk(int bytes)
{
	ChunkHeader h;
	SpotlightKeyframeChunk spot;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case NODE_ID:
			{
				fread(&spot.nodeID,sizeof(unsigned short),1,f);
				debugPrintf("   Node ID: %d\n",spot.nodeID);
				break;
			}
			case NODE_HEADER:
			{
				readKeyframeNodeHeader(spot.nodeHeader);
				break;
			}
			case POSITION_TRACK:
			{
				readKeyframeTrackPosition(spot.trackPosition);
				break;
			}
			case COLOR_TRACK_TAG:
			{
				readKeyframeTrackColor(spot.trackColor);
				break;
			}
			case HOTSPOT_TRACK_TAG:
			{
				readKeyframeTrackLightHotspot(spot.trackLightHotspot);
				break;
			}
			case FALLOFF_TRACK_TAG:
			{
				readKeyframeTrackLightFalloff(spot.trackLightFalloff);
				break;
			}
			case ROLL_TRACK_TAG:
			{
				readKeyframeCameraRollPosition(spot.cameraRollPosition);
				break;
			}
			default: debugPrintf("   Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
	keyframe->spotlightKeyframes.add(spot);
}

void MaxParser::readLightTargetKeyframeChunk(int bytes)
{
	ChunkHeader h;
	LightTargetKeyframeChunk target;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case NODE_ID:
			{
				fread(&target.nodeID,sizeof(unsigned short),1,f);
				debugPrintf("   Node ID: %d\n",target.nodeID);
				break;
			}
			case NODE_HEADER:
			{
				readKeyframeNodeHeader(target.nodeHeader);
				break;
			}
			case POSITION_TRACK:
			{
				readKeyframeTrackPosition(target.trackPosition);
				break;
			}
			default: debugPrintf("   Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
	keyframe->lightTargetKeyframes.add(target);
}

void MaxParser::readLightKeyframeChunk(int bytes)
{
	ChunkHeader h;
	LightKeyframeChunk light;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case NODE_ID:
			{
				fread(&light.nodeID,sizeof(unsigned short),1,f);
				debugPrintf("   Node ID: %d\n",light.nodeID);
				break;
			}
			case NODE_HEADER:
			{
				readKeyframeNodeHeader(light.nodeHeader);
				break;
			}
			case POSITION_TRACK:
			{
				readKeyframeTrackPosition(light.trackPosition);
				break;
			}
			case COLOR_TRACK_TAG:
			{
				readKeyframeTrackColor(light.trackColor);
				break;
			}
			default: debugPrintf("   Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
	keyframe->lightKeyframes.add(light);
}

void MaxParser::readCameraKeyframeChunk(int bytes)
{
	ChunkHeader h;
	CameraKeyframeChunk camera;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case NODE_ID:
			{
				fread(&camera.nodeID,sizeof(unsigned short),1,f);
				debugPrintf("   Node ID: %d\n",camera.nodeID);
				break;
			}
			case NODE_HEADER:
			{
				readKeyframeNodeHeader(camera.nodeHeader);
				break;
			}
			case POSITION_TRACK:
			{
				readKeyframeTrackPosition(camera.trackPosition);
				break;
			}
			case FOV_TRACK_TAG:
			{
				readKeyframeCameraFieldOfView(camera.cameraFieldOfView);
				break;
			}
			case ROLL_TRACK_TAG:
			{
				readKeyframeCameraRollPosition(camera.cameraRollPosition);
				break;
			}
			default: debugPrintf("   Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
	keyframe->cameraKeyframes.add(camera);
}

void MaxParser::readTargetKeyframeChunk(int bytes)
{
	ChunkHeader h;
	TargetKeyframeChunk target;
	while(bytes)
	{
		readChunkHeader(h);
		switch(h.chunk_id)
		{
			case NODE_ID:
			{
				fread(&target.nodeID,sizeof(unsigned short),1,f);
				debugPrintf("   Node ID: %d\n",target.nodeID);
				break;
			}
			case NODE_HEADER:
			{
				readKeyframeNodeHeader(target.nodeHeader);
				break;
			}
			case POSITION_TRACK:
			{
				readKeyframeTrackPosition(target.trackPosition);
				break;
			}
			default: debugPrintf("   Skip unknown %X subchunk\n",h.chunk_id);
	
		}
		fseek(f,h.start_position + h.chunk_length,SEEK_SET);
		updateBytesToRead(bytes, h.chunk_length);
	}
	keyframe->targetKeyframes.add(target);
}
			

void MaxParser::readKeyframeNodeHeader(KeyframeNodeHeader &header)
{
	header.name = readName();
	fread(&header.flags,sizeof(unsigned short),2,f);
	fread(&header.heirarchy,sizeof(unsigned short),1,f);
	debugPrintf("   Name: %s\n",header.name);
	debugPrintf("   flag1: %d; flag2: %d\n",header.flags[0],header.flags[1]);
	debugPrintf("   Heirarchy: %d\n",header.heirarchy);
}

void MaxParser::readKeyframeTrackPosition(KeyframeTrackPosition &track)
{
	readKeyframeTrackHeader(track);
	track.position = (float3 *) malloc(track.nrOfKeys*3*sizeof(float));
	for(int i=0; i<track.nrOfKeys; i++)
	{
		readTrackData(track.trackData[i]);
		fread(&track.position[i],sizeof(float),3,f);
	}
	debugPrintf("   Keyframe track position block\n");
}

void MaxParser::readKeyframeTrackRotation(KeyframeTrackRotation &track)
{
	readKeyframeTrackHeader(track);
	track.rotation = (float *) malloc(track.nrOfKeys*sizeof(float));
	track.axis = (float3 *) malloc(track.nrOfKeys*3*sizeof(float));
	for(int i=0; i<track.nrOfKeys; i++)
	{
		readTrackData(track.trackData[i]);
		fread(&track.rotation[i],sizeof(float),1,f);
		fread(&track.axis[i],sizeof(float),3,f);
	}
	debugPrintf("   Keyframe track rotation block\n");
}

void MaxParser::readKeyframeTrackScale(KeyframeTrackScale &track)
{
	readKeyframeTrackHeader(track);
	track.scale = (float3 *) malloc(track.nrOfKeys*3*sizeof(float));
	for(int i=0; i<track.nrOfKeys; i++)
	{
		readTrackData(track.trackData[i]);
		fread(&track.scale[i],sizeof(float),3,f);
	}
	debugPrintf("   Keyframe track scale block\n");
}

void MaxParser::readKeyframeTrackColor(KeyframeTrackColor &track)
{
	readKeyframeTrackHeader(track);
	track.color = (float3 *) malloc(track.nrOfKeys*3*sizeof(float));
	for(int i=0; i<track.nrOfKeys; i++)
	{
		readTrackData(track.trackData[i]);
		fread(&track.color[i],sizeof(float),3,f);
	}
	debugPrintf("   Keyframe track color block\n");
}

void MaxParser::readKeyframeTrackLightHotspot(KeyframeTrackLightHotspot &track)
{
	readKeyframeTrackHeader(track);
	track.angle = (float *) malloc(track.nrOfKeys*sizeof(float));
	for(int i=0; i<track.nrOfKeys; i++)
	{
		readTrackData(track.trackData[i]);
		fread(&track.angle[i],sizeof(float),1,f);
	}
	debugPrintf("   Keyframe track light hotspot block\n");
}

void MaxParser::readKeyframeTrackLightFalloff(KeyframeTrackLightFalloff &track)
{
	readKeyframeTrackHeader(track);
	track.angle = (float *) malloc(track.nrOfKeys*sizeof(float));
	for(int i=0; i<track.nrOfKeys; i++)
	{
		readTrackData(track.trackData[i]);
		fread(&track.angle[i],sizeof(float),1,f);
	}
	debugPrintf("   Keyframe track light falloff block\n");
}

void MaxParser::readKeyframeCameraRollPosition(KeyframeCameraRollPosition &track)
{
	readKeyframeTrackHeader(track);
	track.roll = (float *) malloc(track.nrOfKeys*sizeof(float));
	for(int i=0; i<track.nrOfKeys; i++)
	{
		readTrackData(track.trackData[i]);
		fread(&track.roll[i],sizeof(float),1,f);
	}
	debugPrintf("   Keyframe camera roll position block\n");
}

void MaxParser::readKeyframeCameraFieldOfView(KeyframeCameraFieldOfView &track)
{
	readKeyframeTrackHeader(track);
	track.fieldOfView = (float *) malloc(track.nrOfKeys*sizeof(float));
	for(int i=0; i<track.nrOfKeys; i++)
	{
		readTrackData(track.trackData[i]);
		fread(&track.fieldOfView[i],sizeof(float),1,f);
	}
	debugPrintf("   Keyframe camera field of view block\n");
}

void MaxParser::readKeyframeTrackHeader(KeyframeTrack &track)
{
	fread(&track.flags,sizeof(unsigned short),1,f);
	fread(&track.unknown,4,2,f);
	fread(&track.nrOfKeys,sizeof(int),1,f);
	track.trackData = (TrackData *) malloc(track.nrOfKeys*sizeof(TrackData));
}

void MaxParser::readTrackData(TrackData &data)
{
	fread(&data.frameNumber,sizeof(int),1,f);
	fread(&data.splineFlags,sizeof(unsigned short),1,f);
	if(data.splineFlags != 0)
	{
		if(data.splineFlags & 0x01 != 0 )
			fread(&data.splineData[0],sizeof(float),1,f);
		if(data.splineFlags & 0x02 != 0 )
			fread(&data.splineData[1],sizeof(float),1,f);
		if(data.splineFlags & 0x04 != 0 )
			fread(&data.splineData[2],sizeof(float),1,f);
		if(data.splineFlags & 0x08 != 0 )
			fread(&data.splineData[3],sizeof(float),1,f);
		if(data.splineFlags & 0x10 != 0 )
			fread(&data.splineData[4],sizeof(float),1,f);
	}
}


char *MaxParser::readName()
{
	char *name = (char *) malloc(20*sizeof(char));
	int i = 0;
	do
		fread(&name[i++],1,1,f);
	while(name[i-1] != '\0');
	return name;
}
void MaxParser::readColor(unsigned char (&rgb)[3])
{
	ChunkHeader h;
	readChunkHeader(h);
	switch(h.chunk_id)
	{
		case COLOR_24:
		case LIN_COLOR_24:
		{
			fread(&rgb,1,3,f);
			debugPrintf("%d %d %d\n",rgb[0],rgb[1],rgb[2]);
			break;
		}
		default: debugPrintf("Skip unknown %X subchunk\n",h.chunk_id);

	}
	fseek(f,h.start_position + h.chunk_length,SEEK_SET);
}
void MaxParser::readFloatColor(float (&rgb)[3])
{
	ChunkHeader h;
	readChunkHeader(h);
	switch(h.chunk_id)
	{
		case LIN_COLOR_F:
		case COLOR_F:
		{
			fread(&rgb,sizeof(float),3,f);
			debugPrintf("%.2f %.2f %.2f\n",rgb[0],rgb[1],rgb[2]);
			break;
		}
		default: debugPrintf("Skip unknown %X subchunk\n",h.chunk_id);

	}
	fseek(f,h.start_position + h.chunk_length,SEEK_SET);
}
unsigned short MaxParser::readPercent()
{
	ChunkHeader h;
	readChunkHeader(h);
	unsigned short percent;
	switch(h.chunk_id)
	{
		case INT_PERCENTAGE:
		{
			fread(&percent,2,1,f);
			debugPrintf("%d\n",percent);
			break;
		}
		default: debugPrintf("Skip unknown %X subchunk\n",h.chunk_id);

	}
	fseek(f,h.start_position + h.chunk_length,SEEK_SET);
	return percent;
}
float MaxParser::readFloatPercent()
{
	ChunkHeader h;
	readChunkHeader(h);
	float percent;
	switch(h.chunk_id)
	{
		case FLOAT_PERCENTAGE:
		{
			fread(&percent,sizeof(float),1,f);
			debugPrintf("%.2f\n",percent);
			break;
		}
		default: debugPrintf("Skip unknown %X subchunk\n",h.chunk_id);

	}
	fseek(f,h.start_position + h.chunk_length,SEEK_SET);
	return percent;
}

void MaxParser::updateBytesToRead(int &bytes, unsigned int length)
{
	if(length == 0) { bytes = 0; return; }
	bytes -= length;
	if(bytes < 0)
	{
		fseek(f,bytes,SEEK_CUR);
		bytes = 0;
	}
}
