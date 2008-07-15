""" 3DS constants """

MAIN_CHUNK                          = 0x4D4D
M3D_VERSION                         = 0x0002	# int version
EDITOR_CHUNK                        = 0x3D3D
MESH_VERSION                        = 0x3D3E
MATERIAL_BLOCK 	                    = 0xAFFF
MATERIAL_NAME 	                    = 0xA000	# string name
AMBIENT_COLOR 	                    = 0xA010
DIFFUSE_COLOR 	                    = 0xA020
SPECULAR_COLOR 	                    = 0xA030
SHININESS_PERCENT                   = 0xA040	# shininess ratio
SHIN2PCT_PERCENT                    = 0xA041	# shininess strength
SHIN3PCT_PERCENT                    = 0xA042	# shininess second strength factor
TRANSPARENCY_PERCENT		    = 0xA050
TRANSP_FALLOF_PERCENT		    = 0xA052
REFLECTION_BLUR_PERCENT		    = 0xA053
SELF_ILLUM			    = 0xA080
TWO_SIDE			    = 0xA081	# two-sided lighting
ADDITIVE			    = 0xA083	# additive transparency blend
WIREFRAME			    = 0xA085	# wireframe rendering
WIRESIZE			    = 0xA087	# float size;
SHADING				    = 0xA100
TEXTURE_MAP_1 			    = 0xA200
SPECULAR_MAP			    = 0xA204
OPACITY_MAP			    = 0xA210
REFLECTION_MAP 			    = 0xA220
BUMP_MAP 			    = 0xA230
TEXTURE_MAP_2 			    = 0xA33A
SHININESS_MAP 			    = 0xA33C
TEXTURE_1_MASK 			    = 0xA33E
TEXTURE_2_MASK 			    = 0xA340
OPACITY_MASK 			    = 0xA342
BUMP_MASK 			    = 0xA344
SHININESS_MASK 			    = 0xA346
SPECULAR_MASK 			    = 0xA348
REFLECTION_MASK                     = 0xA34C
MAPPING_FILENAME 		    = 0xA300	# string name;
MAT_BUMP_PERCENT		    = 0xA252	# unsigned short percent;
MAPPING_FILENAME 		    = 0xA300	# string name;
MAP_TILING 			    = 0xA351	# unsigned short tiling;
MAP_TEXBLUR			    = 0xA353	# float blur; 
MAP_U_SCALE 		            = 0xA354	# float scale; 
MAP_V_SCALE 		            = 0xA356	# float scale; 
MAP_U_OFFSET 		            = 0xA358	# float offset; 
MAP_V_OFFSET 		            = 0xA35A	# float offset; 
MAP_ANGLE 			    = 0xA35C	# float rotation_angle; 
MAP_COL1 			    = 0xA360	# first blend colour 
MAP_COL2 			    = 0xA362	# second blend colour 
MAP_R_COL 			    = 0xA364	# red blend colour 
MAP_G_COL 			    = 0xA366	# green blend colour 
MAP_B_COL                           = 0xA368	# blue blend colour 
MASTER_SCALE		            = 0x0100	# float scale; 
AMBIENT_LIGHT			    = 0x2100
MESH 				    = 0x4000	# string name; 
MESH_DATA 			    = 0x4100
VERTICES_LIST 			    = 0x4110	# short nr_vert; float *vertices[3]; 
MAPPING_COORDINATES_LIST 	    = 0x4140	# short nr_coord; float *coord[2]; 
FACES_DESCRIPTION 		    = 0x4120	# short nr_faces; short *flags, *faces[3]; 
MESH_MATERIAL_GROUP 	            = 0x4130	# string name; short nr_faces; short *faces;  
SMOOTHING_GROUP_LIST 	            = 0x4150	# long smooth[nr_faces]; 
LOCAL_COORDINATES_SYSTEM 	    = 0x4160	# float matrix[4][3]; 
MESH_COLOR			    = 0x4165	# char color; 
MESH_TEXTURE_INFO		    = 0x4170	# short map_type; float tiling[2], icon[3], matrix[4][3], 
        					# scaling, plan_icon_w, plan_icon_h, cyl_icon_h 
BOX_MAP			            = 0x4190	# string mapMaterials[6]; 
LIGHT 				    = 0x4600	# float position[3]; 
SPOTLIGHT 			    = 0x4610	# float target[3], hot_spot, fall_off; 
ROLLOFF			            = 0x4656	# float angle; 
ASPECTRATIO			    = 0x4657	# float ratio; 
SEE_CONE			    = 0x4650	# seeCone = true; 
SHADOWED			    = 0x4630	# castsShadows = true; 
LOCAL_SHADOW2		            = 0x4641	# float params[2]; unsigned short mapSize; 
RAY_BIAS			    = 0x4658
RAYSHAD			            = 0x4627
LIGHT_OFF			    = 0x4620
LIGHT_ATTENUATION		    = 0x4625	# float attenuation; 
INNER_RANGE			    = 0x4659	# float range; 
OUTER_RANGE			    = 0x465A	# float range; 
MULTIPLIER			    = 0x465B	# float multiplier; 
EXCLUDE				    = 0x4654	# string exclude; 
CAMERA 				    = 0x4700	# float position[3], target[3], bank, focus; 
CAM_SEE_CONE		            = 0x4710	# seeOutline = true; 
CAM_RANGE			    = 0x4720	# float ranges[2]; 
		
KEYFRAME_CHUNK 			    = 0xB000
AMBIENT_NODE_TAG		    = 0xB001
OBJECT_NODE_TAG 		    = 0xB002
CAMERA_NODE_TAG			    = 0xB003
TARGET_NODE_TAG			    = 0xB004
LIGHT_NODE_TAG			    = 0xB005
LIGHT_TARGET_NODE_TAG		    = 0xB006
SPOTLIGHT_NODE_TAG 		    = 0xB007
KEYFRAME_SEGMENT 		    = 0xB008	# unsigned int start, end; 
CURRENT_TIME			    = 0xB009	# int time; 
KEYFRAME_HEADER			    = 0xB00A	# unsigned short revision; string filename; int animation_length; 
NODE_HEADER			    = 0xB010	# string name; short flags1, flags2, heirarchy; 
INSTANCE_NAME		            = 0xB011	# string name; 
OBJECT_PIVOT_POINT 		    = 0xB013	# float position[3]; 
BOUNDING_BOX			    = 0xB014	# float min[3], max[3]; 
MORPH_SMOOTH			    = 0xB015	# float morph_smoothing_angle; 
POSITION_TRACK 			    = 0xB020	# unsigned short flags; int unknown[2]; nr_keys;
            					# TrackData position_track[nr_keys]; float position[nr_keys][3]; 
ROTATION_TRACK 			    = 0xB021	# unsigned short flags; int unknown[2]; nr_keys;
                                                # TrackData rotation_track[nr_keys]; float rotation[nr_keys], axis[nr_keys][3]; 
SCALE_TRACK 			    = 0xB022	# unsigned short flags; int unknown[2]; nr_keys;
            					# TrackData scale_track[nr_keys]; float scale[nr_keys][3]; 
FOV_TRACK_TAG			    = 0xB023	# unsigned short flags; int unknown[2]; nr_keys;
            					# TrackData fov_track[nr_keys]; float fov[nr_keys]; 
ROLL_TRACK_TAG			    = 0xB024	# unsigned short flags; int unknown[2]; nr_keys;
            					# TrackData roll_track[nr_keys]; float roll[nr_keys]; 
COLOR_TRACK_TAG			    = 0xB025	# unsigned short flags; int unknown[2]; nr_keys;
            					# TrackData color_track[nr_keys]; float color[nr_keys][3]; 
MORPH_TRACK_TAG			    = 0xB026	# unsigned short flags; int unknown[2]; nr_keys;
            					# TrackData morph_track[nr_keys]; string name[nr_keys]; 
HOTSPOT_TRACK_TAG		    = 0xB027	# unsigned short flags; int unknown[2]; nr_keys;
                                                # TrackData hotspot_track[nr_keys]; float angle[nr_keys]; 
FALLOFF_TRACK_TAG		    = 0xB028	# unsigned short flags; int unknown[2]; nr_keys;
            					# TrackData falloff_track[nr_keys]; float angle[nr_keys]; 
NODE_ID 			    = 0xB030	# short id; 
            
            
COLOR_F			            = 0x0010	# float R,G,B 
COLOR_24			    = 0x0011	# unsigned char R,G,B 
LIN_COLOR_24		            = 0x0012	# unsigned char R,G,B 
LIN_COLOR_F			    = 0x0013	# float R,G,B 
INT_PERCENTAGE		            = 0x0030	# short percent 
FLOAT_PERCENTAGE		    = 0x0031	# float percent 
