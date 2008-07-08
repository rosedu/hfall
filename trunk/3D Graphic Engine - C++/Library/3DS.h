#ifndef __3DS_HEADER
#define __3DS_HEADER

#define MAIN_CHUNK 									0x4D4D	//
	#define M3D_VERSION								0x0002	// int version;
	#define EDITOR_CHUNK 							0x3D3D	//
		#define MESH_VERSION 						0x3D3E	// int version;
		#define MATERIAL_BLOCK 						0xAFFF	//
        	#define MATERIAL_NAME 					0xA000	// string name;
        	#define AMBIENT_COLOR 					0xA010	//
        	#define DIFFUSE_COLOR 					0xA020	//
        	#define SPECULAR_COLOR 					0xA030	//
        	#define SHININESS_PERCENT				0xA040	// shininess ratio
        	#define SHIN2PCT_PERCENT				0xA041	// shininess strength
        	#define SHIN3PCT_PERCENT				0xA042	// shininess second strength factor
        	#define TRANSPARENCY_PERCENT			0xA050	//
        	#define TRANSP_FALLOF_PERCENT			0xA052	//
        	#define REFLECTION_BLUR_PERCENT			0xA053	//
        	#define SELF_ILLUM						0xA080	//
        	#define TWO_SIDE						0xA081	// two-sided lighting
        	#define ADDITIVE						0xA083	// additive transparency blend
        	#define WIREFRAME						0xA085	// wireframe rendering
        	#define WIRESIZE						0xA087	// float size;
        	#define SHADING							0xA100	//
        	#define TEXTURE_MAP_1 					0xA200	//
        	#define SPECULAR_MAP					0xA204	//
        	#define OPACITY_MAP						0xA210	//
        	#define REFLECTION_MAP 					0xA220	//
        	#define BUMP_MAP 						0xA230	//
        	#define TEXTURE_MAP_2 					0xA33A	//
        	#define SHININESS_MAP 					0xA33C	//
        	#define TEXTURE_1_MASK 					0xA33E	//
        	#define TEXTURE_2_MASK 					0xA340	//
        	#define OPACITY_MASK 					0xA342	//
        	#define BUMP_MASK 						0xA344	//
        	#define SHININESS_MASK 					0xA346	//
        	#define SPECULAR_MASK 					0xA348	//
        	#define REFLECTION_MASK 				0xA34C	//
        	//[SUB CHUNKS FOR EACH MAP]
        		#define MAT_BUMP_PERCENT			0xA252	// unsigned short percent;
            	#define MAPPING_FILENAME 			0xA300	// string name;
            	#define MAP_TILING 					0xA351	// unsigned short tiling;
        		#define MAP_TEXBLUR					0xA353	// float blur;
        		#define MAP_U_SCALE 				0xA354	// float scale;
        		#define MAP_V_SCALE 				0xA356	// float scale;
        		#define MAP_U_OFFSET 				0xA358	// float offset;
        		#define MAP_V_OFFSET 				0xA35A	// float offset;
        		#define MAP_ANGLE 					0xA35C	// float rotation_angle;
        		#define MAP_COL1 					0xA360	// first blend colour
        		#define MAP_COL2 					0xA362	// second blend colour
        		#define MAP_R_COL 					0xA364	// red blend colour
        		#define MAP_G_COL 					0xA366	// green blend colour
        		#define MAP_B_COL					0xA368	// blue blend colour
		#define MASTER_SCALE						0x0100	// float scale;
		#define AMBIENT_LIGHT						0x2100	//
		#define MESH 								0x4000	// string name;
			#define MESH_DATA 						0x4100	//
            	#define VERTICES_LIST 				0x4110	// short nr_vert; float *vertices[3];
            	#define MAPPING_COORDINATES_LIST 	0x4140	// short nr_coord; float *coord[2];
            	#define FACES_DESCRIPTION 			0x4120	// short nr_faces; short *flags, *faces[3];
               		#define MESH_MATERIAL_GROUP 	0x4130	// string name; short nr_faces; short *faces; 
               		#define SMOOTHING_GROUP_LIST 	0x4150	// long smooth[nr_faces];
            	#define LOCAL_COORDINATES_SYSTEM 	0x4160	// float matrix[4][3];
        		#define MESH_COLOR					0x4165	// char color;
        		#define MESH_TEXTURE_INFO			0x4170	// short map_type; float tiling[2], icon[3], matrix[4][3], 
        													// scaling, plan_icon_w, plan_icon_h, cyl_icon_h
        		#define BOX_MAP						0x4190	// string mapMaterials[6];
         	#define LIGHT 							0x4600	// float position[3];
            	#define SPOTLIGHT 					0x4610	// float target[3], hot_spot, fall_off;
            		#define ROLLOFF					0x4656	// float angle;
            		#define ASPECTRATIO				0x4657	// float ratio;
            		#define SEE_CONE				0x4650	// seeCone = true;
            		#define SHADOWED				0x4630	// castsShadows = true;
            		#define LOCAL_SHADOW2			0x4641	// float params[2]; unsigned short mapSize;
            		#define RAY_BIAS				0x4658
            		#define RAYSHAD					0x4627	//
            	#define LIGHT_OFF					0x4620	//
            	#define LIGHT_ATTENUATION			0x4625	// float attenuation;
            	#define INNER_RANGE					0x4659	// float range;
            	#define OUTER_RANGE					0x465A	// float range;
            	#define MULTIPLIER					0x465B	// float multiplier;
            	#define EXCLUDE						0x4654	// string exclude;
         	#define CAMERA 							0x4700	// float position[3], target[3], bank, focus;
         		#define CAM_SEE_CONE				0x4710	// seeOutline = true;
         		#define CAM_RANGE					0x4720	// float ranges[2];
		
	#define KEYFRAME_CHUNK 							0xB000	//
		#define AMBIENT_NODE_TAG					0xB001	//
		#define OBJECT_NODE_TAG 					0xB002	//
		#define CAMERA_NODE_TAG						0xB003	//
		#define TARGET_NODE_TAG						0xB004	//
		#define LIGHT_NODE_TAG						0xB005	//
		#define LIGHT_TARGET_NODE_TAG				0xB006	//
		#define SPOTLIGHT_NODE_TAG 					0xB007	//
		#define KEYFRAME_SEGMENT 					0xB008	// unsigned int start, end;
		#define CURRENT_TIME						0xB009	// int time;
		#define KEYFRAME_HEADER						0xB00A	// unsigned short revision; string filename; int animation_length;
			#define NODE_HEADER						0xB010	// string name; short flags1, flags2, heirarchy;
			#define INSTANCE_NAME					0xB011	// string name;
            #define OBJECT_PIVOT_POINT 				0xB013	// float position[3];
            #define BOUNDING_BOX					0xB014	// float min[3], max[3];
            #define MORPH_SMOOTH					0xB015	// float morph_smoothing_angle;
            #define POSITION_TRACK 					0xB020	// unsigned short flags; int unknown[2]; nr_keys;
            												// TrackData position_track[nr_keys]; float position[nr_keys][3];
            #define ROTATION_TRACK 					0xB021	// unsigned short flags; int unknown[2]; nr_keys;
            												// TrackData rotation_track[nr_keys]; float rotation[nr_keys], axis[nr_keys][3];
            #define SCALE_TRACK 					0xB022	// unsigned short flags; int unknown[2]; nr_keys;
            												// TrackData scale_track[nr_keys]; float scale[nr_keys][3];
            #define FOV_TRACK_TAG					0xB023	// unsigned short flags; int unknown[2]; nr_keys;
            												// TrackData fov_track[nr_keys]; float fov[nr_keys];
            #define ROLL_TRACK_TAG					0xB024	// unsigned short flags; int unknown[2]; nr_keys;
            												// TrackData roll_track[nr_keys]; float roll[nr_keys];
            #define COLOR_TRACK_TAG					0xB025	// unsigned short flags; int unknown[2]; nr_keys;
            												// TrackData color_track[nr_keys]; float color[nr_keys][3];
            #define MORPH_TRACK_TAG					0xB026	// unsigned short flags; int unknown[2]; nr_keys;
            												// TrackData morph_track[nr_keys]; string name[nr_keys];
            #define HOTSPOT_TRACK_TAG				0xB027	// unsigned short flags; int unknown[2]; nr_keys;
            												// TrackData hotspot_track[nr_keys]; float angle[nr_keys];
            #define FALLOFF_TRACK_TAG				0xB028	// unsigned short flags; int unknown[2]; nr_keys;
            												// TrackData falloff_track[nr_keys]; float angle[nr_keys];
            #define NODE_ID 						0xB030	// short id;
            
            
				#define COLOR_F						0x0010	// float R,G,B
				#define COLOR_24					0x0011	// unsigned char R,G,B
				#define LIN_COLOR_24				0x0012	// unsigned char R,G,B
				#define LIN_COLOR_F					0x0013	// float R,G,B
				#define INT_PERCENTAGE				0x0030	// short percent
				#define FLOAT_PERCENTAGE			0x0031	// float percent

     
#endif
