varying vec3 n;
varying vec3 v;

uniform int numLights;

void main()
{
	vec3 V = normalize(-v);
	gl_FragColor = vec4(0.0);
	float outerCosCutoff = 0.8;

	vec4 globalAmbient = vec4(0.0);
	
	for(int i = 1; i < gl_MaxLights; i++)
	{
		if(i <= 1)
		{
			vec3 L = normalize(gl_LightSource[i].position.xyz - v); 
			
			float dist = length(L);
			float spotEffect = 1.0;
			float cosCutoff = 1.1;
			
			if(gl_LightSource[i].spotCutoff != 0.0)
			{
				vec3 spotDirection = normalize(gl_LightSource[i].spotDirection);
				cosCutoff = dot(spotDirection, -L);
				spotEffect = pow(cosCutoff, gl_LightSource[i].spotExponent);
			}
			
			if(cosCutoff > gl_LightSource[i].spotCosCutoff)
			{
				float atten = spotEffect / (gl_LightSource[i].constantAttenuation +
			           gl_LightSource[i].linearAttenuation * dist +
			           gl_LightSource[i].quadraticAttenuation * dist * dist);
			           
			    vec3 N = normalize(n);
				float NdotL = dot(N, L);
			           
				//calculate Ambient Term:
				globalAmbient += gl_LightSource[i].ambient;
				
				if(NdotL > 0.0)
				{
					vec3 R = normalize(-reflect(L, N));
					
					//calculate Diffuse Term:
					vec4 Idiff = gl_FrontLightProduct[i].diffuse * max(NdotL, 0.0);
					
					// calculate Specular Term:
					vec4 Ispec = gl_FrontLightProduct[i].specular * pow(max(dot(R, V), 0.0), gl_FrontMaterial.shininess);
					gl_FragColor += atten*(Idiff + Ispec);
				}
			}
			/*else if(cosCutoff > outerCosCutoff)
			{
				float atten = spotEffect / (gl_LightSource[i].constantAttenuation +
			           gl_LightSource[i].linearAttenuation * dist +
			           gl_LightSource[i].quadraticAttenuation * dist * dist);
			
				float falloff = (cosCutoff - outerCosCutoff) / (gl_LightSource[i].spotCosCutoff - outerCosCutoff);
				vec3 N = normalize(n);
				float NdotL = dot(N, L);
				
				//calculate Ambient Term:
				globalAmbient += gl_LightSource[i].ambient;
				
				if(NdotL > 0.0)
				{
					vec3 R = normalize(-reflect(L, N));	
				
					//calculate Diffuse Term:
					vec4 Idiff = gl_FrontLightProduct[i].diffuse * max(dot(N, L), 0.0) * falloff;
					
					// calculate Specular Term:
					vec4 Ispec = gl_FrontLightProduct[i].specular * pow(max(dot(R, V),0.0), gl_FrontMaterial.shininess) * falloff;
					gl_FragColor += atten*(Idiff + Ispec);
				}
			}*/
		}
	}
	globalAmbient *= gl_FrontMaterial.ambient;
	gl_FragColor += gl_FrontMaterial.emission + globalAmbient;
	gl_FragColor *= gl_Color;
}